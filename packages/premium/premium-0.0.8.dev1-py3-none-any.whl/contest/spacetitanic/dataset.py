#!/usr/bin/env python

from cProfile import label
from typing import Dict, List, Optional, Set, Tuple

import codefast as cf
import numpy as np
import pandas as pd
from codefast.utils import timethis
from dofast import SyncFile as syncfile
from flaml import AutoML
from sklearn.ensemble import VotingClassifier
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import seaborn as sns

import premium as pm
from disaster_tweets.textclean import clean
from premium.models.benchmark import Benchmark, get_classifiers


class Scavenger(object):
    def __init__(self):
        self.train_file = 'train.csv'
        self.test_file = 'test.csv'
        self.train_imputed = 'train_imputed.csv'

    def load_data(self):
        demo = syncfile('d',
                        local_dir='/tmp/spacetitanic',
                        remote_dir='/kaggle/spacetitanic')
        self.train = demo.clone(self.train_file).read_csv().df
        self.train_imputed = demo.clone(self.train_imputed).read_csv().df
        self.labels = self.train_imputed.Transported

        self.test = demo.clone(self.test_file).read_csv().df
        self.sub = demo.clone('sample_submission.csv').read_csv().df

    def r_missing_features(self):
        """find missing feature names
        ['HomePlanet', 'CryoSleep', 'Cabin', 'Destination', 'Age', 'VIP', 
        'RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck', 'Name']
        """
        missing_features = []
        for col in self.all.columns:
            if self.all[col].isna().sum() > 0:
                missing_features.append(col)
        return missing_features

    def fill_missing(self,
                     df,
                     columns: List[str],
                     strategy: str = 'most_frequent') -> pd.DataFrame:
        imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)
        df[columns] = imputer.fit_transform(df[columns])
        return df

    def convert_cat_to_int(self, df,
                           columns: List[Tuple[str, str]]) -> pd.DataFrame:
        for col, dtype in columns:
            df = pd.get_dummies(df, columns=[col], dtype=dtype)
        return df

    def convert_bool_to_int(self, df, columns: List[str]) -> pd.DataFrame:
        for col in columns:
            df[col] = df[col].astype(int)
        return df

    def split_cabin(self, df) -> pd.DataFrame:
        df[['cabin', 'num', 'port']] = df.Cabin.str.split('/', expand=True)
        df['num'].fillna(42, inplace=True)
        df['num'] = df.num.astype(int)
        df.drop(['Cabin'], axis=1, inplace=True)
        return df

    def drop_columns(self, df, columns: List[str]) -> pd.DataFrame:
        df.drop(columns, axis=1, inplace=True)
        return df

    @timethis
    def preprocess_imputed(self):
        cf.info('start preprocessing')
        df = self.train_imputed
        cf.info('split cabin')
        df = self.split_cabin(df)
        df.drop(['PassengerId', 'Transported', 'first_name', 'last_name'],
                axis=1,
                inplace=True)
        missing_features = [
            'HomePlanet', 'CryoSleep', 'Destination', 'VIP', 'cabin', 'port'
        ]
        df = self.fill_missing(df, missing_features)
        df = pd.get_dummies(df, prefix_sep='__')
        from sklearn.impute import KNNImputer
        knn_imp = KNNImputer(n_neighbors=9)
        df.loc[:, :] = knn_imp.fit_transform(df)
        df['consume'] = df.FoodCourt + df.ShoppingMall + df.Spa + df.VRDeck
        pm.pretools.birdview(df)
        df.drop(['ppid'], axis=1, inplace=True)

        N = len(self.train) - 1
        train = df[:N]
        test = df[N:]
        labels = self.labels[:N].astype(int)
        print(test.shape)
        print(test.tail())
        return train, test, labels

    def run(self):
        pass
