from datetime import datetime
import time


class StatLog(object):

    """
    StatLog is a logger used for stats.
    """

    def __init__(
        self, experiment_id, experiment_dir, time_track, stats_track, freeze=False
    ):
        self.experiment_id = experiment_id
        self.experiment_dir = experiment_dir
        self.time_track = ["time", "time_elapsed", "num_updates"] + time_track
        self.stats_track = stats_track
        self.start_time = time.time()
        self.time_tracked = {k: [] for k in self.time_track}
        self.stats_tracked = {k: [] for k in self.stats_track}
        self.counter = 0
        self.freeze = freeze

    def update(self, time_stats_dict, stats_dict):
        """
        Updates time and stats.

        :param time_stats_dict: Time columns
        :param stats_dict: Stats columns
        """

        # freeze and check
        if self.freeze:
            for k in self.time_track[3:]:
                assert k in time_stats_dict.keys(), f"{k} not in time_stats_dict"
            for k in self.stats_track:
                assert k in time_stats_dict.keys(), f"{k} not in stats_dict"
        else:
            self.counter += 1
            # update time values
            time_stats_dict["time"] = datetime.today().strftime("%H:%M:%S")
            time_stats_dict["time_elapsed"] = time.time() - self.start_time
            time_stats_dict["num_updates"] = self.counter

            # update stats which user has passed
            for k in time_stats_dict.keys():
                if k in self.time_track:
                    self.time_tracked[k].append(time_stats_dict[k])
                else:
                    self.time_track.append(k)
                    self.time_tracked[k] = [time_stats_dict[k]]

            for k in stats_dict.keys():
                if k in self.stats_track:
                    self.stats_tracked[k].append(stats_dict[k])
                else:
                    self.stats_track.append(k)
                    self.stats_tracked[k] = [stats_dict[k]]

            return time_stats_dict, stats_dict
