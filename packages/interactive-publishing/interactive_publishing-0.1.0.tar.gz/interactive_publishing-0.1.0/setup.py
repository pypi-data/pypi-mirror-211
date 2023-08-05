# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ifigures']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0',
 'matplotlib>=3.6.2,<4.0.0',
 'pngquant>=1.0.7,<2.0.0',
 'pyvista>=0.39.1,<0.40.0']

setup_kwargs = {
    'name': 'interactive-publishing',
    'version': '0.1.0',
    'description': 'Templates and tools for creating interactive figures and interactive text for publishing in EPUB3/HTML5.',
    'long_description': "Interactive text and figures\n============================\n\nThis project provides quick starting point for anyone who wants to experiment\nwith **interactive text and figures** in their electronic publications\n(EPUB3 / HTML5 + JavaScript). One possible reason why one would use interactive\ntext and figures is to **communicate many possible stories** to the audience,\ninstead of usual single story line. See [Physics World blogpost](https://physicsworld.com/a/do-interactive-figures-help-physicists-to-communicate-their-science/).\n\nTwo templates and corresponding tools are provided.\nTools generate HTML/Javascript output that can be seen in\nweb-browsers and e-readers.\nGenerated examples don't have any external dependencies that need to be\ndownloaded from the Internet. They are completely self contained,\nand be seen on all devices (even without Internet access),\nand they can be simply included in interactive texts/books in EPUB3 format,\nas well as web-pages.\n\nFor quick overview what can be produced with templates check [HTML page of the\nproject](https://nikolasibalic.github.io/Interactive-Publishing/).\nAn example of EPUB3 eBook using interactive figures can be found\n[here](http://iopscience.iop.org/book/978-0-7503-1635-4/chapter/bk978-0-7503-1635-4ch1).\nAn example of physics blogpost incorporating interactive figures can be\nfound [here](https://piphase.wordpress.com/2019/01/26/youngs-double-slit-in-colour/).\n\n[![DOI](https://zenodo.org/badge/163100222.svg)](https://zenodo.org/badge/latestdoi/163100222)\n\nInteractive text\n----------------\n\nFor interactive text template see\n[```interactive_text.html```](interactive_text.html).\nTo ship your figure, provide to users .html file (with embedded JavaScript\ncalculations), together with TangleKit folder and Tangle.js accessible in\nroot folder of the figure .html.\n\nYou can start by changing text and calculation code in\n[```interactive_text.html```](interactive_text.html).\nExplore in-line documentation of [```TangleKit```](/TangleKit) for\nmore details.\n\n\n\nInteractive figures\n-------------------\n\nFor interactive figure example see\n[```interactive_figure.html```](interactive_figure.html). It is generated\nby the provided Python file\n```\npython interactive_figure_generator.py\n```\n\nYou can start building your own example by changing code in\n[```interactive_figure_generator.py ```](interactive_figure_generator.py),\nrunning Python to generate new\ninteractive figure, and observe results by realoading\n[```interactive_figure.html```](interactive_figure.html) in any web-browser.\n\n[```index.html```](index.html) containts source code of project web-page\nthat incorporates both examples.\n\nNote on implementation\n----------------------\nInteractive text example implements simple calculations in JavaScript. More\ncomplex calculations should be precalculated and provided as look-up tables.\n\nInteractive figures generate figures for all possible combinations of the\ninput. Control JavaScripts then displays just images corresponding to\nselected combination of input parameters, while all other images are hidden.\nThis can make files relatively large, but it allows their viewing on devices\nwith minimal computational resources, like ereaders, and old phones.\n\nLicense\n-------\nThis project uses [```TangleKit```](/TangleKit) package from this repository \nfor creating interactive text. That package is based on \non slightly modified and updated open-source\n[Tangle.js](http://worrydream.com/Tangle/)\nlibrary of [Bret Victor](http://worrydream.com/ExplorableExplanations/).\n\nInteractive figures use Matplotlib Python package and [```ifigures```](/ifigures)\npackage from this repository which is based\non updated and modified version of \n[ipywidgets-static](https://github.com/jakevdp/ipywidgets-static).\nCompared to original package, dependency on IPython is removed,\nPython 2 and 3 are supported now, and few bugs are fixed.\n\nLicenses are inherited from the original projects mentioned above.\nThey are permissive, and allow reuse, with or without modification, but for\ndetails check corresponding LICENSE files and code headers. Overal license\nis BSD-3-Clause.\n\n",
    'author': 'Nikola Sibalic',
    'author_email': 'nikolasibalic@physics.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
