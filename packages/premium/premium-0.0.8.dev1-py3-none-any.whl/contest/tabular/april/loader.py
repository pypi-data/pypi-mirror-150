#!/usr/bin/env python
import codefast as cf
import numpy as np
from sklearn.preprocessing import StandardScaler
import premium as pm
from premium.experimental.kaggle import KaggleData


def add_feature(df, features):
    for f in features:
        df[f + '_lag1'] = df.groupby('sequence')[f].shift(1)
        df.fillna(0, inplace=True)
        df[f + '_diff1'] = df[f] - df[f + '_lag1']
    return df


def load_data():
    cf.info('loading April tabular data')
    kd = KaggleData('/tmp/april', 'kaggle/april')
    x, xt, sub = kd.standard_load()
    y = kd.x.clone('train_labels.csv').read_csv().df
    features = [
        col for col in xt.columns if col not in ('sequence', 'step', 'subject')
    ]
    # x = pd.merge(x, y, on='sequence', how='left')
    # x = add_feature(x, features)
    # print(x.head())
    print(features)
    x = np.array(x[features])

    sc = StandardScaler()
    x = sc.fit_transform(x)

    cf.info('shape of x', x.shape)
    x = np.reshape(x, (-1, 60, 13))
    cf.info('reshaped of x', x.shape)
    cf.info('x[0] is')
    print(x[0])
    return x, y, xt, sub, features
