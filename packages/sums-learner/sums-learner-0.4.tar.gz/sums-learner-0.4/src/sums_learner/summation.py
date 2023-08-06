import functools
import time

import torch
from torch.nn import MSELoss
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

torch.manual_seed(42)
import numpy as np
from matplotlib import pyplot as plt

plt.style.use('fivethirtyeight')


# =====================================================================
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s: %(filename)s: %(lineno)s:\n%(message)s",
)
logger = logging.getLogger(__name__)

# =====================================================================

class DataSetter(Dataset):
    """
    DataSetter converts a dataset of two numpy arrays X & y to a pytorch Dataset object.
    INPUT
        X — numpy array
        y — numpy array
    """
    def __init__(self, X, y):
        self.X = torch.tensor(X).float()
        self.y = torch.tensor(y).float()

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class DataGena:
    """
    DataGena generates data for addition problem.
    INPUT
        sequence_length — number of signals [uniform[0, 1], {0, 1}] in a sequence
        size — number of signal-sequences in resulting data set
        batch_size — size of a batch, used in data loader
    """
    def __init__(
            self,
            sequence_length: int = 10,
            size: int = 100000,
            batch_size: int = 10,
            ) -> None:
        self.sequence_length = sequence_length
        self.size = size
        self.batch_size = batch_size

    def _get_random_signal(self):
        return np.random.uniform(
            low=0,
            high=1,
            size=(self.size,self.sequence_length),
            )

    def _get_mask_signal(self):
        ones_indices = self._get_random_signal().argsort(axis=1)[:, :2]
        mask_signal = np.zeros((self.size, self.sequence_length))
        np.put_along_axis(
            mask_signal,
            ones_indices,
            values=1,
            axis=1)
        return mask_signal

    @functools.cached_property
    def X(self):
        X = np.zeros((self.size, self.sequence_length, 2))
        random_signal = self._get_random_signal()
        mask_signal = self._get_mask_signal()
        X[:, :, 0] = random_signal
        X[:, :, 1] = mask_signal
        return X

    @functools.cached_property
    def y(self):
        return np.sum(
            self.X[:, :, 0] * self.X[:, :, 1],
            axis=1,
            ).reshape(-1, 1)

    @functools.cached_property
    def data_set(self):
        return DataSetter(
            X=self.X,
            y=self.y,
            )

    @functools.cached_property
    def data_generator(self):
        return DataLoader(
            self.data_set,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=2,
            )


class LSTM(torch.nn.Module):
    """
    LSTM creates an object for for training the LSTM RNN using pytorch.
    INPUT
        input_size — LSTM input size;
        it corresponds to the signal size of a problem [uniform[0, 1], {0, 1}]
        hidden_size — number of hidden LSTM neurons;
        it defaults to 100 based on the original paper
        output_size — predicted value;
        just 1 value is predicted (the sum of relevant signals)
        batch_size — size of a batch used in training; default is 10
        num_layers — number of layers in a network; only 1 is used
    """
    def __init__(
            self,
            input_size: int = 2,  # [uniform[0, 1], {0, 1}]
            hidden_size: int = 100,  # based on the original paper
            output_size: int = 1,  # just 1 value is predicted
            batch_size: int = 10,  # default batch size
            num_layers: int = 1,  # only using 1 layer
            ) -> None:
        super(LSTM, self).__init__()

        self.hidden_size = hidden_size
        self.batch_size = batch_size
        self.num_layers = num_layers

        self.lstm = torch.nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0,
            )

        self.linear = torch.nn.Linear(
            in_features = hidden_size,
            out_features = output_size)

    def forward(self, X):

        h_0 = torch.ones(
            self.num_layers, self.batch_size, self.hidden_size)
        c_0 = torch.ones(
            self.num_layers, self.batch_size, self.hidden_size)

        _, (h_out, _) = self.lstm(X, (h_0, c_0))

        h_out = h_out.view(-1, self.hidden_size)
        
        out = self.linear(h_out)

        return out


class SumsLearner:
    """
    SumsLearner learns to make a sum of relevant signals in a sequence of signals.
    INPUT
        sequence_length — length of a signal sequence; default is 10
        train_size — number of sequences in a training-set; default is 10 ** 5
        test_size — number of sequences in a test-set; default is 10 ** 5
        batch_size — size of a batch used in training; default is 10
        num_epochs — number of epochs to train for
        test — specifies whether to run run tests or not;
        it default to false becase it's time consuming
    """

    def __init__(
            self,
            sequence_length: int = 10,
            train_size: int = 10 ** 5,
            test_size: int = 10 ** 4,
            val_size: int = 10 ** 4,
            batch_size: int = 10,
            num_epochs: int = 10,
            test: bool = False,
            ) -> None:
        self.sequence_length = sequence_length
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.test = test

        self.sampling_period = train_size * num_epochs / (100 * batch_size)
        self.train_mse_by_batch = []
        self.val_mse_by_batch = []
        self.test_mse = []
        self.training_time = None
        self.min_num_batches = None

        train_generator = DataGena(
            sequence_length=sequence_length,
            size=train_size,
            batch_size=batch_size,
            )
        self.train_generator = train_generator.data_generator

        test_generator = DataGena(
            sequence_length=sequence_length,
            size=test_size,
            batch_size=batch_size,
            )
        self.test_generator = test_generator.data_generator

        val_generator = DataGena(
            sequence_length=sequence_length,
            size=val_size,
            batch_size=batch_size,
            )
        self.val_generator = val_generator.data_generator

        self.model = LSTM(
            input_size=2,  # [uniform[0, 1], {0, 1}]
            hidden_size=100,  # fix to 100 based on the original paper
            output_size=1,  # 1 we just predict 1 value
            batch_size=batch_size,
            num_layers=1,
        )

        self.optimizer = torch.optim.SGD(
            self.model.parameters(),
            lr=0.01,
            )

    def train(self):
        # Loop over epochs
        mse = MSELoss()
        training_start = time.time()
        counter = 0
        for _ in range(self.num_epochs):
            # Training
            for (X_batch, y_batch) in tqdm(self.train_generator):

                self.optimizer.zero_grad()
                y_hat = self.model(X_batch)
                loss = mse(y_hat, y_batch)
                loss.backward()
                self.optimizer.step()
                self.train_mse_by_batch.append(loss.item())
                # Testing
                if self.test:
                    if counter % self.sampling_period == 0:
                        with torch.set_grad_enabled(False):
                            for X_batch, y_batch in self.val_generator:
                                y_hat = self.model(X_batch)
                                val_loss = mse(y_hat, y_batch)
                                self.val_mse_by_batch.append(val_loss.item())
                counter += 1
            if loss.item() < 0.005:
                self.min_num_batches = counter
                break
        training_end = time.time()
        self.training_time = training_end - training_start
        with torch.set_grad_enabled(False):
            for X_batch, y_batch in self.test_generator:
                y_hat = self.model(X_batch)
                test_loss_final = mse(y_hat, y_batch)
                self.test_mse.append(test_loss_final.item())
        return self


class Examiner:
    """
    Examiner collects & outputs statistics on the learing progress.
    INPUT
        sequence_length — length of a signal sequence; default is 10
        train_size — number of sequences in a training-set; default is 10 ** 5
        test_size — number of sequences in a test-set; default is 10 ** 5
        batch_size — size of a batch used in training; default is 10
        num_epochs — number of epochs to train for
        test — specifies whether to run run tests or not;
        it default to false becase it's time consuming
    """
    def __init__(
            self,
            sequence_length: int = 10,
            train_size: int = 10 ** 5,
            test_size: int = 10 ** 4,
            batch_size: int = 10,
            num_epochs: int = 10,
            test: bool = False,
            ) -> None:

        self.sequence_length = sequence_length
        self.test = test

        sums_learner = SumsLearner(
            sequence_length=sequence_length,
            train_size=train_size,
            test_size=test_size,
            batch_size=batch_size,
            num_epochs=num_epochs,
            test=self.test,
            )

        self.sampling_period = sums_learner.sampling_period
        sums_learner.train()

        self.train_mse_by_batch = sums_learner.train_mse_by_batch
        self.val_mse_by_batch = sums_learner.val_mse_by_batch
        self.test_mse = np.mean(sums_learner.test_mse)
        self.training_time = sums_learner.training_time
        self.min_num_batches = sums_learner.min_num_batches



    @functools.cached_property
    def mse_of_e(self):
        random_sums = DataGena(
            sequence_length=self.sequence_length,
            size=10 ** 4,).data_set.y
        e = torch.ones(random_sums.shape)
        mse = MSELoss()
        return mse(random_sums, e)

    def chart_the_progress(self):

        point_count = 100

        fig, ax = plt.subplots(figsize=(12, 6))

        train_mean_mse = np.mean(
            np.array(self.train_mse_by_batch).reshape(point_count, -1),
            axis=1)
        test_mean_mse = np.mean(
            np.array(self.val_mse_by_batch).reshape(point_count, -1),
            axis=1)

        ax.plot(
            np.arange(0, point_count) * self.sampling_period,
            train_mean_mse,
            linewidth=3,
            color="#e5ae38",
            label="train",
            )
        if self.test:
            ax.plot(
                np.arange(0, point_count) * self.sampling_period,
                test_mean_mse,
                linewidth=3,
                color="#008fd5",
                label="test",
                )

        ax.axhline(
            y=self.mse_of_e,
            color="#8b8b8b",
            linestyle="--",
            linewidth=2,
            )
        ax.set_ylabel("MSE")
        ax.set_xlabel("batches")
        ax.set_title(
            f"sums with {self.sequence_length} numbers"
            f"\ntest MSE {self.test_mse:.5f}"
            )
        ax.legend(loc="upper right")
        plt.show()
        return fig


class ExaminationBoard:
    """
    Examiner collects & outputs statistics on the learing progress.
    INPUT
        sequence_lengths — lengths of a signal sequences to be tested
        train_size — number of sequences in a training-set; default is 10 ** 5
        test_size — number of sequences in a test-set; default is 10 ** 5
        batch_size — size of a batch used in training; default is 10
        num_epochs — number of epochs to train for
        test — specifies whether to run run tests or not;
        it default to false becase it's time consuming
    """
    def __init__(
            self,
            sequence_lengths: list = [],
            train_size: int = 10 ** 5,
            test_size: int = 10 ** 4,
            batch_size: int = 10,
            num_epochs: int = 100,
            ) -> None:

        self.sequence_lengths = sequence_lengths
        self.train_size = train_size
        self.test_size = test_size
        self.batch_size = batch_size
        self.num_epochs = num_epochs

        self.min_nums_batches = []
        self.min_training_times = []
        self.min_mses_achieved = []

    def run(self):
        for sl in self.sequence_lengths:
            examiner = Examiner(
                sequence_length=sl,
                train_size=self.train_size,
                test_size=self.test_size,
                batch_size=self.batch_size,
                num_epochs=self.num_epochs,
                test=False,
                )

            self.min_nums_batches.append(examiner.min_num_batches)
            self.min_training_times.append(examiner.training_time)
            self.min_mses_achieved.append(examiner.test_mse)

        for i in range(len(self.sequence_lengths)):
            sl = self.sequence_lengths[i]
            min_num_batches = self.min_nums_batches[i]
            min_training_time = self.min_training_times[i]
            min_mse_achieved = self.min_mses_achieved[i]
            print(
                f"{sl} {min_num_batches:>7.0f} {min_training_time/60:>5.1f} {min_mse_achieved:>7.5f}"
                )
        return self
    def plot_batches_required(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.scatter(
            self.sequence_lengths,
            self.min_nums_batches,
            color="#e5ae38",
            )
        ax.set_ylabel("number of batched")
        ax.set_xlabel("sequence length")
        ax.set_title(
            f"batches required VS  signal-sequence length"
            )
        plt.show()
        return fig

    def training_time(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.scatter(
            self.sequence_lengths,
            np.array(self.min_training_times) / 60,
            color="#e5ae38",
            )
        ax.set_ylabel("training time (min)")
        ax.set_xlabel("sequence length")
        ax.set_title(
            f"training time VS  signal-sequence length"
            )
        plt.show()
        return fig