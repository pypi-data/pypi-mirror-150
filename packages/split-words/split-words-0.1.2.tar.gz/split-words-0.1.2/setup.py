# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['split_words']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'split-words',
    'version': '0.1.2',
    'description': 'Split German words',
    'long_description': '[![pytest](https://github.com/ffreemt/split-words/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/split-words/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.8%2B&color=blue)](https://www.python.org/downloads/)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![PyPI version](https://badge.fury.io/py/split-words.svg)](https://badge.fury.io/py/split-words)\n\n# split-words\n\n`CharSplit` repacked with `poetry`, published as `pypi` `split-words`--\nall credit goes to the original author.\n```\npip install split-words\n```\n```\n# replace charsplit with split_words in the following, e.g.\nfrom split_words import Splitter\n...\n```\n\n## CharSplit - An *ngram*-based compound splitter for German\n\nSplits a German compound into its body and head, e.g.\n> Autobahnraststätte -> Autobahn - Raststätte\n\nImplementation of the method decribed in the appendix of the thesis:\n\nTuggener, Don (2016). *Incremental Coreference Resolution for German.* University of Zurich, Faculty of Arts.\n\n**TL;DR**: The method calculates probabilities of ngrams occurring at the beginning, end and in the middle of words and identifies the most likely position for a split.\n\nThe method achieves ~95% accuracy for head detection on the [Germanet compound test set](http://www.sfs.uni-tuebingen.de/lsd/compounds.shtml).\n\nA model is provided, trained on 1 Mio. German nouns from Wikipedia.\n\n### Usage ###\n**Train** a new model:\n```bash\ntraining.py --input_file --output_file\n```\nfrom command line, where `input_file` contains one word (noun) per line and `output_file` is a json file with computed n-gram probabilities.\n\n**Compound splitting**\n\nIn python\n\n```python\n>> from charsplit import Splitter\n>> splitter = Splitter()\n>> splitter.split_compound("Autobahnraststätte")\n```\nreturns a list of all possible splits, ranked by their score, e.g.\n```python\n[(0.7945872450631273, \'Autobahn\', \'Raststätte\'),\n(-0.7143290887876655, \'Auto\', \'Bahnraststätte\'),\n(-1.1132332878581173, \'Autobahnrast\', \'Stätte\'), ...]\n```\nBy default, `Splitter` uses the data from the file `charsplit/ngram_probs.json`. If you retrained the model, you may specify a custom file with\n```python\n>> splitter = Splitter(ngram_path=<json_data_file_with_ngram_probs>)\n```\n\n',
    'author': 'Refer to CharSplit repo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/split-words',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8.3,<4.0.0',
}


setup(**setup_kwargs)
