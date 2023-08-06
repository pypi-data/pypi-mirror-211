import tensorflow as tf

from calotron.models.discriminators.BaseDiscriminator import BaseDiscriminator


class GNNDiscriminator(BaseDiscriminator):
    def __init__(self, name=None, dtype=None) -> None:
        super().__init__(name=name, dtype=dtype)
