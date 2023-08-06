from tidyexp.tidyexp import Logger
import pytest


def test_setup_valid():
    """
    Test for validating logger setup.

    On passing all values to the setup, the log filename should be valid.
    """
    log = Logger("1", ".", ["num_epochs"], ["mse"], "torch")
    log.setup("1", ".", overwrite=False)
    assert log.log_fname == "./tidyexp_experiments/logs/log_1.hdf5"


def test_setup_invalid():
    """
    Test for validating logger setup with invalid args.

    On passing none values to the logger, Logger should raise a TypeError.
    """
    with pytest.raises(TypeError):
        _ = Logger("1", ".", None, None, "torch")
