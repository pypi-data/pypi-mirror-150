#!/usr/bin/env python
from pyexpat import model
import codefast as cf
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
                                        ReduceLROnPlateau)
from tensorflow.keras.layers import (LSTM, Bidirectional, Concatenate, GRU,
                                     GlobalMaxPooling1D, Dense, Bidirectional,
                                     Dropout, Embedding, Input)
from tensorflow.keras.metrics import AUC
from tensorflow.keras.models import Model

import premium as pm
from premium.experimental.kaggle import KaggleData
from premium.models.clf import Classifier


class SimpleLSTMModel(keras.Model):
    def __init__(self, input_shape: int):
        super(SimpleLSTMModel, self).__init__()
        self._input_shape = input_shape
        self.lstm = keras.layers.LSTM(128, return_sequences=True)
        self.dense = keras.layers.Dense(1, activation='sigmoid')

    def call(self, inputs):
        x = self.lstm(inputs)
        x = self.dense(x)
        return x


class ModelCreator(object):
    def __init__(self, input_shape) -> None:
        self._input_shape = input_shape

    def lstm(self):
        return keras.models.Sequential([
            keras.layers.LSTM(256,
                              return_sequences=True,
                              input_shape=self._input_shape),
            keras.layers.LSTM(256, return_sequences=True),
            keras.layers.Dropout(0.4),
            keras.layers.LSTM(256, return_sequences=True),
            keras.layers.Dropout(0.4),
            keras.layers.LSTM(256, return_sequences=True),
            keras.layers.LSTM(128, return_sequences=True),
            GlobalMaxPooling1D(),
            Dense(128, activation='selu'),
            Dense(1, activation='sigmoid')
        ])

    def demo(self, shape):
        x_input = Input(shape=shape)

        x1 = Bidirectional(LSTM(units=512, return_sequences=True))(x_input)
        x2 = Bidirectional(LSTM(units=256, return_sequences=True))(x1)
        z1 = Bidirectional(GRU(units=256, return_sequences=True))(x1)
        c = Concatenate(axis=2)([x2, z1])
        x3 = Bidirectional(LSTM(units=128, return_sequences=True))(c)
        x4 = GlobalMaxPooling1D()(x3)
        x5 = Dense(units=128, activation='selu')(x4)
        x_output = Dense(1, activation='sigmoid')(x5)
        model = Model(inputs=x_input, outputs=x_output, name='lstm_model')
        return model

    def gru(self):
        return keras.models.Sequential([
            keras.layers.GRU(100,
                             return_sequences=True,
                             input_shape=self._input_shape),
            keras.layers.GRU(100, return_sequences=True),
            keras.layers.GRU(50, return_sequences=True),
            keras.layers.TimeDistributed(keras.layers.Dense(1))
        ])

    def BiLSTM(self, input_shape):
        input_layer = Input(input_shape)
        x1 = Bidirectional(LSTM(768, return_sequences=True))(input_layer)

        x21 = Bidirectional(LSTM(512, return_sequences=True))(x1)
        x22 = Bidirectional(LSTM(512, return_sequences=True))(input_layer)
        l2 = Concatenate(axis=2)([x21, x22])

        x31 = Bidirectional(LSTM(384, return_sequences=True))(l2)
        x32 = Bidirectional(LSTM(384, return_sequences=True))(x21)
        l3 = Concatenate(axis=2)([x31, x32])

        x41 = Bidirectional(LSTM(256, return_sequences=True))(l3)
        x42 = Bidirectional(LSTM(128, return_sequences=True))(x32)
        l4 = Concatenate(axis=2)([x41, x42])

        l5 = Concatenate(axis=2)([x1, l2, l3, l4])
        l5 = GlobalMaxPooling1D()(l5)
        x7 = Dense(128, activation='selu')(l5)
        x8 = Dropout(0.3)(x7)
        # output_layer = keras.layers.TimeDistributed(keras.layers.Dense(1))(x8)
        output_layer = Dense(units=1, activation="sigmoid")(x8)
        model = Model(inputs=input_layer,
                      outputs=output_layer,
                      name='BiLSTM_Model')
        cf.info('model summary')
        print(model.summary())

        return model
