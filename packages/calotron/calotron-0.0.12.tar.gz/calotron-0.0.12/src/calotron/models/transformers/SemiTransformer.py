import tensorflow as tf

from calotron.models.transformers.Transformer import Transformer


class SemiTransformer(Transformer):
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
        seq_ord_normalizations=10000,
        residual_smoothing=True,
        output_activations=None,
        start_token_initializer="ones",
        name=None,
        dtype=None,
    ) -> None:
        super().__init__(
            output_depth,
            encoder_depth,
            decoder_depth,
            num_layers,
            num_heads,
            key_dims,
            mlp_units,
            dropout_rates,
            seq_ord_latent_dims,
            seq_ord_max_lengths,
            seq_ord_normalizations,
            residual_smoothing,
            output_activations,
            start_token_initializer,
            name,
            dtype,
        )
