#!/usr/bin/env python

from typing import Dict, List, Tuple

import codefast as cf
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
                                        ReduceLROnPlateau, CSVLogger)
from tensorflow.keras.optimizers import Adam
from torch import embedding
from transformers import (BertConfig, BertTokenizer, DistilBertModel,
                          DistilBertTokenizer, RobertaTokenizer, TFBertModel,
                          TFDistilBertForSequenceClassification,
                          TFRobertaModel, TFXLNetModel, XLNetTokenizer)

from premium.data.preprocess import TrainData


class BertClassifier(object):
    def __init__(self,
                 max_sentence_len: int = 64,
                 layer_number: int = 3,
                 bert_name: str = 'bert-base-uncased',
                 do_lower_case: bool = True,
                 num_labels: int = 1,
                 loss: str = None,
                 cache_dir: str = '/data/cache') -> None:
        """ 
        Args:
            max_sentence_len: max length of sentence
            layer_number: number of embedding layers
            bert_name: name of bert model
            do_lower_case: whether to lower case
            num_labels: number of output classes
        """
        self.max_sentence_len = max_sentence_len
        self.bert_name = bert_name
        self.layer_number = layer_number
        self.do_lower_case = do_lower_case
        self.num_labels = num_labels
        self.loss = loss
        self.cache_dir = cache_dir
        if not cf.io.exists(self.cache_dir):
            cf.warning('cache_dir not exists, create one')

    def get_tokenizer(self):
        if self.bert_name in ('bert-large-uncased', 'bert-base-uncased'):
            return BertTokenizer.from_pretrained(self.bert_name,
                                                 cache_dir=self.cache_dir)
        elif self.bert_name in ('roberta-large', 'roberta-base'):
            return RobertaTokenizer.from_pretrained(self.bert_name,
                                                    cache_dir=self.cache_dir)
        elif self.bert_name in ('xlnet-base-cased', 'xlnet-large-cased'):
            return XLNetTokenizer.from_pretrained(self.bert_name,
                                                  cache_dir=self.cache_dir)
        elif self.bert_name in ('distilbert-base-uncased'):
            return DistilBertTokenizer.from_pretrained(
                self.bert_name, cache_dir=self.cache_dir)
        else:
            raise ValueError('bert_name not supported')

    def get_pretrained_model(self):
        config = BertConfig.from_pretrained(self.bert_name,
                                            output_hidden_states=True,
                                            output_attentions=True)
        if self.bert_name in ('bert-large-uncased', 'bert-base-uncased'):
            return TFBertModel.from_pretrained(self.bert_name,
                                               config=config,
                                               cache_dir=self.cache_dir)
        elif self.bert_name in ('roberta-large', 'roberta-base'):
            return TFRobertaModel.from_pretrained(self.bert_name,
                                                  cache_dir=self.cache_dir)
        elif self.bert_name in ('xlnet-base-cased', 'xlnet-large-cased'):
            return TFXLNetModel.from_pretrained(self.bert_name,
                                                cache_dir=self.cache_dir)
        elif self.bert_name in ('distilbert-base-uncased'):
            return TFDistilBertForSequenceClassification.from_pretrained(
                self.bert_name, cache_dir=self.cache_dir)
        else:
            raise ValueError('bert_name not supported')

    def _bert_encode(self, texts: List[str]):
        cf.info('start {} encoding'.format(self.bert_name))
        tokenizer = self.get_tokenizer()
        input_ids = []
        attention_masks = []

        for text in texts:
            encoded = tokenizer.encode_plus(
                text,
                add_special_tokens=True,
                max_length=self.max_sentence_len,
                padding='max_length',
                return_attention_mask=True,
                truncation=True,
            )
            input_ids.append(encoded['input_ids'])
            attention_masks.append(encoded['attention_mask'])
        cf.info('{} encoding finished'.format(self.bert_name))
        return np.array(input_ids), np.array(attention_masks)

    def _create_model(self, sequnce_len: int = 64):
        cf.info('start creating model')
        input_ids = tf.keras.Input(shape=(sequnce_len, ), dtype='int32')
        attention_masks = tf.keras.Input(shape=(sequnce_len, ), dtype='int32')

        bert_model = self.get_pretrained_model()
        cf.info('model {} created'.format(self.bert_name))
        # Get the final embeddings from the BERT model
        embedding = bert_model([input_ids, attention_masks])
        cf.info('embedding length', len(embedding))
        cf.info('embedding[0] shape', embedding[0].shape)
        # if self.bert_name in ('bert-large-uncased', 'bert-base-uncased',
        #                       'roberta-large', 'roberta-base',
        #                       'xlnet-base-cased', 'xlnet-large-cased'):
        #     embedding = embedding[0]
        # else:

        embedding = embedding[0]
        embedding = tf.keras.layers.Flatten()(embedding)
        embedding = Dense(128, activation='relu')(embedding)
        for _ in range(self.layer_number):
            embedding = Dense(128, activation='relu')(embedding)
            embedding = Dropout(0.2)(embedding)

        if self.num_labels == 1:
            output = Dense(1, activation='sigmoid')(embedding)
            loss = 'binary_crossentropy'
        else:
            output = Dense(self.num_labels, activation='softmax')(embedding)
            loss = 'sparse_categorical_crossentropy'

        if self.loss is not None:
            loss = self.loss
        cf.info('setting output dim to {}'.format(self.num_labels))
        cf.info('setting loss to {}'.format(loss))

        model = tf.keras.models.Model(inputs=[input_ids, attention_masks],
                                      outputs=output)

        model.compile(Adam(lr=6e-6), loss=loss, metrics=['accuracy'])
        cf.info('model created')
        return model

    def fit(self,
            x,
            y,
            epochs: int = 10,
            batch_size: int = 32,
            early_stop: int = 5,
            validation_split: float = 0.2) -> Tuple[tf.keras.Model, Dict]:
        """
        Args:
            batch_size(int): batch size, if set -1, will try and found the max batch 
            size that suits the gpu.
        """
        ids, masks = self._bert_encode(x)
        model = self._create_model(sequnce_len=self.max_sentence_len)
        cf.info('model summary:')
        print(model.summary())

        # trained the classfier on use layer
        # filepath = "models/weights-improvement-{epoch:02d}-{val_accuracy:.2f}.hdf5"
        early_stopping = EarlyStopping(
            monitor='val_loss',
            mode='min',
            patience=early_stop,
            restore_best_weights=True,
            # restore model weights from the epoch with the best value of the monitored quantity
            verbose=1)

        mcp_save = ModelCheckpoint(filepath='/tmp/',
                                   save_weights_only=True,
                                   monitor='val_loss',
                                   mode='auto')

        reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss',
                                           factor=0.1,
                                           patience=5,
                                           verbose=1,
                                           mode='min')

        csv_logger = CSVLogger('/tmp/keraslog.csv', append=True, separator=';')
        history = model.fit(
            [ids, masks],
            y,
            validation_split=validation_split,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, mcp_save, reduce_lr_loss, csv_logger],
        )
        self.model = model
        return history

    def predict(self, xt):
        cf.info('start predicting')
        tids, tmasks = self._bert_encode(xt)
        preds = self.model.predict([tids, tmasks])
        preds = np.round(preds).astype(int)
        cf.info('predict finished')
        return preds

    def show_history(self, history):
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()
