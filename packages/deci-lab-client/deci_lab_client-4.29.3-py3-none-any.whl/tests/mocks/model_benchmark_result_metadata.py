import random

import factory
from deci_lab_client import ModelBenchmarkResultMetadata


class ModelBenchmarkResultMetadataFactory(factory.Factory):
    class Meta:
        model = ModelBenchmarkResultMetadata

    batch_inf_time = factory.LazyFunction(lambda: 10 * random.random())
