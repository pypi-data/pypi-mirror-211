# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['teda', 'teda.models', 'teda.painterShapes', 'teda.views', 'teda.widgets']

package_data = \
{'': ['*'], 'teda': ['icons/*']}

install_requires = \
['astropy>5.2.2',
 'matplotlib>=3.7.1,<4.0.0',
 'pyside6>=6.5.0,<7.0.0',
 'scipy>=1.10.1,<2.0.0',
 'traitlets>=5.9.0,<6.0.0']

entry_points = \
{'console_scripts': ['teda = teda.teda_fits:main']}

setup_kwargs = {
    'name': 'teda',
    'version': '3.1.0',
    'description': 'Yet Another FITS Viewer',
    'long_description': '# TeDa FITS Viewer\n\nObservatory optimized FITS Images viewer\n\n![](img/teda.png)\n\n## Key Features\n* Flexible windows and widgets layout\n* WCS support\n* Radial Profile with gaussoide fit (try `r`-key)\n* Scan mode: observes directory for changes and automatically opens new FITS\n* Integrated ipython console with direct access to data and application\n\n## Installation\n``` bash\n   pip install teda\n   teda_viewer \n``` \n### Optional dependencies\nTo use ipython console the `qtconsole` package is needed, additionally:\n``` bash\n    pip install qtconsole\n``` \nFor directory scanning functionality, the `watchdog` package should be installed, e.g. \n``` bash\n    pip install watchdog\n``` \n\n## Run\nThe installation scripts should install the command:\n```\n    teda_viewer\n```\nTry \n```\n    teda_viewer --help\n```\nfor list of command line parameters.\n\n## Dynamic Scale and Color\nThe dynamic scale of the image, and color mapping can be adjusted form \nthe **Dynamic Scale** panel. From menu: **View/Dynamic Scale**\n\n## Fits Header Cards Pinning\nOn the FITS Header panel, selected keys can be *pinned* to appear\non the top ot the list. This can be done via context (right-click) menu.\n\nThe set of pinned keys is saved and preserved between sessions.  \n\n## Radial Profile\nThe **Radial Profile** button turns on the mode of selecting targets for \nthe radial profile analysis. Make sure the radial profile panel is visible \n(View/Radial Profile). The shortcut for displaying radial profile of the star \nunder cursor is the **R**-key.\n\nThe centroid of the star is corrected within small (be precise!) radius\nusing the bivariate gaussoide fit.\n\nTogether with the pixels values, the radial profile presents 1D fit of\n"gaussian(r) + sky". This fit provides information of presented fwhm and sky level.\n   \n\n## Integrated Python Console\nIn order to use integrated python console the `qtconsole` module, and it\'s\ndependencies (jupyter related) have to be installed. This is not done by\ndefault `pip` installation to keep number of dependencies reasonably small.\nInstall `qtconsole` by:\n``` bash\n    pip install qtconsole\n``` \n\nThe console is available form menu **View/Python Console**\n### Predefined variables\nThe console has a number of predefined variables set:\n* `ax: WCSAxesSubplot` main plotting axes.\n* `window: MainWindow` main window\n* `data: numpy.ndarray` current HDU data\n* `header: astropy.fits.Header` current HDU header\n* `wcs: astropy.wcs.WCS` the WCS transformer\n\n### Plotting\nTo plot directly on the console, run the following magic command `%matplotlib inline`.\n\nWhen plotting on the main canvas, the result will appear after redrawing\nmain figure by `ax.figure.canvas.draw()`.\n\nThe example below, draws linear profile on the console and corresponding\nline on the main FITS display:    \n  \n``` python\n%matplotlib inline\nimport matplotlib.pyplot as plt\nax.plot([10,30], [10,10])\nax.figure.canvas.draw()\nplt.plot(data[10,10:30])\n```\n\n## Directory Scan\nThe **Scan Toolbar** (hidden by default) provides controls for the \ndirectory scanning mode.\n\nThis mode is intended to observe newly created FITS files in observatory.\n\nAfter pressing **Scan** button, and choosing directory, TeDa Fits Viewer will\nload most recent FITS file from that directory, and keep watching the directory \nfor changes. When new FITS file is added to directory, it will be loaded \nautomatically.\n\nUser can pause scanning using **Pause** button. There is also **auto pause** feature,\nwhen active, any mouse movement in the main area pauses scanning for 5 seconds,\navoiding FITS reload when working.\n\nAfter un-pausing (manually or after idle 5 seconds when auto-pause) the newest\nFITS will be loaded if any new files appeared during the pause.\n\nDirectory scanning needs the [`watchdog`](https://pypi.org/project/watchdog/) component to be \ninstalled manually (optional dependence).\n\n## Directory Panel\nThe Directory Panel can be shown using menu command **View-Directory view**.\n\nThe Directory Panel is convenient files navigator. The panel has two views:\n* Directory Tree\n* Files List\n\nUser can collapse any of them using divider handle and use only remaining one.\nIf the tree view is the only visible, it shows directories and files as well.      \n\n## Development version install\n``` bash\n\n    git clone https://github.com/majkelx/teda.git\n    cd teda\n    python -m venv venv\n    source ./venv/bin/activate\n    pip install -r requirements.txt\n    pip install -e .\n```\n\n## Bugs, remarks, greetings and contribution \nPlease use [GitHub issues tracker](https://github.com/majkelx/teda/issues) \nand [pull requests](https://github.com/majkelx/teda/pulls).\n\n\n@2020  [AkondLab](http://www.akond.com) for the [Araucaria Project](https://araucaria.camk.edu.pl).\n',
    'author': 'majkelx',
    'author_email': 'mkalusz@camk.edu.pl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
