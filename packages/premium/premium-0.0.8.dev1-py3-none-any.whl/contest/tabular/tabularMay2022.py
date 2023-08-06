#!/usr/bin/env python
from typing import Dict, List, Optional, Set, Tuple

import codefast as cf
import numpy as np
import pandas as pd
import tensorflow as tf
from dofast import SyncFile
from sklearn.preprocessing import LabelBinarizer, LabelEncoder, StandardScaler
from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten,
                                     GlobalAveragePooling2D, MaxPooling2D,
                                     Concatenate)
from tensorflow.keras.models import Model, Sequential
from sklearn.model_selection import KFold, StratifiedKFold
import premium as pm
from premium import birdview, ml, pretools


def load_data():
    train = SyncFile('train.csv',
                     local_dir='/tmp/may',
                     remote_dir='kaggle/tabular/may',
                     loader_name='oss_loader')
    test = train.clone('test.csv')
    sub = train.clone('sample_submission.csv')
    x = train.read_csv().df
    cf.info('Train loaded, shape:', x.shape)
    xt = test.read_csv().df
    cf.info('Test loaded, shape:', xt.shape)
    sub = sub.read_csv().df
    cf.info('Sub loaded, shape:', sub.shape)
    return x, xt, sub


def preprocess(train, test, sub):
    for df in [train, test]:
        # Extract the 10 letters from f_27 into individual features
        for i in range(10):
            df[f'ch{i}'] = df.f_27.str.get(i).apply(ord) - ord('A')
        # unique_characters feature is from https://www.kaggle.com/code/cabaxiom/tps-may-22-eda-lgbm-model
        df["unique_characters"] = df.f_27.apply(lambda s: len(set(s)))
        cont = [f for f in df.columns if f.startswith('f_') and f != 'f_27']
        df['f_sum'] = df[cont].sum(axis=1)
        df['f_mean'] = df[cont].mean(axis=1)
        df['f_std'] = df[cont].std(axis=1)
        df['f_max'] = df[cont].max(axis=1)
        df['f_min'] = df[cont].min(axis=1)
        df['f_var'] = df[cont].var(axis=1)
        df['f_kurt'] = df[cont].kurt(axis=1)
        df['f_median'] = df[cont].median(axis=1)
        df['f_q1'] = df[cont].quantile(q=0.25, axis=1)
        df['f_q3'] = df[cont].quantile(q=0.75, axis=1)
        df['f_iqr'] = df['f_q3'] - df['f_q1']
        df['f_range'] = df['f_max'] - df['f_min']

    features = [f for f in test.columns if f != 'id' and f != 'f_27']
    cf.info('features are ', features)
    scaler = StandardScaler()
    labels = train['target']
    train = scaler.fit_transform(train[features])
    test = scaler.transform(test[features])
    return train, test, labels, features


class CNN(Model):
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        activation = 'swish'
        reg = tf.keras.regularizers.l2(30e-6)
        self._layers = [
            Dense(128, kernel_regularizer=reg, activation=activation),
            Dropout(0.2),
            Dense(64, kernel_regularizer=reg, activation=activation),
            Dropout(0.2),
            Dense(64, kernel_regularizer=reg, activation=activation),
            Dropout(0.2),
            Dense(32, kernel_regularizer=reg, activation=activation),
            Dense(16, kernel_regularizer=reg, activation=activation),
            Dense(1, activation='sigmoid'),
        ]

    def call(self, inputs):
        for layer in self._layers:
            inputs = layer(inputs)
        return inputs

    def train(self, X, y):
        self.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy'],
        )
        callbacks = pm.KerasCallbacks().all
        self.fit(X, y, epochs=self.cfg.epochs, callbacks=callbacks)

    def kfold_fit_predict(self, X, y, Xt, sub):
        callbacks = pm.KerasCallbacks().all

        kf = StratifiedKFold(n_splits=self.cfg.n_splits,
                             shuffle=True,
                             random_state=42)
        ypreds = []
        for i, (train_index, test_index) in enumerate(kf.split(X, y)):
            self.__init__(self.cfg)
            self.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'],
            )
            cf.info(f'Fold {i}')
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            self.fit(X_train,
                     y_train,
                     epochs=self.cfg.epochs,
                     callbacks=callbacks,
                     validation_data=(X_test, y_test))
            ypreds.append(self.predict(Xt, batch_size=32))
        ypreds = np.mean(ypreds, axis=0)
        ypreds = ypreds.flatten()
        sub['target'] = ypreds
        sub.to_csv('submission.csv', index=False)
        return ypreds

    def make_predict(self, Xt, sub):
        ypreds = self.predict(Xt, batch_size=32)
        ypreds = ypreds.flatten()
        cf.info('Predictions:', ypreds)
        sub['target'] = ypreds
        sub.to_csv('preds.csv', index=False)
        return ypreds


if __name__ == '__main__':
    X, Xt, sub = load_data()
    X, Xt, y, features = preprocess(X, Xt, sub)
    cfg = type(
        'ModelConfig', (object, ), {
            'epochs': 100,
            'n_splits': 7,
            'batch_size': 32,
            'model_path': '/tmp/model.h5',
            'features': features,
        })
    cnn = CNN(cfg)
    cnn.kfold_fit_predict(X, y, Xt, sub)
    # cnn.train(X, y)
    # cnn.make_predict(Xt, sub)
