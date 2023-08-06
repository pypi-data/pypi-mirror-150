#!/usr/bin/env python
#!/usr/bin/env python
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import datetime
import os
import random
import re
import sys
import time
from collections import defaultdict
from functools import reduce
from typing import Dict, List, Optional, Set, Tuple

import codefast as cf
import joblib
import numpy as np
import pandas as pd
import premium as pm
import rich
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text
import transformers
from dofast import SyncFile as syncfile
from nltk.stem import SnowballStemmer
from rich.console import Console
from rich.table import Table
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras import layers
from transformers import AutoModel, BertTokenizerFast

snowball = SnowballStemmer("english")

demo = syncfile('d',
                local_dir='/tmp/twitterdisaster',
                remote_dir='/kaggle/twitterdisaster')
x = demo.clone('train.csv').read_csv()
t = demo.clone('test.csv').read_csv()

x.df.keyword.fillna('X', inplace=True)
x.df.keyword = x.df.keyword.apply(lambda e: e.replace('%20', ' '))
td = pm.TrainData({
    'x': pm.SentenceList(x.df.text),
    'y': pm.LabelData(x.df.target),
    't': pm.SentenceList(t.df.text)
})

x, xt, y, yt = pm.pretools.train_test_split(td.x.sentences,
                                            td.y.labels,
                                            test_size=0.15,
                                            random_state=2022)


def use_classfier() -> tf.keras.Model:
    MODEL_URL = "https://tfhub.dev/google/universal-sentence-encoder/4"
    sentence_encoder_layer = hub.KerasLayer(MODEL_URL,
                                            input_shape=[],
                                            dtype=tf.string,
                                            trainable=False,
                                            name="USE")
    # Create model using sequentinal api
    model = tf.keras.Sequential([
        sentence_encoder_layer,
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(32, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(1, activation="sigmoid", name="output_layer"),
    ],
        name="Model_USE")
    return model


model = use_classfier()
# Compile the model
model.compile(loss="binary_crossentropy",
              optimizer=tf.keras.optimizers.Adam(),
              metrics=["accuracy"])

ES = EarlyStopping(monitor='val_loss',
                   mode='min',
                   patience=10,
                   restore_best_weights=True,
                   verbose=1)

model_history = model.fit(
    x,
    y,
    epochs=20,
    batch_size=16,
    validation_data=(xt, yt),
    callbacks=[ES],
)

preds = model.predict(xt)
preds = np.round(preds).astype(int).flatten()
print(preds)
pm.libra.metrics(yt, preds)

preds = model.predict(td.t.sentences)
preds = np.round(preds).astype(int).flatten()
sub = pd.DataFrame({'id': t.df.id, 'target': preds})
sub.to_csv('submission_twitter.csv', index=False)
