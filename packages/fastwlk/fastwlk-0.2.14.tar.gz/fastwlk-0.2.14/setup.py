# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastwlk', 'fastwlk.utils']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.0,<2.0.0',
 'networkx>=2.6.3,<3.0.0',
 'numpy>=1.22.1,<2.0.0',
 'tqdm>=4.62.3,<5.0.0']

setup_kwargs = {
    'name': 'fastwlk',
    'version': '0.2.14',
    'description': 'fastwlk is a Python package that implements a fast version of the Weisfeiler-Lehman kernel.',
    'long_description': "=============================\nFastWLK\n=============================\n\n.. image:: https://github.com/pjhartout/fastwlk/actions/workflows/main.yml/badge.svg\n        :target: https://github.com/pjhartout/fastwlk/\n\n\n.. image:: https://img.shields.io/pypi/v/fastwlk.svg\n        :target: https://pypi.python.org/pypi/fastwlk\n\n\n.. image:: https://codecov.io/gh/pjhartout/fastwlk/branch/main/graph/badge.svg?token=U054MJONED\n      :target: https://codecov.io/gh/pjhartout/fastwlk\n\n.. image:: https://img.shields.io/website-up-down-green-red/http/shields.io.svg\n   :target: https://pjhartout.github.io/fastwlk/\n\n\nQuick Links\n-------------------------\n`Documentation`_\n\n`Installation`_\n\n`Usage`_\n\n`Contributing`_\n\n\nWhat does ``fastwlk`` do?\n-------------------------\n\n\n``fastwlk`` is a Python package that implements a fast version of the\nWeisfeiler-Lehman kernel. It manages to outperform current state-of-the-art\nimplementations on sparse graphs by implementing a number of improvements\ncompared to vanilla implementations:\n\n1. It parallelizes the execution of Weisfeiler-Lehman hash computations since\n   each graph's hash can be computed independently prior to computing the\n   kernel.\n\n2. It parallelizes the computation of similarity of graphs in RKHS by computing\n   batches of the inner products independently.\n\n3. When comparing graphs, lots of computations are spent processing\n   positions/hashes that do not actually overlap between Weisfeiler-Lehman\n   histograms. As such, we manually loop over the overlapping keys,\n   outperforming numpy dot product-based implementations on collections of\n   sparse graphs.\n\nThis implementation works best when graphs have relatively few connections\ncompared to the number of possible connections and are reasonably dissimilar\nfrom one another. If you are not sure the graphs you are using are either sparse\nor dissimilar enough, try to benchmark this package with others out there using `this script`_.\n\nHow fast is ``fastwlk``?\n-------------------------\n\nRunning the benchmark script in ``examples/benchmark.py`` shows that for the\ngraphs in ``data/graphs.pkl``, we get an approximately 80% speed improvement\nover other implementations like `grakel`_. The example dataset contains 2-nn\ngraphs extracted from 100 random proteins from the human proteome from the\n`AlphaFold EBI database`_.\n\nTo see how much faster this implementation is for your use case:\n\n.. code-block:: console\n\n   $ git clone git://github.com/pjhartout/fastwlk\n   $ poetry install\n   $ poetry run python examples/benchmark.py\n\nYou will need to swap out the provided ``graphs.pkl`` with a pickled iterable of\ngraphs from the database you are interested in.\n\n.. _Documentation: https://pjhartout.github.io/fastwlk/\n.. _Installation: https://pjhartout.github.io/fastwlk/installation.html\n.. _Usage: https://pjhartout.github.io/fastwlk/usage.html\n.. _Contributing: https://pjhartout.github.io/fastwlk/contributing.html\n.. _grakel: https://github.com/ysig/GraKeL\n.. _AlphaFold EBI database: https://alphafold.ebi.ac.uk/download\n.. _this script: https://github.com/pjhartout/fastwlk/blob/main/examples/benchmark.py\n",
    'author': 'Philip Hartout',
    'author_email': 'philip.hartout@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
