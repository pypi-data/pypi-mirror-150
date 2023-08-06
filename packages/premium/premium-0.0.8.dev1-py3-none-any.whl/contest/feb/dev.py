from re import A
import torch.nn as nn
from scipy.stats import mode
import time
import random
from typing import Any, Callable, NamedTuple

import codefast as cf
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
import premium as pm
import matplotlib.pyplot as plt

from data import DataLoader


class _DataLoader(object):
    def __init__(self, train_frac: float = 0.1):
        self.dl = DataLoader('tabular_2022_feb')
        self.train_frac = train_frac
        self.label_encoder = LabelEncoder()

    def run(self, *args: Any, **kwds: Any) -> Any:
        train, test, sub = self.dl.load()
        features = [col for col in test.columns if 'row_id' not in col]
        train = train.drop_duplicates(subset=features).sample(
            frac=self.train_frac)
        labels = self.label_encoder.fit_transform(train['target'])
        train, test = train[features], test[features]
        print(train.head(), train.shape)
        return train, labels, test, sub


class _StratifiedKFold(object):
    def __init__(self,
                 model: Any,
                 corpus: pm.Corpus,
                 metric: Callable,
                 n_splits: int = 5,
                 shuffle: bool = True,
                 random_state: int = 63):
        self.model = model
        self.corpus = corpus
        self.metric = metric
        self.n_splits = n_splits
        self.skf = StratifiedKFold(n_splits=n_splits,
                                   shuffle=shuffle,
                                   random_state=random_state)

    def run(self):
        scores = []
        y_preds = []
        y_probs = []
        corpus = self.corpus
        for fold, (train_idx,
                   test_idx) in enumerate(self.skf.split(corpus.x, corpus.y)):
            X_train, X_valid = corpus.x.iloc[train_idx], corpus.x.iloc[
                test_idx]
            y_train, y_valid = corpus.y[train_idx], corpus.y[test_idx]
            time_start = time.time()
            self.model.fit(X_train, y_train)
            time_diff: str = cf.io.readable_duration(time.time() - time_start)
            valid_pred = self.model.predict(X_valid)
            score = self.metric(y_valid, valid_pred)
            scores.append(score)
            y_preds.append(self.model.predict(corpus.t))
            y_probs.append(self.model.predict_proba(corpus.t))

            cf.info(
                f'Fold {fold+1:3}, {self.metric.__name__} = {score:.4f}, time = {time_diff}'
            )
        cf.info(f'average score = {np.mean(scores):.4f}')
        self.y_preds = y_preds
        self.y_probs = y_probs
        return self


import premium as pm


def ensemble():
    dl = _DataLoader(train_frac=1)
    train_x, train_y, test, sub = dl.run()
    corpus = pm.Corpus(x=train_x, y=train_y, t=test, s=sub)
    etc = ExtraTreesClassifier(n_estimators=1250,
                               n_jobs=-1,
                               min_samples_split=2,
                               verbose=1,
                               random_state=random.randint(1, 2022))
    lgb = pm.demo.classifiers.lightgbm_classifier(objective='multiclass',
                                                  metric='multi_logloss')
    xgb = pm.demo.classifiers.xgboost_classifier(objective='multi:softmax')
    cat = pm.demo.classifiers.catboost_classifier(loss_function='MultiClass')
    y_preds = []
    for i, clf in enumerate([etc, lgb, xgb, cat]):
        preds = pm.Classifier(clf).fit(corpus.x, corpus.y).predict(corpus.t)
        c_pred = np.array(preds).flatten()
        y_preds.append(c_pred)
        c_pred = dl.label_encoder.inverse_transform(c_pred)
        sub['target'] = c_pred
        sub.to_csv('{}.csv'.format(clf.__class__.__name__.lower()),
                   index=False)
    y_preds = pm.array.mode(y_preds, compress='col').flatten()
    print(y_preds.shape)
    y_preds = dl.label_encoder.inverse_transform(y_preds)
    sub['target'] = y_preds
    sub.to_csv('submission.csv', index=False)


if __name__ == '__main__':
    train, test, sub = DataLoader('tabular_2022_feb').load()
    corpus = pm.Corpus(x=train, t=test, s=sub)
    corpus.pie(train, 'target')
    # ensemble()
    # model.train(train_x, train_y)
    # skf = _StratifiedKFold(etc, corpus, accuracy_score, n_splits=10).run()
    # y_probs = skf.y_probs
    # y_probs = sum(y_probs) / len(y_probs)
    # y_probs += np.array([0, 0, 0.01, 0.03, 0, 0, 0, 0, 0, 0])
