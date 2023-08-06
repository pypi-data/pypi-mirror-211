# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['databallpy',
 'databallpy.features',
 'databallpy.load_data',
 'databallpy.load_data.event_data',
 'databallpy.load_data.tracking_data',
 'databallpy.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'lxml>=4.9.2,<5.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas==2.0.1',
 'requests>=2.28.2,<3.0.0',
 'tqdm>=4.64.1,<5.0.0']

setup_kwargs = {
    'name': 'databallpy',
    'version': '0.3.1',
    'description': 'A package for loading, preprocessing, vizualising and synchronizing soccere event aand tracking data.',
    'long_description': '# databallpy\n\nA package for loading, preprocessing, vizualising and synchronizing soccer event- and tracking data.\n\nThis package is developed to create a standardized way to analyse soccer matches using both event- and tracking data. Other packages, like [kloppy](https://github.com/PySport/kloppy) and [floodlight](https://github.com/floodlight-sports/floodlight), already standardize the import of data sources. The current package goes a step further in combining different data streams from the same match. In this case, the `Match` object combines information from the event and tracking data.\n\n### Changelog for version 0.3.0\n\n- Added way to save Match objects, and to load saved Match objects\n- Fixed bug in opta event data, own goals are now parsed as seperate event type\n- Added parser for Inmotio tracking data\n- Added parser for Instat event data\n- Added quality checks for the data, raises warning if quality is not good enough\n\n### Planned changes\n\n- Adding different filters to filter the tracking data\n- Adding features to quantify pressure, ball possession, etc. (if you have any ideas/requests, please open an issue!)\n- Standardizing events in the event data\n- Adding expected passing and goals models\n\n## Installation\n\n```bash\n$ pip install databallpy\n```\n\n## Usage\n\nThe package is centered around the `Match` object. A `Match` has tracking data, event data metadata about the match.\nFor a more elaborate example, see the [example file](https://databallpy.readthedocs.io/en/latest/example.html)\n\n```console\n$ from databallpy import get_match, get_open_match\n$\n$ match = get_match(\n$   tracking_data_loc="../data/tracking_data.dat",\n$   tracking_metadata_loc="../data/tracking_metadata.xml",\n$   tracking_data_provider="tracab"\n$   event_data_loc="../data/event_data_f24.xml",\n$   event_metadata_loc="../data/event_metadata_f7.xml",\n$   event_data_provider="opta",\n$ )\n$\n$ # or to load an open metrica dataset of tracking and event data\n$ match = get_open_match()\n$\n$ match.home_team_name # the team name of the home playing team\n$ match.away_players # pandas dataframe with the names, ids, shirt numbers and positions of the away team\n$ match.tracking_data # pandas dataframe with tracking data of the match\n$ match.event_data # pandas dataframe with event data of the match\n```\n\nSee [the documentation](https://databallpy.readthedocs.io/en/latest/autoapi/databallpy/match/index.html) of the `Match` object and the [example usage](https://databallpy.readthedocs.io/en/latest/example.html) for more options. Note that this package is developed to combine event and tracking data, for now both datastreams are necessary to create a `Match` object.\n\n## Synchronization of tracking and event data\n\nTracking and event data is often poorly synchronized. For instance, when taking the event data of Opta and tracking data of Tracab, you can sync the fist frame with the kick-off pass. Now you can sync the other events with the tracking data based on the time difference between the event and the kick off pass. If you do this, how get something like this:\n\n<video width="640" height="480" controls>\n  <source src="https://raw.githubusercontent.com/Alek050/databallpy/main/docs/example_data/not_synced.mp4" type="video/mp4">\n  Your browser does not support the video tag.\n</video>\n\nhttps://user-images.githubusercontent.com/49450063/224564808-fa71735f-5510-464d-8499-9044227a02e8.mp4\n\n\nAs you can see, the timing (and placing) of the events do not correspond good with the tracking data locations, especially when events follow up quickly or around shots. Using the methodology of [this](https://kwiatkowski.io/sync.soccer) article, this package is able to synchronize tracking and event data using the Needleman-Wunsch algorithm. \n\nAfter running the following command, the events are better synchronized to the tracking data:\n\n```batch\n$ match.synchronise_tracking_and_event_data()\n```\n\n<video width="640" height="480" controls>\n  <source src="https://raw.githubusercontent.com/Alek050/databallpy/main/docs/example_data/synced.mp4" type="video/mp4">\n  Your browser does not support the video tag.\n</video>\n\n\nhttps://user-images.githubusercontent.com/49450063/224564913-4091faf7-f6ef-4429-b132-7f93ce5e1d91.mp4\n\n\n## Documentation\n\nThe official documentation can be found [here](https://databallpy.readthedocs.io/en/latest/autoapi/databallpy/index.html).\n\n## Providers\n\nFor now we limited providers. We are planning on adding more providers later on.\n\nEvent data providers:\n- Opta\n- Metrica\n- Instat\n\nTracking data providers:\n- Tracab\n- Metrica\n- Inmotio\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n#### Maintainers & owners\n\n- [Alek050](https://github.com/Alek050/)\n- [DaanGro](https://github.com/DaanGro/)\n\n#### Contributors\n\n- [rdghe](https://github.com/rdghe/)\n\n## License\n\n`databallpy` was created by Alexander Oonk & Daan Grob. It is licensed under the terms of the MIT license.\n\n## Similar projects\n\nAlthough we think this package helps when starting to analyse soccer data, other packages may be better suited for your specific needs. Make sure to check out the following packages as well:\n- [kloppy](https://github.com/PySport/kloppy)\n- [floodlight](https://github.com/floodlight-sports/floodlight)\n- [codeball](https://github.com/metrica-sports/codeball)\n\nAnd for a more specific toturials on how to get started with soccer data"\n- [Friends of Tracking](https://github.com/Friends-of-Tracking-Data-FoTD)\n\n\n\n',
    'author': 'Alexander Oonk',
    'author_email': 'alexanderoonk26@gmail.com',
    'maintainer': 'Alexander Oonk',
    'maintainer_email': 'alexanderoonk26@gmail.com',
    'url': 'https://pypi.org/project/databallpy/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
