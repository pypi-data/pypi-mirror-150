"""
FIXME: Verify predict and compute_accuracy() functions by comparing to older versions in git

$ python main.py
WARNING:__main__:args: []
WARNING:__main__:kwargs: {}
100%|████████████████████████████████████████████████████████████████████████████████████████████| 7613/7613 [00:00<00:00, 242018.81it/s]
Epoch: 1, loss: 0.71129, Train accuracy: 0.56970, Test accuracy: 0.64698
Epoch: 2, loss: 0.62170, Train accuracy: 0.64458, Test accuracy: 0.71260
Epoch: 3, loss: 0.52818, Train accuracy: 0.67421, Test accuracy: 0.70997
Epoch: 4, loss: 0.47667, Train accuracy: 0.70690, Test accuracy: 0.73753
Epoch: 5, loss: 0.45808, Train accuracy: 0.73113, Test accuracy: 0.74672
Epoch: 6, loss: 0.40075, Train accuracy: 0.75376, Test accuracy: 0.74803
Epoch: 7, loss: 0.43526, Train accuracy: 0.76558, Test accuracy: 0.75066
Epoch: 8, loss: 0.42900, Train accuracy: 0.79317, Test accuracy: 0.75722
Epoch: 9, loss: 0.49162, Train accuracy: 0.79054, Test accuracy: 0.76247
Epoch: 10, loss: 0.38202, Train accuracy: 0.80324, Test accuracy: 0.75984


$ python main.py --tokenizer=tokenize_spacy --stride=2 --vocab_size=4000 --kernel_lengths=[3,4,5] --text_len=40
WARNING:__main__:args: []
WARNING:__main__:kwargs: {'tokenizer': 'tokenize_spacy', 'stride': '2', 'vocab_size': '4000', 'kernel_lengths': '[3,4,5]', 'text_len': '40'}
WARNING:__main__:NEW KWARGS: tokenizer: tokenize_spacy (<class 'str'>)
WARNING:__main__:NEW KWARGS: vocab_size: 4000 (<class 'int'>)
WARNING:__main__:NEW KWARGS: kernel_lengths: (3, 4, 5) (<class 'tuple'>)
WARNING:__main__:NEW KWARGS: stride: 2 (<class 'int'>)
100%|███████████████████████████████████████████████████████████████████████████████████████████████| 7613/7613 [00:36<00:00, 207.29it/s]
Epoch: 1, loss: 0.73025, Train accuracy: 0.55247, Test accuracy: 0.65748
Epoch: 2, loss: 0.52448, Train accuracy: 0.62808, Test accuracy: 0.68241
Epoch: 3, loss: 0.49091, Train accuracy: 0.67319, Test accuracy: 0.72310
Epoch: 4, loss: 0.42739, Train accuracy: 0.69917, Test accuracy: 0.68898
Epoch: 5, loss: 0.35826, Train accuracy: 0.72179, Test accuracy: 0.74541
Epoch: 6, loss: 0.38785, Train accuracy: 0.74091, Test accuracy: 0.73885
Epoch: 7, loss: 0.38957, Train accuracy: 0.76222, Test accuracy: 0.75066
Epoch: 8, loss: 0.30744, Train accuracy: 0.76850, Test accuracy: 0.75328
Epoch: 9, loss: 0.30294, Train accuracy: 0.78178, Test accuracy: 0.75984
Epoch: 10, loss: 0.39879, Train accuracy: 0.79988, Test accuracy: 0.76115

FIXME:
$ python main.py --tokenizer=tokenize_re --stride=1 --vocab_size=1500 --kernel_lengths=[2,3,4,5] --text_len=35
WARNING:__main__:args: []
WARNING:__main__:kwargs: {'tokenizer': 'tokenize_re', 'stride': '1', 'vocab_size': '1500', 'kernel_lengths': '[2,3,4,5]', 'text_len': '35'}
WARNING:__main__:NEW KWARGS: tokenizer: tokenize_re (<class 'str'>)
WARNING:__main__:NEW KWARGS: vocab_size: 1500 (<class 'int'>)
WARNING:__main__:NEW KWARGS: kernel_lengths: (2, 3, 4, 5) (<class 'tuple'>)
WARNING:__main__:NEW KWARGS: stride: 1 (<class 'int'>)
100%|████████████████████████████████████████████████████████████████████████████████████████████| 7613/7613 [00:00<00:00, 240734.29it/s]
Traceback (most recent call last):
  File "/home/hobs/code/tangibleai/nlpia2/src/nlpia2/ch08/cnn-classify-text/main.py", line 305, in <module>
    pipeline.train()
  File "/home/hobs/code/tangibleai/nlpia2/src/nlpia2/ch08/cnn-classify-text/main.py", line 249, in train
    y_pred = self.model(x_batch)
  File "/home/hobs/anaconda3/envs/nlpia2/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1110, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/hobs/code/tangibleai/nlpia2/src/nlpia2/ch08/cnn-classify-text/cnn/model.py", line 80, in forward
    x = self.embedding(x)
  File "/home/hobs/anaconda3/envs/nlpia2/lib/python3.9/site-packages/torch/nn/modules/module.py", line 1110, in _call_impl
    return forward_call(*input, **kwargs)
  File "/home/hobs/anaconda3/envs/nlpia2/lib/python3.9/site-packages/torch/nn/modules/sparse.py", line 158, in forward
    return F.embedding(
  File "/home/hobs/anaconda3/envs/nlpia2/lib/python3.9/site-packages/torch/nn/functional.py", line 2183, in embedding
    return torch.embedding(weight, input, padding_idx, scale_grad_by_freq, sparse)
IndexError: index out of range in self


"""

from collections import Counter
from dataclasses import dataclass
from itertools import chain
import logging
from pathlib import Path
import re
import sys
import numpy as np

from sklearn.model_selection import train_test_split
import torch
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.utils.data import Dataset
from tqdm import tqdm

from cnn.model import CNNTextClassifier
from cnn.language_model import nlp

import pandas as pd

DATA_DIR = Path(__file__).parent / 'data'

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


def tokenize_spacy(doc):
    return [tok.text for tok in nlp(doc) if tok.text.strip()]


def tokenize_re(doc):
    return [tok for tok in re.findall(r'\w+', doc)]


@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False)
class Parameters:
    filepath: str = 'disaster-tweets.csv'
    usecols: tuple = ('text', 'target')
    tokenizer: str = 'tokenize_re'

    seq_len: int = 35
    vocab_size: int = 2000

    embedding_size: int = 64
    kernel_lengths: tuple = (2, 3, 4, 5)
    strides: tuple = (2, 2, 2, 2)
    conv_output_size: int = 32
    stride: int = 2

    # Training parameters
    epochs: int = 10
    batch_size: int = 12
    learning_rate: float = 0.001
    test_size = 0.1

    dropout_portion = 0.2

    case_sensitive = True


HYPERPARAMS = Parameters()


def pad(sequence, pad_value=0, seq_len=HYPERPARAMS.seq_len):
    log.debug(f'BEFORE PADDING: {sequence}')
    padded = list(sequence)[:seq_len]
    padded = padded + [pad_value] * (seq_len - len(padded))
    log.debug(f'AFTER PADDING: {sequence}')
    return padded


def load_dataset_spacy(filepath='tweets.csv', usecols=[0, -1], tokenizer=tokenize_spacy, params=HYPERPARAMS):
    """ load and preprocess csv file: return [(token id sequences, label)...]

    1. Simplified: load the CSV
    2. NOPE: case folding:
    3. NOPE: remove non-letters (nonalpha):
    4. NOPE: remove stopwords
    5. Simplified: tokenize with regex
    6. Simplified: filter infrequent words
    7. Simplified: compute reverse index
    8. Simplified: transform token sequences to integer id sequences
    9. Simplified: pad token id sequences
    10. Simplified: train_test_split
    """

    if not Path(filepath).is_file():
        filepath = DATA_DIR / filepath

    # 1. Simplified: load the CSV

    df = pd.read_csv(filepath, usecols=list(usecols))

    # 2. NOPE: case folding:

    texts = map(str.lower, df['texts'])

    # 3. NOPE: remove non-letters (nonalpha):
    # texts = re.sub(r'[^A-Za-z]', t, ' ') for t in texts]
    # 4. NOPE: remove stopwords
    # 5. Simplified: tokenize with regex

    tokenized_texts = map(re.compile(r'\w+').findall, texts)

    # 6. Simplified: filter infrequent words

    counts = Counter(chain(*tokenized_texts))
    vocab = ['<PAD>'] + [x[0] for x in counts.most_common(params.vocab_size)]

    # 7. Simplified: compute reverse index

    tok2id = dict(zip(vocab, range(len(vocab))))

    # 8. Simplified: transform token sequences to integer id sequences

    id_sequences = [map(tok2id.get, seq) for seq in tokenized_texts]

    # 9. Simplified: pad token id sequences

    id_sequences = [list(map(pad, seq)) for seq in id_sequences]

    # 10. Simplified: train_test_split

    return dict(zip(
        'x_train x_test y_train y_test'.split(),
        train_test_split(
            X=id_sequences,
            y=df['target'],
            test_size=params.test_size,
            random_state=0)))


def load_dataset(filepath='tweets.csv', usecols=[0, -1], tokenizer=tokenize_re, params=HYPERPARAMS, **kwargs):
    """ load and preprocess csv file: return [(token id sequences, label)...]

    1. Simplified: load the CSV
    2. NOPE: case folding:
    3. NOPE: remove non-letters (nonalpha):
    4. NOPE: remove stopwords
    5. Simplified: tokenize with regex
    6. Simplified: filter infrequent words
    7. Simplified: compute reverse index
    8. Simplified: transform token sequences to integer id sequences
    9. Simplified: pad token id sequences
    10. Simplified: train_test_split
    """
    if not Path(filepath).is_file():
        filepath = Path(DATA_DIR) / filepath
    df = pd.read_csv(filepath.open(), usecols=usecols)
    texts = df[usecols[0]].values
    targets = df[usecols[1]].values
    texts = [re.sub(r'[^A-Za-z0-9.?!]+', ' ', x) for x in texts]
    texts = [tokenizer(doc) for doc in tqdm(texts)]
    counts = Counter(chain(*texts))
    vocab = ['<PAD>'] + [x[0] for x in counts.most_common(params.vocab_size)]
    tok2id = dict(zip(vocab, range(len(vocab))))

    # 8. Simplified: transform token sequences to integer id sequences

    id_sequences = [[i for i in map(tok2id.get, seq) if i is not None] for seq in texts]

    # 9. Simplified: pad token id sequences

    padded_sequences = []
    for s in id_sequences:
        padded_sequences.append(pad(s))
    padded_sequences = torch.IntTensor(padded_sequences)

    return dict(zip(
        'x_train x_test y_train y_test'.split(),
        train_test_split(
            padded_sequences,
            targets,
            test_size=HYPERPARAMS.test_size,
            random_state=0)))


class DatasetMapper(Dataset):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


def calculate_accuracy(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    true_positives = 0
    true_negatives = 0
    for true, pred in zip(y_true, y_pred):
        if (pred >= 0.5) and (true == 1):
            true_positives += 1
        elif (pred < 0.5) and (true == 0):
            true_negatives += 1
        else:
            pass
    # Return accuracy
    return (true_positives + true_negatives) / len(y_true)


class Pipeline(Parameters):

    def __init__(self, *args, **kwargs):
        # self.x_train, self.y_train, self.x_test, self.y_test:
        super().__init__()
        log.info(args)
        log.info(kwargs)
        for param_name, param_val in super().__dict__.items():

            log.info(f'DEFAULT: {param_name}: {param_val}')
            kwarg_val = kwargs.get(param_name)
            if kwarg_val is not None:
                dest_type = type(param_val)
                if not isinstance(param_val, str) and isinstance(kwarg_val, str):
                    kwarg_val = eval(kwarg_val)
                setattr(self, param_name, dest_type(kwarg_val))
                log.warning(f'NEW KWARGS: {param_name}: {getattr(self, param_name)} ({type(getattr(self, param_name))})')
        self.__dict__.update(load_dataset(
            filepath=self.filepath,
            usecols=list(self.usecols),
            tokenizer=globals()[self.tokenizer],
            **kwargs))
        model_kwargs = {k: v for (k, v) in vars(self).items() if not k.startswith('_')}
        log.debug(f'MODEL_KWARGS: {model_kwargs}')
        self.model = CNNTextClassifier(params=HYPERPARAMS, **model_kwargs)

    def train(self):

        self.trainset_mapper = DatasetMapper(self.x_train, self.y_train)
        self.testset_mapper = DatasetMapper(self.x_test, self.y_test)

        self.loader_train = DataLoader(self.trainset_mapper, batch_size=self.batch_size)
        self.loader_test = DataLoader(self.testset_mapper, batch_size=self.batch_size)

        optimizer = optim.RMSprop(self.model.parameters(), lr=self.learning_rate)

        for epoch in range(self.epochs):
            self.model.train()
            predictions = []
            for x_batch, y_batch in self.loader_train:
                y_batch = y_batch.type(torch.FloatTensor)
                y_pred = self.model(x_batch)
                loss = F.binary_cross_entropy(y_pred, y_batch)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                # Save predictions
                predictions += list(y_pred.detach().numpy())

            test_predictions = self.predict()
            train_accuary = calculate_accuracy(self.y_train, predictions)
            test_accuracy = calculate_accuracy(self.y_test, test_predictions)
            print("Epoch: %d, loss: %.5f, Train accuracy: %.5f, Test accuracy: %.5f" % (epoch + 1, loss.item(), train_accuary, test_accuracy))
        return self

    def predict(self, X=None):

        self.model.eval()  # evaluation mode
        predictions = []

        if X is not None:
            X_batches = zip(X, [None] * len(X))
        else:
            X_batches = list(zip(*self.loader_test))[0]
        with torch.no_grad():
            for x_batch in X_batches:
                y_pred = self.model(x_batch)
                predictions += list(y_pred.detach().numpy())

        return predictions

    def score(self, X, y):
        y_pred = self.predict(X)
        return torch.Tensor.mean((y_pred - y)**2) ** .5


def parse_argv(sys_argv=sys.argv):
    argv = list(reversed(sys_argv[1:]))

    pipeline_args = []
    pipeline_kwargs = dict(tokenizer='tokenize_re')
    while len(argv):
        a = argv.pop()
        if a.startswith('--'):
            if '=' in a:
                k, v = a.split('=')
                k = k.lstrip('-')
            else:
                k = a.lstrip('-')
                v = argv.pop()
            pipeline_kwargs[k] = v
        else:
            pipeline_args.append(a)

    return pipeline_args, pipeline_kwargs


def main():

    pipeline_args, pipeline_kwargs = parse_argv(sys.argv)

    log.warning(f'args: {pipeline_args}')
    log.warning(f'kwargs: {pipeline_kwargs}')

    pipeline = Pipeline(*pipeline_args, **pipeline_kwargs)

    pipeline = pipeline.train()
    predictions = pipeline.predict()

    return dict(pipeline=pipeline, predictions=predictions)


if __name__ == '__main__':
    import json
    results = main()
    json.dump(
        [float(x) for x in results['predictions']],
        open('predictions.json', 'a'), indent=2)
