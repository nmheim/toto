import logging
import numpy as np

import torsk
from torsk.data.numpy_dataset import NumpyImageDataset as ImageDataset
from torsk.models.numpy_esn import NumpyESN as ESN
from torsk.data.utils import gauss2d_sequence


def test_lissajous(tmpdir):
    np.random.seed(0)

    params = torsk.default_params()
    params.input_map_specs = [
        {"type": "pixels", "size": [30, 30], "input_scale": 3.},
        {"type": "conv", "mode": "same", "size": [5, 5],
            "kernel_type":"gauss", "input_scale": 4.},
        {"type": "conv", "mode": "same", "size": [10, 10],
            "kernel_type":"gauss", "input_scale": 3.},
        {"type": "conv", "mode": "same", "size": [15, 15],
            "kernel_type":"gauss", "input_scale": 4.},
        {"type": "conv", "mode": "same", "size": [5, 5],
            "kernel_type":"random", "input_scale": 4.},
        {"type": "conv", "mode": "same", "size": [10, 10],
            "kernel_type":"random", "input_scale": 4.},
        {"type": "conv", "mode": "same", "size": [20, 20],
            "kernel_type":"random", "input_scale": 4.},
        {"type": "dct", "size": [15, 15], "input_scale": 1.},
        {"type": "gradient", "input_scale": 4.},
        {"type": "gradient", "input_scale": 4.}
    ]

    params.spectral_radius = 2.0
    params.density = 0.001
    params.input_shape = [30, 30]
    params.train_length = 1200
    params.pred_length = 300
    params.transient_length = 200
    params.dtype = "float64"
    params.reservoir_representation = "sparse"
    params.backend = "numpy"
    params.train_method = "pinv_svd"
    params.imed_loss = False
    params.tikhonov_beta = None
    params.debug = False

    logger = logging.getLogger(__name__)
    level = "DEBUG" if params.debug else "INFO"
    logging.basicConfig(level=level)
    logging.getLogger("matplotlib").setLevel("INFO")

    logger.info("Creating circle dataset ...")
    t = np.arange(0, 200 * np.pi, 0.02 * np.pi)
    x, y = np.sin(0.3 * t), np.cos(t)

    center = np.array([y, x]).T
    images = gauss2d_sequence(center, sigma=0.5, size=params.input_shape)
    dataset = ImageDataset(images, params, scale_images=True)

    logger.info("Building model ...")
    model = ESN(params)

    logger.info("Training + predicting ...")
    model, outputs, pred_labels = torsk.train_predict_esn(model, dataset)

    # logger.info("Visualizing results ...")
    # import matplotlib.pyplot as plt
    # from torsk.visualize import animate_double_imshow
    # anim = animate_double_imshow(pred_labels, outputs)
    # plt.show()

    error = np.abs(outputs - pred_labels)
    logger.info(error.mean())
    logger.info(error.max())
    assert error.mean() < 3e-4
    assert error.max() < 9e-3
