# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cassa']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0',
 'scikit-learn>=1.0.2,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

extras_require = \
{'progress': ['progress>=1.6,<2.0']}

setup_kwargs = {
    'name': 'cassa',
    'version': '2.1.1',
    'description': 'Python package to perform unsupervised and semi-supervised machine learning (ML) classification algorithms on generic tensors of pre-processed data',
    'long_description': "# Classification with Automated Semi-Supervised Algorithms (CASSA) package\n\n![test-main](https://github.com/giorgiosavastano/cassa/actions/workflows/python-test-main.yml/badge.svg)\n![coverage-main](https://img.shields.io/codecov/c/github/giorgiosavastano/cassa)\n![license](https://img.shields.io/github/license/giorgiosavastano/cassa)\n\n## Overview\n\n`CASSA` is a Python package to perform unsupervised and semi-supervised machine learning (ML) classification algorithms on generic tensors of pre-processed data, such as time series, altitude profiles, images, DDMs and spectra. Mainly tested on Earth Observation (EO) satellites data, such as GNSS-RO sTEC profiles and GNSS-R DDMs. It produces a database of labeled clusters that can be used to classify new unlabeled data.\nThe documentation is available at <https://cassa.readthedocs.io/en/latest/>.\n\nIt includes the following blocks:\n\n* Parallelized distance matrix computation using earth mover's distance (EMD, aka Wasserstein metric)\n* Spetral clustering using precomputed distance matrix\n* Self-tuned spectral clustering using precomputed distance matrix\n* HDBSCAN clustering using precomputed distance matrix\n* Classification of new data based on database of labeled clusters\n\n## Installation\n\n    pip install cassa\n\n\n### Authors\n\n- Giorgio Savastano (<giorgiosavastano@gmail.com>)\n- Karl Nordstrom (<karl.am.nordstrom@gmail.com>)\n\n## References\n\nSavastano, G., K. Nordström, and M. J. Angling (2022), Semi-supervised Classification of Lower-Ionospheric Perturbations using GNSS Radio Occultation Observations from Spire’s Cubesat Constellation. Submitt. to JSWSC.\n",
    'author': 'Karl Nordstrom',
    'author_email': 'karl.am.nordstrom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
