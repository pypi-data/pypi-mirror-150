# tidyexp

Easy-to-use, offline-first ML experiment management solution.

![PyPI - Downloads](https://img.shields.io/pypi/dm/tidyexp)
![PyPI](https://img.shields.io/pypi/v/tidyexp)

## What does it solve?

Other competitors are complex in nature – they have a slight steep learning curve and aren’t often beginner-friendly. Some of them require you to create an account on their platform to get started.

tidyexp aims to provide a free, easy-to-use platform for tracking ML experiment metadata.

## Installation

Through `pip`:

```
pip install tidyexp
```

## Usage

Import tidyexp:

```py
import tidyexp
```

Create a Logger instance with the experiment metadata:

```py
log = tidyexp.Logger(experiment_id="1", experiment_dir=".", time_track=["num_epochs"], stats_track=["mse"], overwrite=True, model_type="torch")
```

Track experiment metadata in the training loop:

```py
for i in range(epochs):
    ....

    time_dict = {"num_epochs": i}
    stats_dict = {"mse": curr_loss}
    log.update(time_dict, stats_dict)
```

Save logs:

```py
log.save()
```

Load logs:

```py
from tidyexp.load.load_log import load_log, load_stats, load_time

logs = load_log("abcd/logs/log_1.hdf5")
stats = load_stats("abcd/logs/log_1.hdf5", "1")
time_stats = load_time("abcd/logs/log_1.hdf5", "1")
```

Save model:

```py
log.save_model(model)
```

Load model:

```py
from tidyexp.load.load_model import load_model
ckpt = load_model("abcd/models/final/final_1.pt", "torch")
```

Create archive (`.zip`):

```py
log.archive("archive")
```

Upload to Google Drive:

```py
log.upload_gdrive("./credentials.json", "MyExperiment", "archive.zip")
```

Push to local Git repository:

```py
log.commit("C:\\Users\\ExampleUser\\Experiments", ".\abcd")
```

## License

tidyexp is licensed under the MIT License.
