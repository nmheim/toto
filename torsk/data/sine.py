import numpy as np
import torch
from torch.utils.data import Dataset
from torsk.data.utils import normalize, split_train_label_pred


def _make_sine(periods=30, N=20):
    dx = 2 * np.pi / (N + 1)
    x = np.linspace(0, 2 * np.pi - dx, N)
    y = np.sin(x)
    y = np.tile(y, periods)
    return y


class SineDataset(Dataset):
    """Creates a simple sine dataset.

    Parameters
    ----------
    train_length : int
        length of the training inputs/labels sequences
    pred_length : int
        length of the prediction label sequence
    periods : int
        total number of training periods
    points_per_period : int
        number of points within (0, 2pi)

    Returns
    -------
    inputs : torch.Tensor
        sequence of shape (train_length, 1)
    labels : torch.Tensor
        sequence of shape (train_length, 1)
    pred_labels : torch.Tensor
        sequence of shape (pred_length, 1) that starts right after the end of
        the labels sequence.
    """
    def __init__(self, train_length, pred_length,
                 periods=100, points_per_period=40):
        self.train_length = train_length
        self.pred_length = pred_length
        self.nr_sequences = periods * points_per_period \
            - self.train_length - self.pred_length

        self.seq = normalize(_make_sine(N=points_per_period, periods=periods))
        self.seq = self.seq.reshape((-1, 1))

    def __getitem__(self, index):
        if (index < 0) or (index >= self.nr_sequences):
            raise IndexError('MackeyDataset index out of range.')
        sub_seq = self.seq[index:index + self.train_length + self.pred_length + 1]
        inputs, labels, pred_labels = split_train_label_pred(
            sub_seq, self.train_length, self.pred_length)
        inputs = torch.Tensor(inputs)
        labels = torch.Tensor(labels)
        pred_labels = torch.Tensor(pred_labels)
        return inputs, labels, pred_labels, torch.Tensor([[0]])

    def __len__(self):
        return self.nr_sequences


if __name__ == "__main__":

    ds = SineDataset(100, 100)
    inputs, labels, pred_labels = ds[0]

    import matplotlib.pyplot as plt
    plt.plot(inputs.numpy())
    plt.plot(labels.numpy())
    plt.plot(np.arange(100, 200), pred_labels.numpy())
    plt.show()
