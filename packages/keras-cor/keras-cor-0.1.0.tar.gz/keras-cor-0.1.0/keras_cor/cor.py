import tensorflow as tf


def pearson_cols(a, b, tol: float = 1e-8):
    """ compute pearson' rhos btw. columns of a and b
    Example:
    --------
        BATCH_SIZE, NUM_NEURONS = 128, 5
        a = tf.random.normal((BATCH_SIZE, NUM_NEURONS))
        b = tf.random.normal((BATCH_SIZE, NUM_NEURONS))
        rhos = pearson_cols(a, b)
        assert rhos.shape == NUM_NEURONS
    """
    mu_a = tf.reduce_mean(a, axis=0)
    mu_b = tf.reduce_mean(b, axis=0)
    centered_a = a - mu_a
    centered_b = b - mu_b
    nomin = tf.reduce_sum(tf.multiply(centered_a, centered_b), axis=0)
    denom1 = tf.math.sqrt(tf.reduce_sum(tf.math.pow(centered_a, 2), axis=0))
    denom2 = tf.math.sqrt(tf.reduce_sum(tf.math.pow(centered_b, 2), axis=0))
    rhos = nomin / (denom1 * denom2 + tol)
    return rhos


def pearson_vec(x):
    """ Compute pearson coefficient between all columns of x
    Examples:
    ---------
        BATCH_SIZE, NUM_NEURONS = 128, 3
        x = tf.random.normal((BATCH_SIZE, NUM_NEURONS))
        rhos = pearson_vec(x)
        assert rhos.shape == NUM_NEURONS
    """
    rhos = []
    n = x.shape[1]
    for i in range(0, n):
        for j in range(1 + i, n):
            rhos.append(pearson_cols(x[:, i], x[:, j]))
    return tf.stack(rhos, axis=0)


class CorrOutputsRegularizer(tf.keras.layers.Layer):
    """ Correlated Outputs Regularization
    Parameters:
    -----------
    target_corr : tf.constant
        Target correlations as vector

    cor_rate : float (Default: 1e-3)
        The factor how much COR regularization contributes to the loss function

    Example:
    --------
    The CorrOutputsRegularizer is applied after the layer that produces the
      outputs Z[batch, features] that are supposed to be generate a target
      correlation.
    Here is an example  using the Keras Functional API

        target_corr = pearson_vec(y_train)
        ...
        def build_mymodel(self, inputs, ...):
            ...
            h = tf.keras.layers.Dense(units=3)(h)
            h = tf.keras.layers.Activation("gelu")(h)
            h = CorrOutputsRegularizer(target_corrmat, cor_rate)(h)
            return h
    """
    def __init__(self, target_corr, cor_rate: float = 1e-3):
        super(CorrOutputsRegularizer, self).__init__()
        self.target_corr = target_corr
        self.cor_rate = cor_rate

    def call(self, h):
        d = self.target_corr - pearson_vec(h)
        d = tf.math.reduce_mean(tf.math.pow(d, 2))
        loss = self.cor_rate * d
        self.add_loss(loss)
        self.add_metric(loss, name="corr_outputs_regulizer")
        return h
