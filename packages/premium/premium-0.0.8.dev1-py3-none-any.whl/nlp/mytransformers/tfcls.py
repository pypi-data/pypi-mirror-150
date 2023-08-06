from transformers import TFBertForSequenceClassification, BertTokenizer, TFBertModel
import tensorflow as tf


class CFG(object):
    MAXLEN = 100
    BATCHSIZE = 32
    EPOCHS = 3
    MODEL_NAME = 'bert-base-uncased'
    DEVICE = 'cuda'
    MODEL_PATH = '/data/cache/'
    DATA_PATH = '/data/cache/'
    NUM_LABELS = 2


def create_model():
    bert_model = TFBertModel.from_pretrained(
        CFG.MODEL_NAME, num_labels=CFG.NUM_LABELS, cache_dir=CFG.MODEL_PATH)

    input_ids = tf.keras.layers.Input(
        shape=(CFG.MAXLEN,), dtype=tf.int32, name='input_ids')
    attention_mask = tf.keras.layers.Input(
        shape=(CFG.MAXLEN,), dtype=tf.int32, name='attention_mask')
    x = bert_model([input_ids, attention_mask])[1]
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.1)(x)
    x = tf.keras.layers.Dense(128, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.1)(x)
    x = tf.keras.layers.Dense(
        CFG.NUM_LABELS, activation='sigmoid')(x)
    model = tf.keras.models.Model(
        inputs=[input_ids, attention_mask], outputs=x)
    return model


def batch_encode(X, tokenizer):
    return tokenizer.batch_encode_plus(
        X,
        max_length=CFG.MAXLEN,
        add_special_tokens=True,  # add [CLS] and [SEP] tokens
        return_attention_mask=True,
        return_token_type_ids=False,  # not needed for this type of ML task
        pad_to_max_length=True,  # add 0 pad tokens to the sequences less than max_length
        return_tensors='tf'
    )
