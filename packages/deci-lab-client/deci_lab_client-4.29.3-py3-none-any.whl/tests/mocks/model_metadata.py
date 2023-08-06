import random

import factory
from deci_common.data_types.hardware import get_hardware_return_schema
from deci_lab_client import (
    APIResponseBaselineModelResponseMetadata,
    BaselineModelResponseMetadata,
    DeepLearningTaskLabel,
)
from deci_lab_client.models import (
    DeepLearningTask,
    FrameworkType,
    HardwareType,
    ModelMetadata,
)


class ModelMetadataFactory(factory.Factory):
    class Meta:
        model = ModelMetadata

    name = factory.Faker("name")
    framework = factory.LazyFunction(
        lambda: random.choice(list(filter(lambda v: v != "pytorch", FrameworkType.allowable_values)))
    )
    dl_task = factory.LazyFunction(lambda: random.choice(DeepLearningTask.allowable_values))
    primary_hardware = factory.LazyFunction(lambda: random.choice(HardwareType.allowable_values))
    input_dimensions = factory.LazyFunction(lambda: [[random.randint(1, 100) for _ in range(3)]])
    primary_batch_size = factory.Faker("pyint", min_value=1, max_value=64)


class BaselineModelResponseMetadataFactory(factory.Factory):
    class Meta:
        model = BaselineModelResponseMetadata

    name = factory.Faker("name")
    benchmark = dict()
    framework = factory.LazyFunction(
        lambda: random.choice(list(filter(lambda v: v != "pytorch", FrameworkType.allowable_values)))
    )
    dl_task = factory.LazyFunction(lambda: random.choice(DeepLearningTask.allowable_values))
    dl_task_label = factory.LazyFunction(lambda: random.choice(DeepLearningTaskLabel.allowable_values))
    primary_hardware = factory.LazyFunction(
        lambda: get_hardware_return_schema(random.choice(HardwareType.allowable_values))
    )
    input_dimensions = factory.Faker("name")
    primary_batch_size = factory.Faker("pyint", min_value=1, max_value=64)


class APIResponseBaselineModelResponseMetadataFactory(factory.Factory):
    class Meta:
        model = APIResponseBaselineModelResponseMetadata

    success = True
    data = factory.LazyFunction(BaselineModelResponseMetadataFactory.create)
    message = ""
