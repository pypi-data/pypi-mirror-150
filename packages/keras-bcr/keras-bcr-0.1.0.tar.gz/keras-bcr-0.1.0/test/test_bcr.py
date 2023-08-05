from keras_bcr import BatchCorrRegulizer
import tensorflow as tf


# The BCR layer is added before the addition of the skip-connection
def build_resnet_block(inputs, units=64, activation="gelu",
                       dropout=0.4, bcr_rate=0.1):
    h = tf.keras.layers.Dense(units=units)(inputs)
    h = h = tf.keras.layers.Activation(activation=activation)(h)
    h = tf.keras.layers.Dropout(rate=dropout)(h)
    h = BatchCorrRegulizer(bcr_rate=bcr_rate)([h, inputs])  # << HERE
    outputs = tf.keras.layers.Add()([h, inputs])
    return outputs


# An model with 3 ResNet blocks
def build_model(input_dim):
    inputs = tf.keras.Input(shape=(input_dim,))
    h = build_resnet_block(inputs, units=input_dim)
    h = build_resnet_block(h, units=input_dim)
    outputs = build_resnet_block(h, units=input_dim)
    model = tf.keras.Model(inputs=inputs, outputs=outputs)
    return model


def test1():
    INPUT_DIM = 64
    model = build_model(input_dim=INPUT_DIM)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss="mean_squared_error")

    BATCH_SZ = 128
    X_train = tf.random.normal([BATCH_SZ, INPUT_DIM])
    y_train = tf.random.normal([BATCH_SZ])

    history = model.fit(X_train, y_train, verbose=1, epochs=2)
    assert "batch_corr_regulizer" in history.history.keys()
