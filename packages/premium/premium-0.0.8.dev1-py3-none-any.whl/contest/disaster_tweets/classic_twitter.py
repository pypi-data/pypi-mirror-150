#!/usr/bin/env python
#!/usr/bin/env python
from premium.models.bert import BertClassifier
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier
from disaster_tweets.textclean import clean
import numpy as np
import pandas as pd
from cProfile import label
from premium.models.benchmark import Benchmark
from typing import Dict, List, Optional, Set, Tuple

import codefast as cf
import premium as pm
import random
from dofast import SyncFile as syncfile
from nltk.stem import SnowballStemmer
from sklearn.model_selection import train_test_split

snowball = SnowballStemmer("english")
demo = syncfile('d',
                local_dir='/tmp/twitterdisaster',
                remote_dir='/kaggle/twitterdisaster')
train = demo.clone('train_text_cleaned.csv').read_csv()
cf.info('train loaded')
test = demo.clone('test_text_cleaned.csv').read_csv()
cf.info('test loaded')
sub = demo.clone('sample_submission.csv').read_csv().df
train.df.keyword.fillna('X', inplace=True)
train.df.keyword = train.df.keyword.apply(lambda e: e.replace('%20', ' '))

df = train.df
dft = test.df

# df = df.sample(frac=0.1, random_state=42).reset_index(drop=True)
# drop duplicates based on text and keep the most frequent label
# df = df.groupby('text').target.agg(pd.Series.mode).reset_index()
labels = df.target
x = pm.SentenceList(df.text)
x.tfidf()
test = pm.SentenceList(dft.text)
test = x.vectorizer.transform(test.sentences)


def do_benchmark():
    from premium.models.benchmark import Benchmark, get_classifiers
    td = {'x': x.sentences, 'y': labels, 't': test}
    td = pm.TrainData(td)
    models = get_classifiers(use_gpu=True)
    bm = Benchmark(td, models)
    bm.run()


def make_prediction():
    model = pm.classifiers.catboost_classifier()
    model = pm.classifiers.ada_boost_classifier()
    preds = np.round(preds).astype(int).flatten()
    sub.target = preds
    sub.to_csv('submission_twitter.csv', index=False)


def tune(df: pd.DataFrame):
    """ 
    """
    model = pm.classifiers.svm_classifier()
    config = {'max_sentence_len': 80, 'layer_number': 1,
              'bert_name': 'bert-large-uncased'}
    model = BertClassifier(**config)
    make_prediction_now = True
    clf = pm.Classifier(model)
    # df = df.sample(frac=0.1).reset_index(drop=True)
    _x = df.text
    _y = df.target
    indices = np.arange(len(_x))
    x, xv, y, yv, xidx, xvidx = pm.pretools.split(_x,
                                                  _y,
                                                  indices,
                                                  test_size=0.2,
                                                  random_state=random.randint(1, 1 << 20))

    # print(f'Accuracy: {pm.libra.accuracy_score(yv, preds)}')
    clf.fit(_x, _y, epochs=20, batch_size=9)
    if make_prediction_now:
        preds = clf.predict(dft.text).flatten()
        sub['target'] = preds
        sub.to_csv('submission_twitter.csv', index=False)


if __name__ == '__main__':
    tune(df)
    # do_benchmark()
