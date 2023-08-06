# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tidyexp', 'tidyexp.load', 'tidyexp.save', 'tidyexp.utils']

package_data = \
{'': ['*']}

install_requires = \
['google-api-core==2.7.1',
 'google-api-python-client==2.43.0',
 'google-auth-httplib2==0.1.0',
 'google-auth-oauthlib>=0.5.1,<0.6.0',
 'google-auth==2.6.2',
 'googleapis-common-protos==1.56.0',
 'h5py==3.6.0',
 'pygit2==1.9.1',
 'pytest>=7.1.2,<8.0.0',
 'rich>=12.2.0,<13.0.0']

setup_kwargs = {
    'name': 'tidyexp',
    'version': '0.1.0',
    'description': 'Easy-to-use, offline-first ML experiment management solution.',
    'long_description': '# tidyexp\n\nEasy-to-use, offline-first ML experiment management solution.\n\n![PyPI - Downloads](https://img.shields.io/pypi/dm/tidyexp)\n![PyPI](https://img.shields.io/pypi/v/tidyexp)\n\n## What does it solve?\n\nOther competitors are complex in nature – they have a slight steep learning curve and aren’t often beginner-friendly. Some of them require you to create an account on their platform to get started.\n\ntidyexp aims to provide a free, easy-to-use platform for tracking ML experiment metadata.\n\n## Installation\n\nThrough `pip`:\n\n```\npip install tidyexp\n```\n\n## Usage\n\nImport tidyexp:\n\n```py\nimport tidyexp\n```\n\nCreate a Logger instance with the experiment metadata:\n\n```py\nlog = tidyexp.Logger(experiment_id="1", experiment_dir=".", time_track=["num_epochs"], stats_track=["mse"], overwrite=True, model_type="torch")\n```\n\nTrack experiment metadata in the training loop:\n\n```py\nfor i in range(epochs):\n    ....\n\n    time_dict = {"num_epochs": i}\n    stats_dict = {"mse": curr_loss}\n    log.update(time_dict, stats_dict)\n```\n\nSave logs:\n\n```py\nlog.save()\n```\n\nLoad logs:\n\n```py\nfrom tidyexp.load.load_log import load_log, load_stats, load_time\n\nlogs = load_log("abcd/logs/log_1.hdf5")\nstats = load_stats("abcd/logs/log_1.hdf5", "1")\ntime_stats = load_time("abcd/logs/log_1.hdf5", "1")\n```\n\nSave model:\n\n```py\nlog.save_model(model)\n```\n\nLoad model:\n\n```py\nfrom tidyexp.load.load_model import load_model\nckpt = load_model("abcd/models/final/final_1.pt", "torch")\n```\n\nCreate archive (`.zip`):\n\n```py\nlog.archive("archive")\n```\n\nUpload to Google Drive:\n\n```py\nlog.upload_gdrive("./credentials.json", "MyExperiment", "archive.zip")\n```\n\nPush to local Git repository:\n\n```py\nlog.commit("C:\\\\Users\\\\ExampleUser\\\\Experiments", ".\\abcd")\n```\n\n## License\n\ntidyexp is licensed under the MIT License.\n',
    'author': 'TidyExp Team',
    'author_email': '500076406@stu.upes.ac.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
