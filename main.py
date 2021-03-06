import pandas as pd
import tensorflow as tf


def prep_v2(frame):
    # rescale training hours
    trh = 'training_hours'
    frame[trh] = frame[trh] / frame[trh].max()
    # one-hot encode categorical data
    frame = pd.get_dummies(frame)
    # split dataframe up into training and testing sets
    # then pop target sets for both
    print(tf.shape(frame))
    train_size = int(0.85 * len(frame))
    train_x = frame.iloc[:train_size, :]
    train_y = pd.get_dummies(train_x.pop('target'))
    test_x = frame.iloc[train_size+1:, :]
    test_y = pd.get_dummies(test_x.pop('target'))

    return (train_x, train_y), (test_x, test_y)


def get_compiled_model():
    # define neural-network core logic
    # sequential, feed-forward network with 2 hidden layers and 1 output layer
    mod = tf.keras.Sequential([
        tf.keras.layers.Dense(20, activation='relu', kernel_initializer='he_normal'),
        tf.keras.layers.Dense(10, activation='relu', kernel_initializer='he_normal'),
        tf.keras.layers.Dense(2, activation='softmax')
    ])
    # compile with loss function that is most applicable given the data sets and output layer
    mod.compile(optimizer='adam',
                loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
                metrics=['accuracy'])
    return mod


# get prepped datasets from CSV file
(train, train_target), (test, test_target) = prep_v2(pd.read_csv('aug_train.csv'))
# compile, train, and evaluate model
model = get_compiled_model()
model.fit(train, train_target, epochs=30, validation_split=.176, batch_size=256)
model.evaluate(test, test_target)
model.summary()
