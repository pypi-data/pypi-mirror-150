# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skyline',
 'skyline.analysis',
 'skyline.commands',
 'skyline.config',
 'skyline.data',
 'skyline.io',
 'skyline.models',
 'skyline.profiler',
 'skyline.protocol',
 'skyline.protocol_gen',
 'skyline.tests',
 'skyline.tracking',
 'skyline.tracking.memory',
 'skyline.tracking.time']

package_data = \
{'': ['*']}

install_requires = \
['numpy',
 'nvidia-ml-py3',
 'protobuf',
 'pyyaml',
 'toml>=0.10.2,<0.11.0',
 'torch']

entry_points = \
{'console_scripts': ['skyline = skyline.skyline:main']}

setup_kwargs = {
    'name': 'skyline-profiler',
    'version': '0.10.8',
    'description': 'Interactive performance profiling and debugging tool for PyTorch neural networks.',
    'long_description': '![Skyline](https://raw.githubusercontent.com/skylineprof/skyline/master/assets/skyline-wordmark.png)\n[![License](https://img.shields.io/badge/license-Apache--2.0-green?style=flat)](https://github.com/UofT-EcoSystem/skyline/blob/main/LICENSE)\n\nSkyline is a tool to profile and debug the training performance of [PyTorch](https://pytorch.org) neural networks.\n\n- [Installation](#installation)\n- [Usage example](#getting-started)\n- [Development Environment Setup](#dev-setup)\n- [Release Process](#release-process)\n- [Release History](#release-history)\n- [Meta](#meta)\n- [Contributing](#contributing)\n\n<h2 id="installation">Installation</h2>\n\nSkyline works with *GPU-based* neural networks that are implemented in [PyTorch](https://pytorch.org).\n\nTo run Skyline, you need:\n- A system equipped with an NVIDIA GPU\n- PyTorch 1.1.0+\n- Python 3.6+ or Python 3.7+ on OSX\n- [Poetry](https://python-poetry.org/)\n\n### Installation from source\n```zsh\ngit clone https://github.com/skylineprof/skyline.git\ncd skyline\npoetry install\npoetry run skyline --help\n```\n\n### Installation from PyPi\n\n**Note:** Not implemented yet\n\nInstalling with [Poetry](https://python-poetry.org/)\n```zsh\npoetry add skyline-profiler\npoetry run skyline --help\n```\n\nInstalling with [Pipenv](https://pipenv.pypa.io/en/latest/)\n```zsh\npipenv install skyline-profiler\npipenv run skyline --help\n```\n\nInstalling with [Pip](https://packaging.python.org/en/latest/tutorials/installing-packages/#use-pip-for-installing)\n```zsh\npython3 -m pip install skyline-profiler\npython3 skyline\n```\n\n<h2 id="getting-started">Usage example</h2>\n\nTo use Skyline in your project, you need to first write an entry point file, which is a regular Python file that describes how your model is created and trained. See the [Entry Point](https://github.com/UofT-EcoSystem/skyline/blob/main/docs/providers.md) for more information.\n\nOnce your entry point file is ready, there are two ways to profile interactive profiling and standalone profiling.\n\n### Interactive Profiling\n```zsh\npoetry run skyline interactive --skip-atom path/to/entry/point/file\n```\n\n### Standalone Profiling\nStandalone profiling is useful when you just want access to Skyline\'s profiling functionality. Skyline will save the profiling results (called a "report") into a [SQLite database file](https://www.sqlite.org/) that you can then query yourself. We describe the database schema for Skyline\'s run time and memory reports in the [Run Time Report Format](https://github.com/UofT-EcoSystem/skyline/blob/main/docs/run-time-report.md) and [Memory Report Format](https://github.com/UofT-EcoSystem/skyline/blob/main/docs/memory-report.md) pages respectively.\n\nTo have Skyline perform run time profiling, you use the `skyline time`\nsubcommand. In addition to the entry point file, you also need to specify the\nfile where you want Skyline to save the run time profiling report using the\n`--output` or `-o` flag.\n\n```zsh\npoetry run skyline time entry_point.py --output my_output_file.sqlite\n```\n\nLaunching memory profiling is almost the same as launching run time profiling.\nYou just need to use `skyline memory` instead of `skyline time`.\n\n```zsh\npoetry run skyline memory entry_point.py --output my_output_file.sqlite\n```\n\n<h2 id="dev-setup">Development Environment Setup</h2>\n\nFrom the project root, do\n```zsh\npoetry install\n```\n<h2 id="release-process">Release Process</h2>\n\n1. Make sure you\'re on main branch and it is clean\n1. Run [tools/prepare-release.sh](tools/prepare-release.sh) which will:\n    * Increment the version\n    * Create a release branch\n    * Create a release PR\n1. After the PR is merged [build-and-publish-new-version.yml](.github/workflows/build-and-publish-new-version.yml) GitHub action will:\n    * build the Python Wheels\n    * GitHub release\n    * Try to publish to Test PyPI\n    * Subject to approval publish to PyPI\n\n<h2 id="release-history">Release History</h2>\n\nSee [Releases](https://github.com/UofT-EcoSystem/skyline/releases)\n\n<h2 id="meta">Meta</h2>\n\nSkyline began as a research project at the [University of Toronto](https://web.cs.toronto.edu) in collaboration with [Geofrey Yu](mailto:gxyu@cs.toronto.edu), [Tovi Grossman](https://www.tovigrossman.com) and [Gennady Pekhimenko](https://www.cs.toronto.edu/~pekhimenko/).\n\nThe accompanying research paper appears in the proceedings of UIST\'20. If you are interested, you can read a preprint of the paper [here](https://arxiv.org/pdf/2008.06798.pdf).\n\nIf you use Skyline in your research, please consider citing our paper:\n\n```bibtex\n@inproceedings{skyline-yu20,\n  title = {{Skyline: Interactive In-Editor Computational Performance Profiling\n    for Deep Neural Network Training}},\n  author = {Yu, Geoffrey X. and Grossman, Tovi and Pekhimenko, Gennady},\n  booktitle = {{Proceedings of the 33rd ACM Symposium on User Interface\n    Software and Technology (UIST\'20)}},\n  year = {2020},\n}\n```\n\nIt is distributed under Apache 2.0 license. See [LICENSE](https://github.com/UofT-EcoSystem/skyline/blob/main/LICENSE) and [NOTICE](https://github.com/UofT-EcoSystem/skyline/blob/main/NOTICE) for more information.\n\n<h2 id="contributing">Contributing</h2>\n\nCheck out [CONTRIBUTING.md](https://github.com/UofT-EcoSystem/skyline/blob/main/CONTRIBUTING.md) for more information on how to help with Skyline.\n',
    'author': 'Geoffrey Yu',
    'author_email': 'gxyu@cs.toronto.edu',
    'maintainer': 'Akbar Nurlybayev',
    'maintainer_email': 'akbar.nur@gmail.com',
    'url': 'https://github.com/UofT-EcoSystem/skyline',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
