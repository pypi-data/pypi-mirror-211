import tensorflow as tf
from tensorflow.keras.callbacks import Callback


class AttnMaskIgnition(Callback):
    def __init__(self, attn_mask, ignition_step, verbose=False, prefix=None) -> None:
        super().__init__()

        # Attention mask
        assert isinstance(attn_mask, tf.Variable)
        self._attn_mask = attn_mask

        # Ignition step
        assert isinstance(ignition_step, (int, float))
        assert ignition_step > 0
        self._ignition_step = int(ignition_step)

        # Verbose
        assert isinstance(verbose, bool)
        self._verbose = verbose

        # Key prefix
        if prefix is not None:
            assert isinstance(prefix, str)
            self._prefix = prefix
        else:
            self._prefix = None

    def on_train_begin(self, logs=None) -> None:
        self._dtype = self._attn_mask.dtype
        self._step = -1
        self._ignition = 0.0

    def on_batch_begin(self, batch, logs=None) -> None:
        self._step += 1
        if self._step == self._ignition_step:
            self._attn_mask.assign(tf.ones_like(self._attn_mask))
        self._ignition = tf.math.count_nonzero(
            self._attn_mask, dtype=self._dtype
        ) / tf.cast(tf.size(self._attn_mask), dtype=self._dtype)

    def on_batch_end(self, batch, logs=None) -> None:
        logs = logs or {}
        if self._verbose:
            key = f"{self._prefix}_ignition" if self._prefix else "ignition"
            logs[key] = self._ignition

    def on_epoch_end(self, epoch, logs=None) -> None:
        logs = logs or {}
        if self._verbose:
            key = f"{self._prefix}_ignition" if self._prefix else "ignition"
            logs[key] = self._ignition

    @property
    def attn_mask(self) -> tf.Variable:
        return self._attn_mask

    @property
    def ignition_step(self) -> int:
        return self._ignition_step
