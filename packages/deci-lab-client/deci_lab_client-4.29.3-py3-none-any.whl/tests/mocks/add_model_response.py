from uuid import uuid4

import factory
from deci_lab_client import AddModelResponse, APIResponseAddModelResponse


class AddModelResponseFactory(factory.Factory):
    class Meta:
        model = AddModelResponse

    model_id = factory.LazyFunction(lambda: str(uuid4()))
    benchmark_request_id = factory.LazyFunction(lambda: str(uuid4()))


class APIResponseAddModelResponseFactory(factory.Factory):
    class Meta:
        model = APIResponseAddModelResponse

    success = True
    data = factory.LazyFunction(AddModelResponseFactory.create)
    message = ""
