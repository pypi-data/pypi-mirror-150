import logging
import math
import numpy as np
import torch
import torch.nn as nn

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


class CNNTextClassifier(nn.ModuleList):

    def __init__(self, params=None, **kwargs):
        self.random_state = kwargs.pop('random_state', None)
        if self.random_state is not None:
            self.torch_random_state = self.random_state
            self.numpy_random_state = self.random_state + 1
        if params.torch_random_state is None:
            self.torch_random_state = torch.random.initial_seed()
        else:
            self.torch_random_state = params.torch_random_state
        if params.numpy_random_state is None:
            self.numpy_random_state = np.random.get_state()[1][0]
        else:
            self.numpy_random_state = params.numpy_random_state

        torch.random.manual_seed(self.torch_random_state)
        np.random.seed(self.numpy_random_state)

        assert self.torch_random_state == torch.random.initial_seed()
        assert self.numpy_random_state == np.random.get_state()[1][0]

        log.warning("=" * 100)
        log.warning(f"torch_random_state={self.torch_random_state}")
        log.warning(f"numpy_random_state={self.numpy_random_state}")
        log.warning("=" * 100)

        super().__init__()

        self.convolvers = []
        self.poolers = []

        self.seq_len = params.seq_len
        self.vocab_size = params.vocab_size
        self.embedding_size = params.embedding_size
        self.kernel_lengths = list(params.kernel_lengths)

        self.stride = getattr(params, 'stride', 2)
        self.strides = getattr(params, 'strides')
        if not self.strides:
            self.strides = [self.stride] * len(self.kernel_lengths)
        if len(self.strides) < len(self.kernel_lengths):
            self.strides = list(self.strides) + [self.stride] * (len(self.kernel_lengths) - len(self.strids))

        self.dropout_portion = params.dropout_portion
        self.dropout = nn.Dropout(self.dropout_portion)

        self.conv_output_size = getattr(params, 'conv_output_size', 32)
        self.__dict__.update(kwargs)

        for param_name, param_val in vars(self).items():
            if param_name.startswith('_'):
                continue
            if param_name in kwargs:
                setattr(self, param_name, kwargs[param_name])
            log.info(f'MODEL: {param_name}: {getattr(self, param_name)} ({type(getattr(self, param_name))})')

        self.embedding = nn.Embedding(self.vocab_size + 1, self.embedding_size, padding_idx=0)

        # default: 4 CNN layers with max pooling
        for i, (kernel_len, stride) in enumerate(zip(self.kernel_lengths, self.strides)):
            self.convolvers.append(nn.Conv1d(self.seq_len, self.conv_output_size, kernel_len, stride))
            # setattr(self, f'conv_{i + 1}', self.convolvers[i])
            self.poolers.append(nn.MaxPool1d(kernel_len, stride))
            # setattr(self, f'pool_{i + 1}', self.poolers[i])

        self.encoding_size = self.cnn_output_size()
        self.linear_layer = nn.Linear(self.encoding_size, 1)

    def cnn_output_size(self):
        """ Calculate the number of encoding dimensions output from CNN layers

        Convolved_Features = ((embedding_size + (2 * padding) - dilation * (kernel - 1) - 1) / stride) + 1
        Pooled_Features = ((embedding_size + (2 * padding) - dilation * (kernel - 1) - 1) / stride) + 1

        source: https://pytorch.org/docs/stable/generated/torch.nn.Conv1d.html
        """
        out_pool_total = 0
        for kernel_len, stride in zip(self.kernel_lengths, self.strides):
            out_conv = ((self.embedding_size - 1 * (kernel_len - 1) - 1) / stride) + 1
            out_conv = math.floor(out_conv)
            out_pool = ((out_conv - 1 * (kernel_len - 1) - 1) / stride) + 1
            out_pool = math.floor(out_pool)
            out_pool_total += out_pool

        # Returns "flattened" vector (input for fully connected layer)
        return out_pool_total * self.conv_output_size

    def forward(self, x):
        """ Takes sequence of integers (token indices) and outputs binary class label """

        x = self.embedding(x)

        conv_outputs = []
        for (conv, pool) in zip(self.convolvers, self.poolers):
            z = conv(x)
            z = torch.relu(z)
            z = pool(z)
            conv_outputs.append(z)

        # The output of each convolutional layer is concatenated into a unique vector
        union = torch.cat(conv_outputs, 2)
        union = union.reshape(union.size(0), -1)

        # The "flattened" vector is passed through a fully connected layer
        out = self.linear_layer(union)
        # Dropout is applied
        out = self.dropout(out)
        # Activation function is applied
        out = torch.sigmoid(out)

        return out.squeeze()
