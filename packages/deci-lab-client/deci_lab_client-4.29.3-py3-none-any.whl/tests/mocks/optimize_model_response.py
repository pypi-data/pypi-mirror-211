from uuid import uuid4

import factory
from deci_lab_client import APIResponseOptimizeModelResponse, OptimizeModelResponse


class OptimizeModelResponseFactory(factory.Factory):
    class Meta:
        model = OptimizeModelResponse

    optimized_model_id = factory.LazyFunction(lambda: str(uuid4()))
    optimization_request_id = factory.LazyFunction(lambda: str(uuid4()))


class APIResponseOptimizeModelResponseFactory(factory.Factory):
    class Meta:
        model = APIResponseOptimizeModelResponse

    success = True
    data = factory.LazyFunction(OptimizeModelResponseFactory.create)
    message = ""
