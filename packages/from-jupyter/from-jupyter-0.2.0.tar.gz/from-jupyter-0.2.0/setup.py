# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['from_jupyter']

package_data = \
{'': ['*']}

install_requires = \
['Pygments>=2.12.0,<3.0.0',
 'imgkit>=1.2.2,<2.0.0',
 'jupytext>=1.13.8,<2.0.0',
 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['from-jupyter = from_jupyter.__main__:cli']}

setup_kwargs = {
    'name': 'from-jupyter',
    'version': '0.2.0',
    'description': 'Blogging from Jupyter notebooks',
    'long_description': '(Blogging) from Jupyter\n=======================\n\n## Installation\n\nThis package is compatible with Python 3.8 and higher\n\n```shell\npip install from-jupyter\n```\n\nIf you want to be able to export data frames to images, it is also necessary to install [wkhtmltopdf](https://wkhtmltopdf.org/):\n\n```shell\n# Debian\nsudo apt-get install wkhtmltopdf\n# MacOS with brew\nbrew install --cask wkhtmltopdf\n```\n\n## Usage\n\n*from-jupyter* relies heavily on cell metadata, whenever you want to export a cell, you probably need to add metadata\nto make sure the export happens as you want.\n\n### Exporting images\n\nGiven a code cell that produces a *matplotlib* plot:\n\n```python\nimport matplotlib.pyplot as plt\n\nplt.plot(1, 2, 3)\n```\n\nIt is necessary to add the `"image"` key to the metadata, the value should be the name you want the plot to have when\nexported to the local file system.\n\n![Set image metadata](https://ik.imagekit.io/thatcsharpguy/posts/from-jupyter/image-export.gif?ik-sdk-version=javascript-1.4.3&updatedAt=1652333071909)\n\nThe command below will output the plot to the path `output/showcase/my-first-plot.png`:\n\n```shell\nfrom-jupyter images showcase.ipynb\n```\n\nThe output:\n\n![my-first-plot.png](https://ik.imagekit.io/thatcsharpguy/posts/from-jupyter/my-first-plot.png?ik-sdk-version=javascript-1.4.3&updatedAt=1652334258025)\n\n### Exporting *pandas* data frames\n\nGiven a cell that outputs a *pandas* data frame as a table:\n\n```python\nimport pandas as pd\n\nmy_frame = pd.DataFrame([\n    (1, 2),\n    (3, 4),\n    (5, 6),\n], columns=["column 1", "column 2"])\n\nmy_frame.head()\n```\n\nIt is necessary to add the `"dataframe"` key to the metadata, the value should be the name you want the exported\ndataframe to have in the local file system.\n\n![Set dataframe metadata](https://ik.imagekit.io/thatcsharpguy/posts/from-jupyter/my-dataframe.gif?ik-sdk-version=javascript-1.4.3&updatedAt=1652334019004)\n\nThe command below will generate the dataframe as image located in `output/showcase/my-dataframe.png`:\n\n```shell\nfrom-jupyter frames showcase.ipynb\n```\n\nThe output:\n\n![my-dataframe.png](https://ik.imagekit.io/thatcsharpguy/posts/from-jupyter/my-dataframe.png?ik-sdk-version=javascript-1.4.3&updatedAt=1652334258980)\n\n### Exporting code\n\nAny code cell can also be exported to an independent code file, to do this, it is necessary to add the "gist" key to the\ncell, with the value being the name of the file you want to take.\n\nTo export them to the output folder, one needs to use:\n\n```shell\nfrom-jupyter code showcase.ipynb\n```\n\n## Similar projects\n\n - [IPyPublish](https://github.com/chrisjsewell/ipypublish)\n - [Jupyter Book](https://github.com/executablebooks/jupyter-book)\n ',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fferegrino/from-jupyter',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
