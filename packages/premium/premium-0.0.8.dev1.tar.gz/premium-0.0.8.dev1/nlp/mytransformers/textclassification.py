from umap import UMAP
from transformers import AutoModel, AutoTokenizer
from sklearn.preprocessing import MinMaxScaler
from datasets import list_datasets, load_dataset
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import codefast as cf
from sklearn.linear_model import LogisticRegression
from transformers import AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, f1_score
from transformers import Trainer, TrainingArguments
from transformers import Trainer
import os
os.environ['TRANSFORMERS_CACHE'] = '/data/cache/'


class Config(object):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_name = 'distilbert-base-uncased'


def load_data():
    datasets = list_datasets()
    print(
        f"There are {len(datasets)} datasets currently available on the Hub.")
    print(f"The first 10 are: {datasets[:10]}")

    metadata = list_datasets(with_details=True)[datasets.index(
        "emotion")]     # Show dataset description
    print("Description:", metadata.description, "\n")
    # Show first 8 lines of the citation string
    print("Citation:", "\n".join(metadata.citation.split("\n")[:8]))

    emotions = load_dataset("emotion",  cache_dir="/data/cache/")
    emotions.set_format(type="pandas")
    df = emotions["train"][:]
    print(df.head())
    print(df.shape)

    def label_int2str(row, split):
        return emotions[split].features["label"].int2str(row)

    df["label_name"] = df["label"].apply(label_int2str, split="train")
    print(df.head(10))
    return df, emotions


def plot_emotion_distribution(df):
    emotion_count = df["label_name"].value_counts()
    emotion_count.plot(kind="bar")
    plt.show()


def tokenization(df):
    model_name = 'distilbert-base-uncased'
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    cf.info('vocab size', tokenizer.vocab_size)
    cf.info('vocab files name', tokenizer.vocab_files_names)
    cf.info('special token map', tokenizer.special_tokens_map)
    cf.info('model max length', tokenizer.model_max_length)
    encoded_str = tokenizer.encode("are you really okay?")
    cf.info('encoded string is', encoded_str)

    for token in encoded_str:     # decoding the token
        print(token, tokenizer.decode(token))
    return tokenizer


def feature_extraction(tokenizer, emotions):
    cf.info('transformers as feature extraction')
    model_name = 'distilbert-base-uncased'
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    cf.info('current device is', device)
    model = AutoModel.from_pretrained(model_name).to(device)

    text = "this is a test"
    # return_tensors="pt" returns PyTorch tensors
    text_tensor = tokenizer.encode(text, return_tensors="pt").to(device)
    cf.info('text tensor is', text_tensor)

    output = model(text_tensor)
    cf.info('output is', output)
    cf.info('output last hidden layer shape', output.last_hidden_state.shape)

    def _tokenize(batch):
        return tokenizer(batch["text"], padding=True, truncation=True)

    emotions.reset_format()
    emotions_encoded = emotions.map(_tokenize, batched=True, batch_size=None)
    cf.info('emotions_encoded train features',
            emotions_encoded['train'].features)
    return emotions_encoded, model


def inputids2hidden_state(emotions_encoded, model):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def forward_pass(batch):
        input_ids = torch.tensor(batch["input_ids"]).to(device)
        attention_mask = torch.tensor(batch["attention_mask"]).to(device)
        with torch.no_grad():
            last_hidden_state = model(input_ids,
                                      attention_mask).last_hidden_state
            last_hidden_state = last_hidden_state.cpu().numpy()
            # Use average of unmasked hidden states for classification
            lhs_shape = last_hidden_state.shape
            boolean_mask = ~np.array(batch["attention_mask"]).astype(bool)
            boolean_mask = np.repeat(boolean_mask, lhs_shape[-1], axis=-1)
            boolean_mask = boolean_mask.reshape(lhs_shape)
            masked_mean = np.ma.array(last_hidden_state,
                                      mask=boolean_mask).mean(axis=1)
            batch["hidden_state"] = masked_mean.data
            return batch

    emotions_encoded = emotions_encoded.map(forward_pass,
                                            batched=True,
                                            batch_size=16)
    print(emotion_encoded['train'].features)
    return emotions_encoded


def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    f1 = f1_score(labels, preds, average="weighted")
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1}


def main(emotions_encoded, model):
    X_train = np.array(emotions_encoded["train"]["hidden_state"])
    X_valid = np.array(emotions_encoded["validation"]["hidden_state"])
    y_train = np.array(emotions_encoded["train"]["label"])
    y_valid = np.array(emotions_encoded["validation"]["label"])
    cf.info('train shape, valid shape', X_train.shape, X_valid.shape)

    lr_clf = LogisticRegression(n_jobs=-1, penalty="none")
    lr_clf.fit(X_train, y_train)
    score = lr_clf.score(X_valid, y_valid)
    cf.info('lr score', score)

    num_labels = 6
    model = (AutoModelForSequenceClassification
             .from_pretrained(Config.model_name, num_labels=num_labels)
             .to(Config.device))

    emotions_encoded.set_format(
        "torch", columns=["input_ids", "attention_mask", "label"])

    batch_size = 64
    logging_steps = len(emotions_encoded["train"]) // batch_size
    training_args = TrainingArguments(output_dir="results",
                                      num_train_epochs=5,
                                      learning_rate=2e-5,
                                      per_device_train_batch_size=batch_size,
                                      per_device_eval_batch_size=batch_size,
                                      load_best_model_at_end=False,
                                      metric_for_best_model="f1",
                                      weight_decay=0.01,
                                      evaluation_strategy="epoch",
                                      disable_tqdm=False,
                                      logging_steps=logging_steps,)

    trainer = Trainer(model=model, args=training_args,
                      compute_metrics=compute_metrics,
                      train_dataset=emotions_encoded["train"],
                      eval_dataset=emotions_encoded["validation"])
    trainer.train()


if __name__ == "__main__":
    df, emotions = load_data()
    # plot_emotion_distribution(df)
    tokenizer = tokenization(df)
    emotion_encoded, model = feature_extraction(tokenizer, emotions)
    emotion_encoded = inputids2hidden_state(emotion_encoded, model)
    main(emotion_encoded, model)
