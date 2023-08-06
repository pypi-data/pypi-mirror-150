#!/usr/bin/env python
from typing import Dict, List, Optional, Set, Tuple
import codefast as cf
from codefast.utils import timethis
import numpy as np
import pandas as pd

import premium as pm
from premium.models.benchmark import Benchmark, get_classifiers
from spacetitanic.dataset import Scavenger


class FineTune(object):
    def __init__(self) -> None:
        self.sca = Scavenger()
        self.sca.load_data()
        x, xt = self.sca.train, self.sca.test
        all_data = pd.concat([x, xt], axis=0)

        all_data['CryoSleep'].fillna(False, inplace=True)
        all_data['Cabin'].fillna('None', inplace=True)
        all_data['VIP'].fillna(all_data.VIP.mode()[0], inplace=True)
        all_data['HomePlanet'].fillna(all_data.HomePlanet.mode()[0],
                                      inplace=True)
        all_data['Destination'].fillna(all_data.Destination.mode()[0],
                                       inplace=True)

        # Replace continuous variables with specific values (0) or averages.
        all_data['Age'].fillna(all_data.Age.mean(), inplace=True)
        all_data[['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']] =\
        all_data[['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']].fillna(0)

        all_data['Deck'] = all_data.Cabin.apply(lambda x: str(x)[:1])
        all_data['Side'] = all_data.Cabin.apply(lambda x: str(x)[-1:])
        all_data['PassengerGroup'] = all_data['PassengerId'].apply(
            lambda x: x.split('_')[0])
        all_data['PassengerNo'] = all_data['PassengerId'].apply(
            lambda x: x.split('_')[1])

        # Generate new variables based on the amount of money used for various services.
        all_data['TotalSpend'] = all_data['RoomService'] + all_data[
            'FoodCourt'] + all_data['ShoppingMall'] + all_data[
                'Spa'] + all_data['VRDeck']
        all_data['PctRoomService'] = all_data['RoomService'] / all_data[
            'TotalSpend']
        all_data[
            'PctFoodCourt'] = all_data['FoodCourt'] / all_data['TotalSpend']
        all_data['PctShoppingMall'] = all_data['ShoppingMall'] / all_data[
            'TotalSpend']
        all_data['PctSpa'] = all_data['Spa'] / all_data['TotalSpend']
        all_data['PctVRDeck'] = all_data['VRDeck'] / all_data['TotalSpend']

        fill_cols = [
            'PctRoomService', 'PctFoodCourt', 'PctShoppingMall', 'PctSpa',
            'PctVRDeck'
        ]
        all_data[fill_cols] = all_data[fill_cols].fillna(0)
        # Create new variables by dividing age groups.
        all_data['AgeBin'] = 7
        for i in range(6):
            all_data.loc[(all_data.Age >= 10 * i) & (all_data.Age < 10 *
                                                     (i + 1)), 'AgeBin'] = i

        all_data.drop(['PassengerId', 'Name', 'Cabin'], axis=1, inplace=True)

        from sklearn.preprocessing import LabelEncoder
        for col in all_data.columns[all_data.dtypes == object]:
            if col != 'Transported':
                le = LabelEncoder()
                all_data[col] = le.fit_transform(all_data[col])

        all_data['CryoSleep'] = all_data['CryoSleep'].astype('int')
        all_data['VIP'] = all_data['VIP'].astype('int')

        train = all_data[~all_data.Transported.isnull()]
        train, self.xt = all_data.iloc[:train.shape[0]], all_data.iloc[
            train.shape[0]:].drop(['Transported'], axis=1)
        print(train.shape, self.xt.shape)
        self.x, self.y = train.drop(['Transported'],
                                    axis=1), train['Transported']
        self.y = self.y.astype('int')
        print('all data info:', self.xt.head())
        print(all_data.info())
        print(self.y.value_counts())

    @timethis
    def catboost(self):
        model = pm.demo.classifiers.catboost_classifier()
        clf = pm.Classifier(model)
        _, preds = clf.cv2(self.x, self.y, cv=50, test=self.xt)
        print(preds)
        self.export_submission(preds)

    @timethis
    def lightgbm(self):
        model = pm.demo.classifiers.lightgbm_classifier()
        clf = pm.Classifier(model)
        _, preds = clf.cv2(self.x, self.y, cv=100, test=self.xt)
        self.export_submission(preds)

    def export_submission(self, preds: list):
        cf.info('exporting predictions')
        preds = preds.astype(bool)
        sub = pd.read_csv('/tmp/spacetitanic/sample_submission.csv')
        sub['Transported'] = preds
        sub.to_csv('submission_spacetitanic.csv', index=False)

    def do_benchmark(self):
        cf.info('running benchmark')
        models = get_classifiers()
        td = pm.TrainData({'x': self.x, 'y': self.y, 'xt': self.xt})
        benchmark = Benchmark(td, models)
        benchmark.run(display_only=True)

    @timethis
    def keras(self):
        from premium.models.tensorflow.binary_classifier import BinaryClassifier as tfbc
        feature_number = self.x.shape[1]
        model = tfbc(feature_number, epoches=100)
        clf = pm.Classifier(model)
        _, preds = clf.cv2(self.x, self.y, cv=3, test=self.xt)
        # self.export_submission(preds)

    def run(self):
        # self.catboost()
        # self.do_benchmark()
        # self.lightgbm()
        self.keras()
