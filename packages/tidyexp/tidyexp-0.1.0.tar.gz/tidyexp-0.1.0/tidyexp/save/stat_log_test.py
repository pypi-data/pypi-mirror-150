from tidyexp.save.stat_log import StatLog
import pytest


def test_statlog_valid():
    """
    Test for validating StatLog setup and update.

    On passing key-value pairs to update, the local state should be modified.
    """
    log = StatLog("1", ".", ["num_epochs"], ["mse"])
    time_dict = {"num_epochs": 10}
    stats_dict = {"mse": 0.17}
    t_dict, s_dict = log.update(time_dict, stats_dict)

    assert t_dict["num_updates"] == 1
    assert s_dict["mse"] == 0.17


def test_statlog_invalid():
    """
    Test for validating StatLog setup with invalid args.

    On passing none values to the logger, StatLog should raise a TypeError.
    """
    with pytest.raises(TypeError):
        _ = StatLog("1", None, None, None)
