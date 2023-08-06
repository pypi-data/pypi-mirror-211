import numpy as np
import tensorflow as tf


class SeqOrderEmbedding(tf.keras.layers.Layer):
    def __init__(
        self,
        latent_dim=16,
        max_length=512,
        normalization=10_000,
        dropout_rate=0.1,
        epsilon=1e-12,
        name=None,
        dtype=None,
    ) -> None:
        super().__init__(name=name, dtype=dtype)
        if name is not None:
            prefix = name.split("_")[0]

        # Sequence order latent space dimension
        assert isinstance(latent_dim, (int, float))
        assert latent_dim >= 1
        self._latent_dim = int(latent_dim)

        # Sequence max length
        assert isinstance(max_length, (int, float))
        assert max_length >= 1
        self._max_length = int(max_length)

        # Sequence order encoding normalization
        assert isinstance(normalization, (int, float))
        assert normalization > 0.0
        self._normalization = float(normalization)

        # Dropout rate
        assert isinstance(dropout_rate, (int, float))
        assert dropout_rate >= 0.0 and dropout_rate < 1.0
        self._dropout_rate = float(dropout_rate)

        # Epsilon
        assert isinstance(epsilon, (int, float))
        assert epsilon > 0.0
        self._epsilon = float(epsilon)

        # Sequence order encoding
        self._seq_ord_encoding = self._seq_order_encoding(
            length=self._max_length,
            depth=self._latent_dim,
            normalization=self._normalization,
            dtype=self.dtype,
        )

        # Embedding layer
        self._embedding = tf.keras.Sequential(
            [
                tf.keras.layers.Dense(
                    units=self._latent_dim,
                    activation="linear",
                    kernel_initializer="he_normal",
                    bias_initializer="zeros",
                    name=f"{prefix}_seq_ord_dense" if name else None,
                    dtype=self.dtype,
                ),
                tf.keras.layers.Dropout(
                    rate=self._dropout_rate,
                    name=f"{prefix}_dropout" if name else None,
                    dtype=self.dtype,
                ),
            ]
        )

        # Add layer
        self._add = tf.keras.layers.Add()

    def call(self, x) -> tf.Tensor:
        seq_order = tf.tile(
            self._seq_ord_encoding[None, : tf.shape(x)[1], :],
            multiples=(tf.shape(x)[0], 1, 1),
        )
        emb_output = self._embedding(x) + self._epsilon
        output = self._add([emb_output, seq_order])
        return output

    @staticmethod
    def _seq_order_encoding(
        length, depth, normalization=10_000, dtype=tf.float32
    ) -> tf.Tensor:
        pos_encoding = np.zeros(shape=(length, depth))  # buffer to fill
        for k in range(length):
            for i in range(int(depth / 2)):
                denominator = np.power(normalization, 2 * i / depth)
                pos_encoding[k, 2 * i] = np.sin(k / denominator)
                pos_encoding[k, 2 * i + 1] = np.cos(k / denominator)
        return tf.cast(pos_encoding, dtype=dtype)

    @property
    def latent_dim(self) -> int:
        return self._latent_dim

    @property
    def max_length(self) -> int:
        return self._max_length

    @property
    def normalization(self) -> float:
        return self._normalization

    @property
    def dropout_rate(self) -> float:
        return self._dropout_rate

    @property
    def epsilon(self) -> float:
        return self._epsilon
