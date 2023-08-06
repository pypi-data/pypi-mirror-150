from keras_cor import CorrOutputsRegularizer, pearson_vec
import tensorflow as tf


# Simple regression NN
def build_mymodel(input_dim, target_corr, cor_rate=0.1,
                  activation="sigmoid", output_dim=3):
    inputs = tf.keras.Input(shape=(input_dim,))
    h = tf.keras.layers.Dense(units=output_dim)(inputs)
    h = tf.keras.layers.Activation(activation)(h)
    outputs = CorrOutputsRegularizer(target_corr, cor_rate)(h)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model


def test1():
    BATCH_SZ = 128
    INPUT_DIM = 64
    OUTPUT_DIM = 3

    X_train = tf.random.normal([BATCH_SZ, INPUT_DIM])
    y_train = tf.random.normal([BATCH_SZ, OUTPUT_DIM])
    target_corr = tf.constant([.5, -.4, .9])

    model = build_mymodel(
        input_dim=INPUT_DIM,
        target_corr=target_corr,
        output_dim=OUTPUT_DIM)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss="mean_squared_error")

    history = model.fit(X_train, y_train, verbose=1, epochs=2)
    assert "corr_outputs_regulizer" in history.history.keys()

    yhat = model.predict(X_train)
    rhos = pearson_vec(yhat)
    assert rhos.shape == target_corr.shape


def test2():
    BATCH_SIZE, NUM_NEURONS = 128, 4
    x = tf.random.normal((BATCH_SIZE, NUM_NEURONS))
    rhos = pearson_vec(x)
    assert rhos.shape[0] == (NUM_NEURONS * (NUM_NEURONS - 1)) // 2
