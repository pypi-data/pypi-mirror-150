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
from dofast import SyncFile as syncfile

demo = syncfile('d',
                local_dir='/tmp/twitterdisaster',
                remote_dir='/kaggle/twitterdisaster')
train = demo.clone('train.csv').read_csv()
test = demo.clone('test.csv').read_csv()
sub = demo.clone('sample_submission.csv').read_csv()
sub = sub.df

df = train.df
dft = test.df
df.text = df.text.apply(clean)
dft.text = dft.text.apply(clean)
labels = df.target
td = pm.TrainData({'x': df.text, 'y': labels, 't': dft.text})
bert_clf = BertClassifier(td)
bert_clf.fit(epochs=20, batch_size=10, validation_split=0.15)
preds = bert_clf.predict()
sub.target = preds
sub.to_csv('submission_twitter.csv', index=False)
