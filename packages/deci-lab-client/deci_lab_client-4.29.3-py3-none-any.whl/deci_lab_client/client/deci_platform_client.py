import io
import logging
import os
import re
import threading
import time
import urllib.parse
import urllib.request
from contextlib import contextmanager, redirect_stdout
from pathlib import Path
from timeit import default_timer
from typing import TYPE_CHECKING, overload
from uuid import uuid4
from warnings import warn

import requests
from deci_common.abstractions.abstract_logger import get_logger
from requests import Response

from deci_lab_client.api.platform_api import PlatformApi
from deci_lab_client.client.api_client import ApiClient
from deci_lab_client.client.configuration import Configuration
from deci_lab_client.client.exceptions import (
    BenchmarkRequestError,
    BenchmarkResultNotFoundException,
    PyTorchNotInstalledError,
    TimeoutWasReachedBeforeBenchmarkFinishedError,
    UnsupportedLoadedModelFramework,
)
from deci_lab_client.client.helpers import (
    TqdmUpTo,
    build_gru_request_form,
    build_model_metadata,
    wait_until,
)
from deci_lab_client.exceptions import ApiException
from deci_lab_client.models import (
    AddModelResponse,
    APIResponse,
    BodyAddModelV2,
    BodySendModelBenchmarkRequest,
    DeepLearningTask,
    ExperimentForm,
    FrameworkType,
    HardwareType,
    LogRequestBody,
    Metric,
    ModelBenchmarkResultMetadata,
    ModelBenchmarkState,
    ModelMetadata,
    ModelOptimizationState,
    ModelSource,
    OptimizationRequestForm,
    OptimizeModelResponse,
    QuantizationLevel,
    SentryLevel,
)
from deci_lab_client.types.s3_signed_url import S3SignedUrl

if TYPE_CHECKING:
    from collections.abc import Generator, Mapping, Sequence
    from typing import Any, Literal, Optional, Union
    from uuid import UUID

    from torch import nn

    from deci_lab_client.models import (
        APIResponseAddModelResponse,
        BaselineModelResponseMetadata,
    )


def get_docstring_from(original_function):
    """
    A decorator that attaches the docstring one function to another function in real time
    (for transparent auto completion).
    """

    def doc_wrapper(target):
        target.__doc__ = original_function.__doc__
        return target

    return doc_wrapper


class AddAndOptimizeResponse:
    def __init__(
        self,
        model_id: "Optional[UUID]" = None,
        benchmark_request_id: "Optional[UUID]" = None,
        optimized_model_id: "Optional[UUID]" = None,
        optimization_request_id: "Optional[UUID]" = None,
    ):
        self.model_id = model_id
        self.benchmark_request_id = benchmark_request_id
        self.optimized_model_id = optimized_model_id
        self.optimization_request_id = optimization_request_id


class DeciPlatformClient(PlatformApi):
    """
    A wrapper for OpenAPI's generated client http library to deci's API.
    Extends the functionality of generated platform client and ease it's usage and experience.
    """

    def __init__(self, proxy_headers=None, logger=None, **kwargs: "Any"):
        self._logger = logger or get_logger(logger_name="deci_platform_client")

        configuration = Configuration(proxy_headers=proxy_headers)
        client_config = ApiClient(configuration=configuration)
        super().__init__(client_config)

        self.experiment = None
        self.experiments_pool: "dict[str, threading.Thread]" = dict()

        client_id = os.getenv("DECI_CLIENT_ID")
        secret = os.getenv("DECI_CLIENT_SECRET")
        if client_id is not None and secret is not None:
            self.login(client_id=client_id, secret=secret)

    def login(self, client_id: "Optional[str]" = None, secret: "Optional[str]" = None, **kwargs: "Any") -> None:
        """
        Login to the platform.

        :param client_id: The user's client ID generated in the Deci platform.
        :type client_id: str
        :param secret: The user's secret generated in the Deci platform.
        :type secret: str
        """
        if not client_id or not secret:
            return
        self.api_client.set_up_frontegg_auth(client_id=client_id, secret=secret)
        self._logger.info(
            f"Successfully logged in as {self.api_client.email} (Workspace ID - {self.api_client.workspace_id})."
        )

    def logout(self):
        """
        Log out of the platform (Disposes the credentials).
        """
        self.api_client.tear_down_frontegg_auth()
        self._logger.info("Successfully logged out.")

    def _prepare_model(
        self,
        model_metadata: "ModelMetadata",
        model: "Optional[nn.Module]",
        inputs_metadata: "Optional[Mapping[str, Mapping[str, Any]]]",
        **kwargs: "Any",
    ) -> "Optional[str]":
        model_path: "Optional[str]" = None
        if model is not None:
            if model_metadata.framework == FrameworkType.PYTORCH:
                with self.support(tag="pytorch-to-onnx"):
                    model_path = self.convert_pytorch_to_onnx(
                        local_loaded_model=model,
                        inputs_metadata=inputs_metadata,
                        **kwargs,
                    )
                model_metadata.framework = FrameworkType.ONNX
            else:
                raise UnsupportedLoadedModelFramework
        model_metadata.source = ModelSource.SDK
        self.assert_model_arguments(model_metadata=model_metadata)
        return model_path

    def _add_model_start(
        self,
        model_metadata: "ModelMetadata",
        model: "Optional[nn.Module]" = None,
        model_path: "Optional[str]" = None,
        inputs_metadata: "Optional[Mapping[str, Mapping[str, Any]]]" = None,
        **kwargs: "Any",
    ) -> "str":
        if (model is not None and model_path is not None) or (model is None and model_path is None):
            raise TypeError(
                f"Exactly one of model and model_path parameters must be specified,"
                f" received model={model}, model_path={model_path}"
            )

        converted_pytorch_model_path = self._prepare_model(
            model_metadata=model_metadata, model=model, inputs_metadata=inputs_metadata, **kwargs
        )

        self.assert_model_arguments(model_metadata=model_metadata)
        storage_etag = self._upload_file_to_s3(
            converted_pytorch_model_path if converted_pytorch_model_path is not None else model_path,
            model_metadata.name,
        )

        if converted_pytorch_model_path is not None:
            try:
                os.remove(converted_pytorch_model_path)
            except (OSError, UnboundLocalError):
                pass

        return storage_etag

    def add_model_v2(
        self,
        model_metadata: "ModelMetadata",
        hardware_types: "list[str]",
        model_path: "Optional[str]" = None,
        model: "Optional[nn.Module]" = None,
        **kwargs: "Any",
    ):
        """
        Adds a new model to the company's model repository, using the new v2 endpoint.
        The new model arguments are passed to the API, and the model itself is uploaded to s3 from the local machine.
        For pytorch model is expected, for other framework use model_local path instead.
        :param model_metadata: The model metadata.
        :param hardware_types: The hardware types you want to benchmark the model on.
        :param model_path: The path of the model on the local operating system.
        :param model: Pytorch loaded model object.
        if your model's framework is pytorch you may pass the following parameters as kwargs
            in order to control the conversion to onnx:
        :param kwargs: Extra arguments to be passed to the PyTorch to ONNX conversion, for example:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        warn("This method is deprecated, please migrate to using the new 'register_model' method")
        storage_etag = self._add_model_start(
            model_metadata=model_metadata,
            model=model,
            model_path=model_path,
            **kwargs,
        )
        return super(DeciPlatformClient, self).add_model_v2(
            etag=storage_etag,
            body_add_model_v2=BodyAddModelV2(model=model_metadata, hardware_types=hardware_types),
        )

    @overload
    def register_model(
        self,
        model: "nn.Module",
        *,
        name: str,
        framework: "Literal['pytorch']",
        dl_task: str = DeepLearningTask.OTHER,
        inputs_metadata: "Mapping[str, Mapping[str, Any]]",
        input_dimensions: "Optional[Literal[None]]" = None,
        hardware_types: "Optional[list[str]]" = None,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        dataset_name: "Optional[str]" = None,
        target_metric: "Optional[str]" = None,
        target_metric_value: "Optional[float]" = None,
        model_size: "Optional[float]" = None,
        memory_footprint: "Optional[float]" = None,
        **kwargs: "Any",
    ) -> "APIResponseAddModelResponse":
        ...

    @overload
    def register_model(
        self,
        model: "Union[Path, str]",
        *,
        name: str,
        framework: "Union[Literal['tf2'], Literal['keras'], Literal['onnx']]",
        dl_task: str = DeepLearningTask.OTHER,
        inputs_metadata: "Optional[Literal[None]]" = None,
        input_dimensions: "Optional[Union[Sequence[int], Sequence[Sequence[int]]]]" = None,
        hardware_types: "Optional[list[str]]" = None,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        dataset_name: "Optional[str]" = None,
        target_metric: "Optional[str]" = None,
        target_metric_value: "Optional[float]" = None,
        model_size: "Optional[float]" = None,
        memory_footprint: "Optional[float]" = None,
        **kwargs: "Any",
    ) -> "APIResponseAddModelResponse":
        ...

    def register_model(
        self,
        model: "Union[Path, str, nn.Module]",
        *,
        name: str,
        framework: "Literal['tf2', 'keras', 'onnx', 'pytorch']",
        dl_task: str = DeepLearningTask.OTHER,
        inputs_metadata: "Optional[Mapping[str, Mapping[str, Any]]]" = None,
        input_dimensions: "Optional[Union[Sequence[int], Sequence[Sequence[int]]]]" = None,
        hardware_types: "Optional[list[str]]" = None,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        dataset_name: "Optional[str]" = None,
        target_metric: "Optional[str]" = None,
        target_metric_value: "Optional[float]" = None,
        model_size: "Optional[float]" = None,
        memory_footprint: "Optional[float]" = None,
        **kwargs: "Any",
    ) -> "APIResponseAddModelResponse":
        """
        Registers a new model to the company's model repository, using the new v2 endpoint.
        The new model arguments are passed to the API, and the model itself is uploaded to s3 from the local machine.
        If the model's framework is PyTorch, it will first be converted to ONNX.
        :param model: PyTorch loaded model object or path to the model's file.
        :param name: The model's name.
        :param framework: The model's framework.
                          Allowed values can be seen in deci_lab_client.FrameworkType.
        :param dl_task: The deep learning task of the model.
                        Allowed values can be seen in deci_lab_client.DeepLearningTask.
        :param inputs_metadata: A dictionary that describes the inputs of the model, needed for pytroch upload, ex:
            >>> {\
                    "input0": {\
                        "dtype": np.float32,\
                        "shape": (1, 3, 224, 224),\
                    },\
                    ...\
                }
            where batch size is up to 64 and the first input dimension is (3, 224, 224).
        :param input_dimensions: The model's input dimensions.
                                 Currently only a single tuple (or list) of integers is supported for PyTorch models.
        :param hardware_types: A list of hardware types to benchmark the model on. Optional.
                               Allowed values can be seen in deci_lab_client.HardwareType.
        :param accuracy: The model's accuracy, as a float. Optional.
        :param description: The model's description. Optional.
        :param dataset_name: The name of a similar dataset to that your model was trained on. Optional.
        :param target_metric: The model's target metric. Optional.
                              Allowed values can be seen in deci_lab_client.Metric.
        :param target_metric_value: The model's target metric value. Optional.
        :param model_size: The model's target size. Optional.
        :param memory_footprint: The model's target memory footprint. Optional.
        :param kwargs: You may pass the following parameters as kwargs in order to control the conversion to onnx:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        if framework == FrameworkType.PYTORCH:
            from torch import nn

            if not isinstance(model, nn.Module):
                raise TypeError(f"Model parameter must be a nn.Module, received {type(model)}")
            if inputs_metadata is None:
                raise TypeError(
                    "Model inputs metadata must be specified when uploading pytorch models. Refer to the documentation of this function"
                )
            if not all(
                "shape" in input_metadata and "dtype" in input_metadata for input_metadata in inputs_metadata.values()
            ):
                raise TypeError(
                    "Model inputs metadata must have a 'dtype' and 'shape' key. Refer to the documentation of this function"
                )
            input_dimensions = [list(input_metadata["shape"][1:]) for input_metadata in inputs_metadata.values()]
            kwargs["model"] = model
        else:
            kwargs["model_path"] = model
            if input_dimensions is None:
                input_dimensions = []

        model_metadata = build_model_metadata(
            name=name,
            framework=framework,
            dl_task=dl_task,
            input_dimensions=input_dimensions,
            primary_hardware=hardware_types[0] if hardware_types else None,
            accuracy=accuracy,
            description=description,
            dataset_name=dataset_name,
            target_metric=target_metric,
            target_metric_value=target_metric_value,
            model_size=model_size,
            memory_footprint=memory_footprint,
        )
        kwargs.pop("model_metadata", None)
        kwargs.pop("channel_first", None)
        kwargs["inputs_metadata"] = inputs_metadata

        storage_etag = self._add_model_start(model_metadata=model_metadata, **kwargs)
        return super(DeciPlatformClient, self).add_model_v2(
            etag=storage_etag,
            body_add_model_v2=BodyAddModelV2(model=model_metadata, hardware_types=hardware_types or [HardwareType.T4]),
        )

    def add_pytorch_model(
        self,
        model: "nn.Module",
        *,
        name: str,
        dl_task: str,
        input_dimensions: "Sequence[int]",
        hardware_types: "Optional[list[str]]" = None,
        channel_first: bool = True,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        **kwargs: "Any",
    ) -> "APIResponseAddModelResponse":
        """
        Adds a new PyTorch model to the company's model repository, using the new v2 endpoint.
        The new model arguments are passed to the API,
        and the model itself is converted to ONNX and uploaded to s3 from the local machine.
        :param model: Pytorch loaded model object.
        :param name: The model's name.
        :param dl_task: The deep learning task of the model.
                        Allowed values can be seen in deci_lab_client.DeepLearningTask.
        :param input_dimensions: The model's input dimensions.
                                 Currently only a single tuple (or list) of integers is supported.
        :param hardware_types: A list of hardware types to benchmark the model on. Optional.
                               Allowed values can be seen in deci_lab_client.HardwareType.
        :param channel_first: Whether the first dimension is for the number of channels (True, the default),
                              or the last one is (False).
        :param accuracy: The model's accuracy, as a float. Optional.
        :param description: The model's description. Optional.
        :param kwargs: You may pass the following parameters as kwargs in order to control the conversion to onnx:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        warn("This method is deprecated, please migrate to using the new 'register_model' method")
        return self.register_model(
            model=model,
            name=name,
            framework=FrameworkType.PYTORCH,
            dl_task=dl_task,
            input_dimensions=input_dimensions,
            hardware_types=hardware_types,
            channel_first=channel_first,
            accuracy=accuracy,
            description=description,
            **kwargs,
        )

    def add_and_optimize_pytorch_model(
        self,
        model: "nn.Module",
        *,
        name: str,
        dl_task: str,
        input_dimensions: "Sequence[int]",
        hardware_types: "Optional[list[str]]" = None,
        channel_first: bool = True,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        primary_batch_size: int,
        quantization_level: str,
        raw_format: bool = False,
        **kwargs: "Any",
    ):
        """
        Adds a new PyTorch model to the company's model repository, using the new v2 endpoint.
        The new model arguments are passed to the API,
        and the model itself is converted to ONNX and uploaded to s3 from the local machine.
        :param model: Pytorch loaded model object.
        :param name: The model's name.
        :param dl_task: The deep learning task of the model.
                        Allowed values can be seen in deci_lab_client.DeepLearningTask.
        :param input_dimensions: The model's input dimensions.
                                 Currently only a single tuple (or list) of integers is supported.
        :param hardware_types: A list of hardware types to benchmark the model on. Optional.
                               Allowed values can be seen in deci_lab_client.HardwareType.
        :param channel_first: Whether the first dimension is for the number of channels (True, the default),
                              or the last one is (False).
        :param accuracy: The model's accuracy, as a float. Optional.
        :param description: The model's description. Optional.
        :param primary_batch_size: The model's primary batch size. Optional.
                                   Allowed values can be seen in deci_lab_client.BatchSize
                                   and deci_lab_client.BatchSize.
        :param quantization_level: The quantization level to optimize for. Optional.
                                   Allowed values can be seen in deci_lab_client.QuantizationLevel.
        :param raw_format: Whether the optimized model should be saved in raw format or not. Optional.
        :param kwargs: You may pass the following parameters as kwargs in order to control the conversion to onnx:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        add_model_response = self.register_model(
            model=model,
            name=name,
            framework=FrameworkType.PYTORCH,
            dl_task=dl_task,
            input_dimensions=input_dimensions,
            hardware_types=hardware_types,
            channel_first=channel_first,
            accuracy=accuracy,
            description=description,
            **kwargs,
        )
        model_id = add_model_response.data.model_id
        return self.gru_model(
            model_id=model_id,
            gru_request_form=build_gru_request_form(
                batch_size=primary_batch_size,
                quantization_level=quantization_level,
                target_hardware_types=hardware_types,
                raw_format=raw_format,
            ),
        )

    def add_pytorch_architecture(
        self,
        model: "nn.Module",
        *,
        name: str,
        dl_task: str,
        input_dimensions: "Sequence[int]",
        primary_hardware_type: "Optional[str]" = None,
        primary_batch_size: int,
        quantization_level: str,
        channel_first: bool = True,
        accuracy: "Optional[float]" = None,
        description: "Optional[str]" = None,
        dataset_name: "Optional[str]" = None,
        target_metric: "Optional[str]" = None,
        target_metric_value: "Optional[float]" = None,
        model_size: "Optional[float]" = None,
        memory_footprint: "Optional[float]" = None,
        raw_format: bool = False,
        **kwargs: "Any",
    ):
        """
        Adds a new PyTorch architecture to the company's model repository, using the new v2 endpoint,
        and requesting an AutoNAC optimization on that model.
        The new model arguments are passed to the API,
        and the model itself is converted to ONNX and uploaded to s3 from the local machine.
        :param model: Pytorch loaded model object.
        :param name: The model's name.
        :param dl_task: The deep learning task of the model.
                        Allowed values can be seen in deci_lab_client.DeepLearningTask.
        :param input_dimensions: The model's input dimensions.
                                 Currently only a single tuple (or list) of integers is supported.
        :param primary_hardware_type: The primary hardware type to benchmark the model and create the AutoNAC model on. Optional.
                               Allowed values can be seen in deci_lab_client.HardwareType.
        :param channel_first: Whether the first dimension is for the number of channels (True, the default),
                              or the last one is (False).
        :param accuracy: The model's accuracy, as a float. Optional.
        :param description: The model's description. Optional.
        :param dataset_name: The name of a similar dataset to that your model was trained on. Optional.
        :param target_metric: The AutoNAC model's target metric. Optional.
                              Allowed values can be seen in deci_lab_client.Metric.
        :param target_metric_value: The AutoNAC model's target metric value. Optional.
        :param model_size: The AutoNAC model's target model size. Optional.
        :param memory_footprint: The AutoNAC model's target memory footprint. Optional.
        :param primary_batch_size: The model's primary batch size. Optional, defaults to 1.
                                   Allowed values can be seen in deci_lab_client.BatchSize
                                   and deci_lab_client.BatchSize.
        :param quantization_level: The quantization level to optimize for. Optional, defaults to FP16.
                                   Allowed values can be seen in deci_lab_client.QuantizationLevel.
        :param raw_format: Whether the optimized model should be saved in raw format or not. Optional.
        :param kwargs: You may pass the following parameters as kwargs in order to control the conversion to onnx:
            opset_version
            do_constant_folding
            dynamic_axes
            input_names
            output_names
        """
        kwargs.pop("model_metadata", None)
        hardware_types = [primary_hardware_type] if primary_hardware_type is not None else None
        add_model_response = self.register_model(
            model=model,
            name=name,
            framework=FrameworkType.PYTORCH,
            dl_task=dl_task,
            input_dimensions=input_dimensions,
            hardware_types=hardware_types,
            channel_first=channel_first,
            accuracy=accuracy,
            description=description,
            dataset_name=dataset_name,
            target_metric=target_metric,
            target_metric_value=target_metric_value,
            model_size=model_size,
            memory_footprint=memory_footprint,
            **kwargs,
        )
        model_id = add_model_response.data.model_id
        self.autonac_model(model_id=model_id)
        return self.gru_model(
            model_id=model_id,
            gru_request_form=build_gru_request_form(
                batch_size=primary_batch_size,
                quantization_level=quantization_level,
                target_hardware_types=hardware_types,
                target_metric=target_metric,
                raw_format=raw_format,
            ),
        )

    def add_model(
        self,
        add_model_request: ModelMetadata,
        optimization_request: OptimizationRequestForm = None,
        model_local_path: str = None,
        local_loaded_model=None,
        wait_async=False,
        **kwargs,
    ):
        """
        DEPRECATED
        Adds a new model to the company's model repository.
        The new model arguments are passed to the API, and the model itself is uploaded to s3 from the local machine.
        For pytorch local_loaded_model is expected, for other framework use model_local path instead.
        :param add_model_request: The model metadata
        :param optimization_request: The params to due optimize the model, if not given model will not be optimized. You can always request the optimization later.
        :param model_local_path: The path of the model on the local operating system.
        :param local_loaded_model: Pytorch loaded model object.
        :param wait_async: If true function will wait unitl the benchmark process was finished, otherwise will return on request acknowledgement.
        if your model's framework is pytorch you may pass the following parameters as kwargs in order to control the conversion to onnx:
        :param opset_version
        :param do_constant_folding
        :param dynamic_axes
        :param input_names
        :param output_names
        """
        warn("This method is deprecated, please migrate to using the new 'register_model' method")
        s3_file_etag = self._add_model_start(
            model_metadata=add_model_request,
            model=local_loaded_model,
            model_path=model_local_path,
            **kwargs,
        )

        try:
            # Adding the model metadata via the API, after verification that the file exists.
            add_model_response: AddModelResponse = super(DeciPlatformClient, self).add_model(
                model_metadata_in=add_model_request, etag=s3_file_etag, **kwargs
            )
            response = AddAndOptimizeResponse(**add_model_response.data.to_dict())
            new_model_id = add_model_response.data.model_id
            if wait_async and not optimization_request:
                return_value = wait_until(
                    self._wait_for_benchmark_to_finish, 20 * 60, optimized_model_id=str(new_model_id)
                )
                if not return_value:
                    raise TimeoutWasReachedBeforeBenchmarkFinishedError
        except Exception as ex:
            self._logger.error(f"Failed to add the model to the repository. {ex}")
            raise ex
        else:
            self._logger.info("Successfully added the model to the repository.")
            self._logger.info(
                "Starting to benchmark the model on the required hardware types. "
                f"You can check the status on https://console.deci.ai/insights/{response.model_id} or by querying the platform."
            )
        if not optimization_request:
            return APIResponse(success=True, message=add_model_response.message, data=response)
        # Requesting to optimize the added model metadata via the API.
        optimize_model_response: OptimizeModelResponse = super(DeciPlatformClient, self).optimize_model(
            model_id=new_model_id, optimization_request_form=optimization_request, **kwargs
        )
        response_dict = response.__dict__
        response_dict.update(optimize_model_response.data.to_dict())
        response = AddAndOptimizeResponse(**response_dict)
        if wait_async:
            return_value = wait_until(
                self._wait_for_benchmark_to_finish, 20 * 60, model_id=str(response.optimized_model_id)
            )
            if return_value:
                self._logger.info(
                    f"Successfully added and optimized {str(return_value.name)} on your model repository. "
                    f"You can see the benchmark results at https://console.deci.ai/insights/{add_model_response.data.model_id}/optimized/{optimize_model_response.data.optimized_model_id}"
                )
            else:
                raise TimeoutWasReachedBeforeBenchmarkFinishedError

        return APIResponse(
            success=True,
            message="Successfully added the model to the model repository and optimized it. ",
            data=response,
        )

    def download_model(self, model_id: str, dest_path: "Optional[str]" = None, show_progress=True) -> Path:
        """
        Downloads a model with the specified UUID to the specified path.
        :param model_id: The model UUID
        :param dest_path: The full path to which the model will be written to, will download to current working directory if None supplied
        :param show_progress: Whether to show the current progress of download
        :return path to the downloaded model
        """
        download_url = self.get_model_signed_url_for_download(model_id=model_id)
        if not dest_path:
            filename = re.findall('filename="(.+)"&', urllib.parse.unquote(download_url.data))[0]
            dest_path = Path.cwd().joinpath(filename)
        self._logger.info("Downloading...")
        with TqdmUpTo(**TqdmUpTo.DOWNLOAD_PARAMS, desc=str(dest_path)) as t:
            urllib.request.urlretrieve(
                url=download_url.data, filename=dest_path, reporthook=t.update_to if show_progress else None
            )
        self._logger.info(f"The model was downloaded to {dest_path}")
        return dest_path

    def _all_models(self) -> "list[ModelMetadata]":
        models = self.get_all_models()
        return [model for model in models.data if not model.deleted]

    def find_model_id(self, model_name: str) -> ModelMetadata:
        return next((model for model in self._all_models() if model.name == model_name), None)

    @staticmethod
    @contextmanager
    def redirect_output() -> "Generator[tuple[io.StringIO, io.StringIO], Any, None]":
        root_logger = logging.getLogger()
        logs = io.StringIO()
        handler = logging.StreamHandler(logs)
        handler.setLevel(logging.DEBUG)
        root_logger.addHandler(handler)
        with redirect_stdout(io.StringIO()) as stdout:
            yield stdout, logs

        root_logger.removeHandler(handler)

    def send_support_logs(
        self,
        *,
        log: str,
        tag: "Optional[str]" = None,
        level: "Optional[SentryLevel]" = None,
    ) -> None:
        if len(log) == 0:
            self._logger.info("No logs detected, not sending anything.")
            return
        log_request_body = LogRequestBody(log=log, tag=tag, level=level)
        self.log(log_request_body=log_request_body)
        self._logger.info("Successfully sent support logs.")

    @contextmanager
    def support(
        self,
        tag: "Optional[str]" = None,
        level: "Optional[SentryLevel]" = None,
    ) -> "Generator[None, None, Any]":
        exception: "Optional[Exception]" = None
        with self.redirect_output() as (stdout, logs):
            try:
                yield
            except Exception as e:
                exception = e
        log = "\n".join(["stdout:", stdout.getvalue(), "logging:", logs.getvalue()])
        self.send_support_logs(log=log, tag=tag, level=level)
        if exception is not None:
            raise exception

    @staticmethod
    def convert_pytorch_to_onnx(
        local_loaded_model: "nn.Module",
        inputs_metadata: "Mapping[str, Mapping[str, Any]]",
        export_path: "Optional[str]" = None,
        opset_version=15,
        do_constant_folding=True,
        dynamic_axes: "Mapping[str, Any]" = None,
        **kwargs: "Any",
    ) -> str:
        """
        Convert PyTorch model to ONNX.
        :param local_loaded_model: Pytorch loaded model object (nn.Module).
        :param inputs_metadata: A dictionary that describes the inputs of the model, ex:
            >>> {\
                    "input0": {\
                        "dtype": np.float32,\
                        "shape": (1, 3, 224, 224),\
                    },\
                    ...\
                }
            where batch size is up to 64 and the first input dimension is (3, 224, 224).
        :param export_path: Path to where to save the converted model file.
            If not given "converted_model_{time.time()}.onnx" will be used.

        You may pass the following parameters as kwargs in order to control the conversion to onnx:
        :param opset_version
        :param do_constant_folding
        """
        import numpy as np

        model_inputs = []
        input_dimensions = []
        try:
            import torch
        except Exception as e:
            raise PyTorchNotInstalledError from e

        # Building the dummy inputs
        for input_name, input_metadata in inputs_metadata.items():
            input_shape, input_dtype = input_metadata["shape"], input_metadata["dtype"]
            input_size = tuple(input_shape)
            if np.issubdtype(input_dtype, int):
                _input = torch.randint(low=1, high=255, size=input_size, requires_grad=False)
            else:
                _input = torch.randn(size=input_size, requires_grad=False)
            model_inputs.append(_input)
            input_dimensions.append(input_size)

        model_path = export_path if export_path is not None else f"converted_model_{time.time()}.onnx"

        # Export the model
        local_loaded_model.eval()  # Put model into eval mode
        # if hasattr(local_loaded_model, "prep_model_for_conversion"):
        #     logging.warning(
        #         "SgModules currently support only 1 input when prepping a model for conversion; feeding index 0 and ignoring the rest of the inputs;"

        logging.info(f"Running torch.jit.trace on model with input dimensions {input_dimensions}")
        try:
            local_loaded_model = torch.jit.trace(local_loaded_model, example_inputs=model_inputs, strict=False)
            logging.info("Successfully traced model.")
        except torch.jit.TracingCheckError as e:
            logging.warning("Error tracing model")
            logging.warning(e)

        logging.info(f"Exporting model to ONNX with opset version {opset_version}")
        try:
            torch.onnx.export(
                model=local_loaded_model,  # Model being run
                # a torch tensor contains the model input dims and the primary_batch_size.
                args=model_inputs[0] if len(model_inputs) == 1 else model_inputs,
                f=model_path,  # Where to save the model (can be a file or file-like object)
                export_params=True,  # Store the trained parameter weights inside the model file
                opset_version=opset_version,  # The ONNX version to export the model to
                do_constant_folding=do_constant_folding,  # Whether to execute constant folding for optimization
                dynamic_axes=dynamic_axes,  # The dynamic axes names for every input
                **kwargs,
            )
        except Exception as e:
            logging.error("Error converting model")
            logging.error(e)
            raise
        logging.info(f"Successfully exported model to {model_path}")

        return model_path

    def _wait_for_benchmark_to_finish(self, model_id: str):
        your_model_from_repo = self.get_model_by_id(model_id=model_id).data
        if your_model_from_repo.benchmark_state not in [ModelBenchmarkState.IN_PROGRESS, ModelBenchmarkState.PENDING]:
            return your_model_from_repo
        return False

    def _upload_file_to_s3(self, model_local_path: str, model_name: str, model_version: "Optional[str]" = None):
        with open(model_local_path, "rb") as f:
            # Upload the model to the s3 bucket of the company
            signed_url_upload_request = self.get_model_signed_url_for_upload(
                model_name=model_name, model_version=model_version
            )
            upload_request_parameters = signed_url_upload_request.data
            requests.post(upload_request_parameters["url"], data=[])
            self._logger.info("Uploading the model file...")
            files = {"file": (upload_request_parameters["fields"]["key"], f)}
            http_response = requests.post(
                upload_request_parameters["url"], data=upload_request_parameters["fields"], files=files
            )
            # Getting the s3 created Etag from the http headers, and passing it to the 'add_model' call
            s3_file_etag = http_response.headers.get("ETag")  # Verify the model was uploaded
            http_response.raise_for_status()
            self._logger.info("Finished uploading the model file.")
            return s3_file_etag

    # TODO: Make the above method to use the one that follows. Ensure good naming conventions.
    @staticmethod
    def upload_file_to_s3(from_path: str, s3_signed_url: S3SignedUrl) -> Response:
        with open(from_path, "rb") as file:
            files = {"file": (s3_signed_url.fields["key"], file)}
            http_response = requests.post(s3_signed_url.url, files=files, data=s3_signed_url.fields)
            return http_response

    def register_experiment(self, name: str, model_name: "Optional[str]" = None, resume: bool = True) -> None:
        """
        Registers a training experiment in Deci's backend

        :param name: The experiment name
        :param model_name: The model name that being run in the experiment. Optional.
        :param resume: Resume the experiment `name` by uploading files to the existing experiment folder alongside any existing files.
                       If `resume=False` - archive all previously existing experiment `name` files. True by default.
        """
        try:
            response = self.start_experiment(
                experiment_form=ExperimentForm(name=name, model_name=model_name, resume=resume)
            )
            if not response.success:
                raise ApiException

            self.experiment = response.data
        except Exception:
            self._logger.error(f"Failed to register experiment {name}")

    def save_experiment_file(self, file_path: str) -> "threading.Thread":
        """
        Uploads a training related file to Deci's location in S3. This can be a TensorBoard file or a log

        :param file_path: The local path of the file to be uploaded
        """

        def save(path: str, existing_thread: "Optional[threading.Thread]") -> None:
            # If there's already an upload schedule for the same file kill it
            if existing_thread:
                self._logger.debug("There's already a thread trying to upload the same filename")
                existing_thread.join()
                self._logger.debug("Old thread finished. We'll create a new one")

            if not os.path.exists(path):
                self._logger.warning("We didn't find that file")
                return

            try:
                filename = os.path.basename(file_path)
                response = self.get_experiment_upload_url(
                    experiment_id=self.experiment.id,
                    filename=filename,
                    model_id=self.experiment.model_id,
                )
            except Exception:
                self._logger.error("We couldn't fetch an upload URL from the server")
                return

            try:
                s3_target = S3SignedUrl(**response.data)
                upload_response = self.upload_file_to_s3(from_path=file_path, s3_signed_url=s3_target)
                upload_response.raise_for_status()
            except Exception:
                self._logger.error("We couldn't upload your file")

        file_absolute_path = str(Path(file_path).resolve())
        current_thread = self.experiments_pool.get(file_absolute_path)

        save_file_thread = threading.Thread(target=save, args=(file_absolute_path, current_thread))
        self.experiments_pool[file_absolute_path] = save_file_thread

        save_file_thread.start()
        return save_file_thread

    def get_model(
        self,
        name: "str",
        version: "Optional[str]" = None,
        download_path: "Optional[str]" = None,
        should_download: bool = True,
    ) -> "tuple[BaselineModelResponseMetadata, Optional[Path]]":
        """
        Get a model from the user's model repository in Lab tab, and optionally downloads the model file to the local machine
        :param name: Name of the model to retrieve from the lab
        :param version: Version of the model to retrieve from the lab (the version is specified near the model name)
        :param download_path: An optional download path to download the model to, if not supplied and should_download is set to True, will download to the current working directory
        :param should_download: A flag to indicate whether to download the model's file locally, defaults to False.
        :return: a tuple containing the model metadata and the download path (or None, if not downloaded) for the location of the model in the local machine
        """

        model_metadata = self.get_model_by_name(name=name, version=version).data
        if should_download:
            download_path = self.download_model(model_id=model_metadata.model_id, dest_path=download_path)
        return model_metadata, download_path

    def request_benchmark(
        self,
        model_path: "Union[Path, str]",
        hardware_type: "str",
        model_name: "Optional[str]" = None,
        batch_size: int = 1,
        quantization_level: str = QuantizationLevel.FP16,
        source_framework: "Literal['tf2', 'keras', 'onnx', 'pytorch']" = FrameworkType.ONNX,
        should_convert: bool = True,
    ) -> "UUID":
        """
        This method is used to request a benchmark of a model on a specified hardware with or without conversion.
        This should be used with the complimentary `get_benchmark_result` and `wait_for_benchmark_result` methods.
        :param model_path: The path of the model to be benchmarked
        :param hardware_type: Hardware type to benchmark the model on
        :param model_name: Optional name of the model to be benchmarked
        :param batch_size: Batch size to benchmark the model on
        :param quantization_level: Quantization level to benchmark the model on
        :param source_framework: The source framework of the model
        :param should_convert: Whether to convert the model to the target hardware before benchmarking
        :return: UUID representing the benchmark request
        :throws: BenchmarkRequestError if the benchmark request could not be created
        """
        model_name = model_name or Path(model_path).stem
        try:
            add_model_response = self.register_model(
                model=model_path,
                name=str(uuid4()),
                primary_batch_size=batch_size,
                architecture=model_name,
                description=f"Benchmark request on model: {model_path}",
                framework=source_framework,
                quantization_level=QuantizationLevel.FP32 if should_convert else quantization_level,
                hardware_types=[hardware_type],
            )
            if not add_model_response.success:
                raise AssertionError(f"Add model failed with message: {add_model_response.message}")
            if not should_convert:
                benchmark_request_form = BodySendModelBenchmarkRequest(
                    batch_sizes=[batch_size],
                    hardwares=[hardware_type],
                )
                self.send_model_benchmark_request(
                    model_id=add_model_response.data.model_id, body_send_model_benchmark_request=benchmark_request_form
                )
                return add_model_response.data.model_id
            optimization_form = OptimizationRequestForm(
                target_hardware=hardware_type,
                target_batch_size=batch_size,
                target_metric=Metric.LATENCY,
                optimize_model_size=False,
                quantization_level=quantization_level,
                optimize_autonac=False,
            )
            optimization_response = self.optimize_model(
                model_id=add_model_response.data.model_id, optimization_request_form=optimization_form
            )
            if not optimization_response.success:
                raise AssertionError(f"Optimize model request failed with message: {optimization_response.message}")
            return optimization_response.data.optimized_model_id
        except Exception as ex:
            msg = f"{ex}: Could not upload or benchmark model {model_name}!"
            self._logger.error(msg)
            raise BenchmarkRequestError(error_message=msg) from ex

    def get_benchmark_result(self, model_id: str) -> "ModelBenchmarkResultMetadata":
        """
        Get a benchmark result on the primary hardware of a model by a model ID or by job_id generated by the `request_benchmark` method.
        :param model_id: The ID of the model to retrieve its results or the job id generated by the `request_benchmark` method
        :return: ModelBenchmarkResultMetadata of the result, the error field will be set if there was an error while benchmarking the model
        :throws: BenchmarkResultNotFoundException if the benchmark result could not be found
        """
        try:
            response = self.get_model_by_id(model_id=model_id)
            if not response.success:
                raise AssertionError(f"Get model by ID failed with message: {response.message}")
            model_metadata = response.data
        except Exception:
            self._logger.error(f"Failed to get benchmark result for job {model_id}, model not found!")
            return ModelBenchmarkResultMetadata(error=f"Model with ID={model_id} not found!")
        if (
            model_metadata.baseline_model_id is not None
            and model_metadata.optimization_state == ModelOptimizationState.FAILED
        ):
            return ModelBenchmarkResultMetadata(error=f"Model conversion failed on job {model_id}")
        if model_metadata.benchmark_state == ModelBenchmarkState.FAILED:
            return ModelBenchmarkResultMetadata(error=f"Model benchmark failed on job {model_id}")

        if model_metadata.benchmark.get(model_metadata.primary_hardware.name) is None:
            raise BenchmarkResultNotFoundException(job_id=model_id)
        try:
            benchmark_results_for_hw = next(
                benchmark_result
                for benchmark_result in model_metadata.benchmark[model_metadata.primary_hardware.name]
                if benchmark_result.batch_size == model_metadata.primary_batch_size
                and benchmark_result.batch_inf_time is not None
            )
        except Exception as ex:
            raise BenchmarkResultNotFoundException(job_id=model_id) from ex

        return benchmark_results_for_hw

    def wait_for_benchmark_result(self, model_id: str, timeout: int = -1) -> "ModelBenchmarkResultMetadata":
        """
        Waits for a benchmark result on the primary hardware of a given model to be available, and returns the result upon completion.
        :param model_id: The ID of the model to retrieve its results or the job id generated by the `request_benchmark` method
        :param timeout: The maximum amount of time to wait, in seconds, for the benchmark result to be available, defaults to -1 (wait forever)
        :return: ModelBenchmarkResultMetadata of the result, the error field will be set if there was an error while benchmarking the model
        :throws: BenchmarkResultNotFoundException if timeout has passed
        """
        start = default_timer()
        while timeout <= 0 or default_timer() - start < timeout:
            try:
                return self.get_benchmark_result(model_id=model_id)
            except BenchmarkResultNotFoundException:
                time.sleep(1)
        raise BenchmarkResultNotFoundException(job_id=model_id)
