import numpy as np
import tensorflow as tf

from calotron.layers import Decoder, Encoder, MultiActivations
from calotron.models.transformers.BaseTransformer import BaseTransformer

START_TOKEN_INITIALIZERS = ["zeros", "ones", "means"]


class Transformer(BaseTransformer):
    def __init__(
        self,
        output_depth,
        encoder_depth,
        decoder_depth,
        num_layers,
        num_heads,
        key_dims,
        mlp_units=128,
        dropout_rates=0.1,
        seq_ord_latent_dims=16,
        seq_ord_max_lengths=512,
        seq_ord_normalizations=10_000,
        enable_residual_smoothing=True,
        enable_source_baseline=True,
        output_activations=None,
        start_token_initializer="ones",
        name=None,
        dtype=None,
    ) -> None:
        super().__init__(name=name, dtype=dtype)

        # Output depth
        assert output_depth >= 1
        self._output_depth = int(output_depth)

        # Encoder depth
        assert encoder_depth >= 1
        self._encoder_depth = int(encoder_depth)

        # Decoder depth
        assert decoder_depth >= 1
        self._decoder_depth = int(decoder_depth)

        # Number of layers (encoder/decoder)
        if isinstance(num_layers, (int, float)):
            assert num_layers >= 1
            self._num_layers = [int(num_layers)] * 2
        else:
            assert isinstance(num_layers, (list, tuple, np.ndarray))
            assert len(num_layers) == 2
            self._num_layers = list()
            for num in num_layers:
                assert isinstance(num, (int, float))
                assert num >= 1
                self._num_layers.append(int(num))

        # Number of heads (encoder/decoder)
        if isinstance(num_heads, (int, float)):
            assert num_heads >= 1
            self._num_heads = [int(num_heads)] * 2
        else:
            assert isinstance(num_heads, (list, tuple, np.ndarray))
            assert len(num_heads) == 2
            self._num_heads = list()
            for num in num_heads:
                assert isinstance(num, (int, float))
                assert num >= 1
                self._num_heads.append(int(num))

        # Key dimension (encoder/decoder)
        if isinstance(key_dims, (int, float)):
            assert key_dims >= 1
            self._key_dims = [int(key_dims)] * 2
        else:
            assert isinstance(key_dims, (list, tuple, np.ndarray))
            assert len(key_dims) == 2
            self._key_dims = list()
            for dim in key_dims:
                assert isinstance(dim, (int, float))
                assert dim >= 1
                self._key_dims.append(int(dim))

        # Feed-forward net units (encoder/decoder)
        if isinstance(mlp_units, (int, float)):
            assert mlp_units >= 1
            self._mlp_units = [int(mlp_units)] * 2
        else:
            assert isinstance(mlp_units, (list, tuple, np.ndarray))
            assert len(mlp_units) == 2
            self._mlp_units = list()
            for units in mlp_units:
                assert isinstance(units, (int, float))
                assert units >= 1
                self._mlp_units.append(int(units))

        # Dropout rate (encoder/decoder)
        if isinstance(dropout_rates, (int, float)):
            assert dropout_rates >= 0.0 and dropout_rates < 1.0
            self._dropout_rates = [float(dropout_rates)] * 2
        else:
            assert isinstance(dropout_rates, (list, tuple, np.ndarray))
            assert len(dropout_rates) == 2
            self._dropout_rates = list()
            for rate in dropout_rates:
                assert isinstance(rate, (int, float))
                assert rate >= 0.0 and rate < 1.0
                self._dropout_rates.append(float(rate))

        # Sequence order latent space dimension (encoder/decoder)
        if isinstance(seq_ord_latent_dims, (int, float)):
            assert seq_ord_latent_dims >= 1
            self._seq_ord_latent_dims = [int(seq_ord_latent_dims)] * 2
        else:
            assert isinstance(seq_ord_latent_dims, (list, tuple, np.ndarray))
            assert len(seq_ord_latent_dims) == 2
            self._seq_ord_latent_dims = list()
            for dim in seq_ord_latent_dims:
                assert isinstance(dim, (int, float))
                assert dim >= 1
                self._seq_ord_latent_dims.append(int(dim))

        # Sequence max length (encoder/decoder)
        if isinstance(seq_ord_max_lengths, (int, float)):
            assert seq_ord_max_lengths >= 1
            self._seq_ord_max_lengths = [int(seq_ord_max_lengths)] * 2
        else:
            assert isinstance(seq_ord_max_lengths, (list, tuple, np.ndarray))
            assert len(seq_ord_max_lengths) == 2
            self._seq_ord_max_lengths = list()
            for length in seq_ord_max_lengths:
                assert isinstance(length, (int, float))
                assert length >= 1
                self._seq_ord_max_lengths.append(int(length))

        # Sequence order encoding normalization (encoder/decoder)
        if isinstance(seq_ord_normalizations, (int, float)):
            assert seq_ord_normalizations > 0.0
            self._seq_ord_normalizations = [float(seq_ord_normalizations)] * 2
        else:
            assert isinstance(seq_ord_normalizations, (list, tuple, np.ndarray))
            assert len(seq_ord_normalizations) == 2
            self._seq_ord_normalizations = list()
            for norm in seq_ord_normalizations:
                assert isinstance(norm, (int, float))
                assert norm > 0.0
                self._seq_ord_normalizations.append(float(norm))

        # Residual smoothing (encoder/decoder)
        if isinstance(enable_residual_smoothing, bool):
            assert isinstance(enable_residual_smoothing, bool)
            self._enable_residual_smoothing = [enable_residual_smoothing] * 2
        else:
            assert isinstance(enable_residual_smoothing, (list, tuple, np.ndarray))
            assert len(enable_residual_smoothing) == 2
            self._enable_residual_smoothing = list()
            for flag in enable_residual_smoothing:
                assert isinstance(flag, bool)
                self._enable_residual_smoothing.append(flag)

        # Source baseline
        assert isinstance(enable_source_baseline, bool)
        self._enable_source_baseline = enable_source_baseline

        # Output activations
        self._output_activations = output_activations

        # Start token initializer
        assert isinstance(start_token_initializer, str)
        if start_token_initializer not in START_TOKEN_INITIALIZERS:
            raise ValueError(
                "`start_token_initializer` should be selected "
                f"in {START_TOKEN_INITIALIZERS}, instead "
                f"'{start_token_initializer}' passed"
            )
        self._start_token_initializer = start_token_initializer

        # Encoder
        self._encoder = Encoder(
            output_depth=self._encoder_depth,
            num_layers=self._num_layers[0],
            num_heads=self._num_heads[0],
            key_dim=self._key_dims[0],
            mlp_units=self._mlp_units[0],
            dropout_rate=self._dropout_rates[0],
            seq_ord_latent_dim=self._seq_ord_latent_dims[0],
            seq_ord_max_length=self._seq_ord_max_lengths[0],
            seq_ord_normalization=self._seq_ord_normalizations[0],
            enable_residual_smoothing=self._enable_residual_smoothing[0],
            name="t_encoder",
            dtype=self.dtype,
        )

        # Decoder
        self._decoder = Decoder(
            output_depth=self._decoder_depth,
            num_layers=self._num_layers[1],
            num_heads=self._num_heads[1],
            key_dim=self._key_dims[1],
            mlp_units=self._mlp_units[1],
            dropout_rate=self._dropout_rates[1],
            seq_ord_latent_dim=self._seq_ord_latent_dims[1],
            seq_ord_max_length=self._seq_ord_max_lengths[1],
            seq_ord_normalization=self._seq_ord_normalizations[1],
            enable_residual_smoothing=self._enable_residual_smoothing[1],
            name="t_decoder",
            dtype=self.dtype,
        )

        # Output layers
        self._output_layer = tf.keras.layers.Dense(
            units=self._output_depth,
            activation="linear",
            kernel_initializer="truncated_normal",
            bias_initializer="zeros",
            name="t_dense_out",
            dtype=self.dtype,
        )
        if output_activations is not None:
            self._multi_activations = MultiActivations(
                activations=output_activations,
                output_depth=self._output_depth,
                name="t_filter",
                dtype=self.dtype,
            )
        else:
            self._multi_activations = None

    def call(self, inputs) -> tf.Tensor:
        source, target = inputs
        target = self._prepare_input_target(target)
        condition = self._encoder(source)
        output = self._decoder(target, condition)
        output = self._output_layer(output)
        if self._multi_activations is not None:
            output = self._multi_activations(output)
        baseline = self._prepare_output_baseline(source, target)
        return baseline + output

    def _prepare_input_target(self, target) -> tf.Tensor:
        if self._start_token_initializer == "zeros":
            start_token = tf.zeros((tf.shape(target)[0], 1, tf.shape(target)[2]))
        elif self._start_token_initializer == "ones":
            zeros = tf.zeros((tf.shape(target)[0], 1, 2))
            ones = tf.ones((tf.shape(target)[0], 1, tf.shape(target)[2] - 2))
            start_token = tf.concat([zeros, ones], axis=-1)
        elif self._start_token_initializer == "means":
            start_token = tf.reduce_mean(target, axis=(0, 1))[None, None, :]
            start_token = tf.tile(start_token, (tf.shape(target)[0], 1, 1))
        return tf.concat([start_token, target[:, :-1, :]], axis=1)

    def _prepare_output_baseline(self, source, target) -> tf.Tensor:
        source_max_length, target_max_length = self._seq_ord_max_lengths
        if self._enable_source_baseline:
            if source_max_length < target_max_length:
                baseline = tf.concat(
                    [
                        source[:, :, :3],
                        tf.zeros(
                            shape=(
                                tf.shape(source)[0],
                                target_max_length - source_max_length,
                                3,
                            )
                        ),
                    ],
                    axis=1,
                )
            elif source_max_length == target_max_length:
                baseline = source[:, :, :3]
            else:
                baseline = source[:, :target_max_length, :3]
            if self._output_depth > 3:
                baseline = tf.concat(
                    [
                        baseline,
                        tf.zeros(
                            shape=(
                                tf.shape(source)[0],
                                target_max_length,
                                self._output_depth - 3,
                            )
                        ),
                    ],
                    axis=-1,
                )
        else:
            baseline = tf.zeros(
                shape=(tf.shape(source)[0], target_max_length, self._output_depth)
            )
        return baseline[:, : tf.shape(target)[1], :]

    def get_start_token(self, target) -> tf.Tensor:
        if self._start_token_initializer == "zeros":
            start_token = tf.zeros((tf.shape(target)[0], tf.shape(target)[2]))
        elif self._start_token_initializer == "ones":
            zeros = tf.zeros((tf.shape(target)[0], 2))
            ones = tf.ones((tf.shape(target)[0], tf.shape(target)[2] - 2))
            start_token = tf.concat([zeros, ones], axis=-1)
        elif self._start_token_initializer == "means":
            start_token = tf.reduce_mean(target, axis=(0, 1))[None, :]
            start_token = tf.tile(start_token, (tf.shape(target)[0], 1))
        return start_token

    @property
    def output_depth(self) -> int:
        return self._output_depth

    @property
    def encoder_depth(self) -> int:
        return self._encoder_depth

    @property
    def decoder_depth(self) -> int:
        return self._decoder_depth

    @property
    def num_layers(self) -> list:
        return self._num_layers

    @property
    def num_heads(self) -> list:
        return self._num_heads

    @property
    def key_dims(self) -> list:
        return self._key_dims

    @property
    def mlp_units(self) -> list:
        return self._mlp_units

    @property
    def dropout_rates(self) -> list:
        return self._dropout_rates

    @property
    def seq_ord_latent_dims(self) -> list:
        return self._seq_ord_latent_dims

    @property
    def seq_ord_max_lengths(self) -> list:
        return self._seq_ord_max_lengths

    @property
    def seq_ord_normalizations(self) -> list:
        return self._seq_ord_normalizations

    @property
    def enable_residual_smoothing(self) -> list:
        return self._enable_residual_smoothing

    @property
    def enable_source_baseline(self) -> bool:
        return self._enable_source_baseline

    @property
    def output_activations(self):  # TODO: add Union[list, None]
        return self._output_activations

    @property
    def start_token_initializer(self) -> str:
        return self._start_token_initializer

    @property
    def attention_weights(self) -> tf.Tensor:
        return self._decoder._last_attn_scores
