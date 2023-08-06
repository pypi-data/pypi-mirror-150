import os
import shutil
from tidyexp.save.model_log import ModelLog
from tidyexp.save.stat_log import StatLog
from rich.console import Console
from .utils.helpers import (
    save_hdf5,
    print_update,
    print_about,
    upload_gdrive,
    commit,
    plot,
)


class Logger(object):
    """
    Logger for Tidyexp.
    """

    def __init__(
        self,
        experiment_id,
        experiment_dir,
        time_track,
        stats_track,
        model_type,
        overwrite=False,
    ):
        """
        Initializes experiment variables.

        :param experiment_id: Experiment ID
        :param experiment_dir: Experiment directory
        :param time_track: Time columns
        :param stats_track: Stats columns
        :param model_type: Model type
        :param overwrite (bool): Overwrite existing logs
        """
        self.experiment_dir = experiment_dir
        self.experiment_id = experiment_id
        self.time_track = time_track
        self.stats_track = stats_track
        self.overwrite = overwrite

        self.setup(experiment_id, experiment_dir, overwrite)
        print_about()
        self.stat_log = StatLog(
            self.experiment_id, self.experiment_dir, self.time_track, self.stats_track
        )
        self.model_log = ModelLog(self.experiment_id, self.experiment_dir, model_type)

    def setup(self, experiment_id, experiment_dir, overwrite):
        """
        Sets up experiment.

        :param experiment_id: Experiment ID
        :param experiment_dir: Experiment directory
        :param overwrite (bool): Overwrite existing logs
        """

        # prefix, etc?
        self.experiment_dir = os.path.join(experiment_dir, "tidyexp_experiments")

        self.log_fname = os.path.join(
            self.experiment_dir, "logs/", "log_" + experiment_id + ".hdf5"
        )

        if overwrite:
            if os.path.exists(self.log_fname):
                Console().log("⚠️ [Warning] Overwriting an existing log.")
                os.remove(self.log_fname)

    def update(self, time, stats, model=None, save=False):
        """
        Updates and prints stats to the console.

        :param time: Time values
        :param stats: Stats values
        :param model: Model
        :param save (bool): Save updates
        """

        # sanitize stats
        stats = {key: float(value) for (key, value) in stats.items()}

        time_dict, stats_dict = self.stat_log.update(time, stats)

        # save model
        if model is not None:
            self.save_model(model)

        # instead log.save() do direct save
        if save:
            self.save()

        # print updates
        print_update(
            ["time", "time_elapsed", "num_updates"],
            stats_dict.keys(),
            time_dict,
            stats_dict,
        )

    def save(self):
        """
        Save metadata, time and stats to a .hdf5 file.
        """

        metadata = [
            self.experiment_id + "/meta/logs",
            self.experiment_id + "/meta/experiment_dir",
        ]

        log_data = [
            [self.log_fname],
            [self.experiment_dir],
        ]

        # save metadata
        for i in range(len(metadata)):
            save_hdf5(self.log_fname, metadata[i], log_data[i])

        # save time stats
        for time_name in self.time_track:
            save_hdf5(
                self.log_fname,
                self.experiment_id + "/time/" + time_name,
                self.stat_log.time_tracked[time_name],
            )

        # save stats
        for stat_name in self.stats_track:
            save_hdf5(
                self.log_fname,
                self.experiment_id + "/stats/" + stat_name,
                self.stat_log.stats_tracked[stat_name],
            )

        # save model meta
        if self.model_log.model_counter > 0:
            save_hdf5(
                self.log_fname,
                self.experiment_id + "/meta/model_checkpoint",
                [self.model_log.final_model_dir],
            )

    def save_model(self, model):
        """
        Saves model using model log.

        :param model: Model
        """
        self.model_log.save(model)

    def archive(self, fname):
        """
        Creates an archive of the saved experiment data.

        :param fname: Filename of the archive
        """
        shutil.make_archive(fname, "zip", self.experiment_dir)

    def upload_gdrive(self, credential_path, folder_name, archive_name):
        """
        Uploads data to Google Drive.

        :param credential_path: Google Drive credentials
        :param folder_name: Folder name
        :param archive_name: Archive name/path
        """
        upload_gdrive(credential_path, folder_name, archive_name)

    def commit(self, git_path, folder_path):
        """
        Commits experiment data to a git repository.

        :param git_path: Git repo path
        :param folder_path: Folder path
        """
        commit(git_path, folder_path)

    def plot(self, x, y, return_fig=False, format_str="rx-"):
        """
        Returns a plot between time and stats.

        :param git_path: Git repo path
        :param folder_path: Folder path
        """

        return plot(
            self.stat_log.time_tracked,
            self.stat_log.stats_tracked,
            x,
            y,
            return_fig,
            format_str,
        )
