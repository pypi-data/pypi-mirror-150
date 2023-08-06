#!/usr/bin/env python
import time

import codefast as cf
import numpy as np
import pandas as pd
from sklearn.model_selection import GroupKFold, KFold
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Model
from apps.alert import Bark

import premium as pm
from tensorflow.keras.metrics import AUC
from contest.tabular.april.loader import load_data
from contest.tabular.april.model import ModelCreator
from premium.experimental.kaggle import KaggleData


class TabularDataPreprocessor(object):
    @classmethod
    def add_feature(cls, df: pd.DataFrame, features):
        for feature in features:
            df[feature + '_lag1'] = df.groupby('sequence')[feature].shift(1)
            df.fillna(0, inplace=True)
            df[feature + '_diff1'] = df[feature] - df[feature + '_lag1']
        return df

    @classmethod
    def add_feature_v2(cls, df):
        df['sensor_02_num'] = df['sensor_02'] > -15
        df['sensor_02_num'] = df['sensor_02_num'].astype(int)
        df['sensor_sum1'] = (df['sensor_00'] + df['sensor_09'] +
                             df['sensor_06'] + df['sensor_01'])
        df['sensor_sum2'] = (df['sensor_01'] + df['sensor_11'] +
                             df['sensor_09'] + df['sensor_06'] +
                             df['sensor_00'])
        df['sensor_sum3'] = (df['sensor_03'] + df['sensor_11'] +
                             df['sensor_07'])
        df['sensor_sum4'] = (df['sensor_04'] + df['sensor_10'])

        sensors = ['sensor_' + '%02d' % i for i in range(0, 13)]
        sensors.extend([
            'sensor_02_num', 'sensor_sum1', 'sensor_sum2', 'sensor_sum3',
            'sensor_sum4'
        ])

        for sensor in sensors:
            df[sensor + '_lag1'] = df.groupby('sequence')[sensor].shift(1)
            df.fillna(0, inplace=True)
            df[sensor + '_diff1'] = df[sensor] - df[sensor + '_lag1']

        return df


class Tabular(object):
    def __init__(self, model_config: pm.ModelConfig) -> None:
        self.__dict__.update(model_config.to_dict())

    def load_data(self):
        cf.info('loading April tabular data')
        kd = KaggleData(local_dir='/tmp/april',
                        remote_dir='kaggle/april',
                        loader_name='oss_loader')
        x, xt, sub = kd.standard_load()
        features = x.columns.tolist()[3:]
        x = TabularDataPreprocessor.add_feature_v2(x)
        xt = TabularDataPreprocessor.add_feature_v2(xt)
        y = kd.x.clone('train_labels.csv').read_csv().df['state']

        self.groups = x['sequence']
        features = x.columns.tolist()[3:]
        self.feature_length = len(features)
        cf.info('features\n', features)

        x, xt = x[features], xt[features]
        cf.info('standard scaling train and test data')
        sc = StandardScaler()
        x = sc.fit_transform(x)
        xt = sc.transform(xt)
        cf.info('standard scaling train and test data completed')

        x = x.reshape(-1, 60, self.feature_length)
        xt = xt.reshape(-1, 60, self.feature_length)
        cf.info('reshaped of x', x.shape)
        cf.info('reshaped of xt', xt.shape)
        cf.info('x[0] is')
        print(x[0])
        return x, y, xt, sub, features

    def build_model(self) -> 'Model':
        mc = ModelCreator([60, self.feature_length])
        self.model = mc.BiLSTM([60, self.feature_length])
        return self.model

    def train(self, x, y, test=None):
        kc = pm.KerasCallbacks(self.patience)
        kc.early_stopping.monitor = 'val_auc'
        kc.early_stopping.mode = 'max'
        kc.reduce_lr.monitor = 'val_auc'
        kc.reduce_lr.mode = 'max'
        predictions, scores = [], []
        kf = GroupKFold(n_splits=self.n_splits)

        cf.info('start training')
        for fold, (train_idx,
                   val_idx) in enumerate(kf.split(x, y, self.groups.unique())):
            cf.info('{} FOLD {} / {} started '.format('>' * 10, fold,
                                                      kf.n_splits))
            start_time = time.time()
            x_train, x_val = x[train_idx], x[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]
            cf.info('shape of x', x_train.shape)
            cf.info('shape of y', y_train.shape)
            model = self.build_model()
            model.compile(optimizer="adam",
                          loss="binary_crossentropy",
                          metrics='AUC')
            cf.info('model summary')
            print(model.summary())
            model.fit(x_train,
                      y_train,
                      validation_data=(x_val, y_val),
                      epochs=self.epochs,
                      batch_size=self.batch_size,
                      callbacks=kc.all())
            predictions.append(model.predict(test).squeeze())

            # scores.append(roc_auc_score(yv, y_pred))
            time_diff = time.time() - start_time
            cf.info('{} FOLD {} ended, time consumed {:<.2f} seconds'.format(
                '<' * 10, fold, time_diff))

        predictions = sum(predictions) / kf.n_splits
        return predictions, scores

    def predict(self, xt):
        cf.info('start predicting')
        yt = self.model.predict(xt)
        yt = np.average(yt, axis=1)
        return yt

    def pipeline(self):
        x, y, xt, sub, _ = self.load_data()
        # cf.info('label count', y.value_counts())
        cf.info('input shape for BiLSTM', x.shape[-2:])
        # self.build_model()
        yt, _ = self.train(x, y, xt)
        # yt = self.predict(xt)
        cf.info('length of yt is', len(yt))
        sub['state'] = yt
        sub.to_csv('/tmp/sub.csv', index=False)
        cf.info('submission file saved to /tmp/sub.csv')
        Bark.alert('AprilTabular', 'MODEL TRAINING COMPLETED!')
        return True


if __name__ == '__main__':
    test_preds = []
    mc = pm.ModelConfig()
    mc.update(
        dict(epochs=20,
             n_splits=5,
             batch_size=256,
             model_type='BiLSTM',
             patience=10))
    tab = Tabular(mc)
    tab.pipeline()
