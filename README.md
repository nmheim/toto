# Torsk

An extended Echo State Network (ESN) for chaotic time series prediction and anomaly
detection.

This is a new implementation of the framework used in my [thesis](https://github.com/nmheim/thesis).
If you are looking for the legacy `torsk` that was used there you 
can find it [here](https://github.com/nmheim/torsk_archived).
In addition to a randomly initialized input matrix this implementation makes it
possible to use convolutions, discrete fourier transforms, and gradients of images
as inputs to the ESN.


## Prediction Examples

For a demonstration of the predictive power of the extended ESN check out
the next three links that compare ESN, LSTM, and cycle-based
of three different problems.

### Lissajous Figure

Prediction of a Gaussian blob that moves according to a [Lissajous figure](https://sid.erda.dk/share_redirect/eySGWidv4I) that is
defined by:

    x = sin(t)
    y = cos(0.3*t)

The true evolution of the time series is visible in the top left,
the ESN prediction in the top right, LSTM prediction lower left,
and the cycle-based prediction in the lower right.


### Mackey-Glass Lissajous

Prediction of a [chaotically moving Gaussian blob](https://sid.erda.dk/share_redirect/gkcHuk6xjR).
The trajectory of the maximum is governed by the Mackey-Glass time series in the x-dimension and a sine in the
y-dimension. The true evolution of the time series is visible in the top left,
the ESN prediction in the top right, LSTM prediction lower left,
and the cycle-based prediction in the lower right.


### Kuroshio

Prediction of the [Kuroshio](https://sid.erda.dk/share_redirect/fhkVWXAYBX) region
at the coast of Japan. Again: The true evolution of the time series is visible
in the top left, the ESN prediction in the top right, LSTM prediction lower
left, and the cycle-based prediction in the lower right.


## Usage

Running with `pip install -e .` installs the `torsk` package which comes with some
convenience scripts to inspect prediction outputs.
After running one of the experiments you can analyse the output files
with one of the commands listed by running `torsk --help`

## Change Backends (WIP)

Switching from Numpy to PyTorch (and soon to
[Bohrium](https://github.com/bh107/bohrium)!) backends can be done by using the
corresponding Numpy/Torch classes. An example usage
which makes it possible to run the prediction with different backends like
this:

    python experiments/chaotic_lissajous/conv_run.py backend torch dtype float32


## Tests

To run the tests, install `torsk` via `pip install -e ".[test]"`and run the
test by executing `pytest` in the main repo directory.
To see logging call during testing you can do:

    pytest --log-cli-level=INFO

To run the tests with flake8:

    pytest --flake8
