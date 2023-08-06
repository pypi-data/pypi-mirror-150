import os
import h5py


def load_meta(log_fname):
    """
    Load metadata and stats from a log file.

    :param log_fname: Log filename
    """

    # check if file exists before opening
    assert os.path.exists(log_fname), f"File {log_fname} doesn't exist"

    # open file in read mode
    hdf5 = h5py.File(log_fname, mode="r")

    # list runs
    runs = list(hdf5.keys())

    result = {key: [] for key in runs}

    # populate result dictionary
    for run in runs:
        data_sources = list(hdf5[run].keys())
        data_items = {source: list(hdf5[run][source].keys()) for source in data_sources}

        rn = hdf5[run]
        source_store = {key: [] for key in data_sources}

        for ds in data_items:
            data_store = {key: {} for key in data_items[ds]}
            for _, o_name in enumerate(data_items[ds]):
                data_store[o_name] = rn[ds][o_name][:]
            source_store[ds] = data_store

        # set result
        result[run] = source_store

    return result


def load_stats(experiment_dir, run, metric_name=""):
    """
    Loads stats-related experiment data from the logs.

    :param experiment_dir: Experiment directory or path
    :param run: Run ID (experiment ID)
    :param metric_name: (optional) Metric name
    """
    result = load_meta(experiment_dir)
    if metric_name != "":
        return result[run]["stats"][metric_name]
    return result[run]["stats"]


def load_time(experiment_dir, run, metric_name=""):
    """
    Loads time-related experiment data from the logs.

    :param experiment_dir: Experiment directory or path
    :param run: Run ID (experiment ID)
    :param metric_name: (optional) Metric name
    """
    result = load_meta(experiment_dir)
    if metric_name != "":
        return result[run]["time"][metric_name]
    return result[run]["time"]


def load_log(experiment_dir):
    """
    Loads logs from a directory or a path.

    :param experiment_dir: Experiment directory or path
    """
    if experiment_dir.endswith(".hdf5"):
        log_path = experiment_dir
        log = load_meta(log_path)
        return log
