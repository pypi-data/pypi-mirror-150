from tabnanny import verbose
import numpy as np
from nlp.mytransformers.tfcls import create_model, batch_encode, CFG
import tensorflow as tf
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMClassifier
import premium as pm
import random
import codefast as cf
import datasets
from transformers import AutoModel, BertTokenizer, pipeline
from utils import device

device = device()
cf.info('device is:', device)


def experiment():
    model_name = 'bert-base-uncased'
    bt = BertTokenizer.from_pretrained(model_name,
                                       cache_dir='/tmp/cache/',
                                       device=device)
    text = 'this is a test'
    tokens = bt.encode(text)
    cf.info('encode tokens', tokens)
    cf.info('encode plus', bt.encode_plus(text, add_special_tokens=True))
    cf.info('batch encode plus',
            bt.batch_encode_plus([text, text], add_special_tokens=True))

    tokens = bt.encode(text, return_tensors='pt').to(device)
    model = AutoModel.from_pretrained(model_name,
                                      cache_dir="/data/cache/").to(device)
    cf.info('model is ', model)
    cf.info('encode tokens', tokens)
    cf.info('tensor shape', tokens.shape)

    output = model(tokens)
    # cf.info('output is ', output)
    cf.info('last hidden layer shape', output.last_hidden_state.shape)
    cf.info('last hidden layer', output.last_hidden_state)
    cf.info('feature is ', output.last_hidden_state[0][0])

    feature_extractor = pipeline('feature-extraction',
                                 model=model,
                                 tokenizer=bt,
                                 device=0)
    cf.info('feature extractor is ', feature_extractor)

    texts = ['are you okay', 'yes im fine']
    features = feature_extractor(texts)
    cf.info('features length ', len(features))
    cf.info('first feature size', len(features[0]))
    cf.info('first feature first token size', len(features[0][0]))

    final_features = [e[0] for e in features]
    print(final_features)


def get_feature_extractor():
    model_name = 'bert-base-uncased'
    bt = BertTokenizer.from_pretrained(model_name, cache_dir='/data/cache/')
    model = AutoModel.from_pretrained(model_name, cache_dir="/data/cache/")
    feature_extractor = pipeline('feature-extraction',
                                 model=model,
                                 tokenizer=bt,
                                 device=0)
    return feature_extractor


def load_data():
    dataset_list = datasets.list_datasets()
    cf.info('dataset list length is', len(dataset_list))
    data_name = 'imdb'
    poem = datasets.load_dataset(data_name, cache_dir='/data/cache/')
    poem.set_format(type='pandas')
    cf.info('train info', poem['train'].info)
    df = poem['train'][:]
    dft = poem['test'][:]
    dfv = poem['test'][:]
    cf.info('data head')
    print(df.head())
    cf.info('train dataset shape', poem['train'].shape)
    return df, dft, dfv


def try_linear_model():
    # score 0.74
    df, dft, dfv = load_data()
    fe = get_feature_extractor()
    features = fe(df['verse_text'].to_list())
    features = [e[0] for e in features]
    cf.info('length of features', len(features))
    cf.info('size of feature[0] is ', len(features[0]))

    labels = df['label']
    lgbc = LGBMClassifier(n_estimators=100,
                          random_state=42,
                          n_jobs=-1,
                          device='gpu')
    lgbc = LogisticRegression(solver='lbfgs', multi_class='multinomial')
    lgbc.fit(features, labels)
    cf.info('training completes')

    features_v = fe(dfv['verse_text'].to_list())
    features_v = [e[0] for e in features_v]
    preds = lgbc.predict(features_v)

    acc = accuracy_score(dfv['label'], preds)
    cf.info('accuracy is', acc)


def get_train_data():
    df, dft, dfv = load_data()
    text_column = 'text'
    x = df[text_column].to_list()
    x.extend(dfv[text_column].to_list())
    y = df['label'].to_list()
    y.extend(dfv['label'].to_list())
    return df[text_column], df['label']


def try_bert():
    x, y = get_train_data()
    CFG.NUM_LABELS = len(set(y))
    CFG.EPOCHS = 3
    cf.info('x length is', len(x))
    cf.info('y length is', len(y))

    model = create_model()
    print(model.summary())

    opt = tf.keras.optimizers.Adam(learning_rate=0.001)
    model.compile(optimizer=opt,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    tokenizer = BertTokenizer.from_pretrained(CFG.MODEL_NAME,
                                              cache_dir=CFG.DATA_PATH)
    x, xv, y, yv = pm.pretools.split(x, y, test_size=0.2)
    x = batch_encode(x, tokenizer).values()
    y = np.array(y)
    xv = batch_encode(xv, tokenizer).values()
    yv = np.array(yv)
    cf.info('type of x is', type(x))
    cf.info('x is ', x)
    model.fit(x, y, validation_data=(xv, yv), epochs=CFG.EPOCHS, verbose=1)


def _fa():
    from premium.models.bert import BertClassifier
    bc = BertClassifier(max_sentence_len=360,
                        layer_number=2,
                        bert_name='bert_large_uncased',
                        cache_dir='/data/cache/')
    x, y = get_train_data()
    bc.fit(x, y, batch_size=7, epochs=10)


# TODO imdb bert to 0.9 accuracy
# with bert base and max_sentence_len to 300

if __name__ == '__main__':
    experiment()
