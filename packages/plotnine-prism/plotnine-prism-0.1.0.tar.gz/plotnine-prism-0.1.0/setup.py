# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotnine_prism']

package_data = \
{'': ['*'], 'plotnine_prism': ['schemes/*']}

install_requires = \
['diot>=0.1,<0.2', 'plotnine>=0.8,<0.9', 'rtoml>=0.8,<0.9']

setup_kwargs = {
    'name': 'plotnine-prism',
    'version': '0.1.0',
    'description': 'Prism themes for plotnine, inspired by ggprism',
    'long_description': '# plotnine-prism\n\nPrism themes for [plotnine][1], inspired by [ggprism][2].\n\n\n## Installation\n\n```\npip install -U plotnine-prism\n```\n\n## Documentation\n\n[https://pwwang.github.io/plotnine-prism][3]\n\n## Usage\n\nSee [this notebook][6] for the following example, and also [Getting started][4] for a quick overview of `plotnine_prism` features.\n\n```python\nfrom plotnine import *\nfrom plotnine_prism import *\n\nfrom datar.all import f, as_categorical, mutate\nfrom datar.datasets import ToothGrowth\n\nToothGrowth >>= mutate(dose=as_categorical(f.dose))\n\nbase = (\n    ggplot(ToothGrowth, aes(x = "dose", y = "len")) +\n    geom_violin(aes(colour = "dose", fill = "dose"), trim = False) +\n    geom_boxplot(aes(fill = "dose"), width = 0.2, colour = "black")\n)\n\np1 = base + ylim(-5, 40)\np2 = (\n    base +\n    scale_y_continuous(limits=[-5, 40], guide=guide_prism_offset_minor()) +\n    scale_color_prism(\'floral\') +\n    scale_fill_prism(\'floral\') +\n    theme_prism()\n)\n# See examples/nb_helpers.py for plot_grid function\n# plot_grid(p1, p2)\n```\n\n<table>\n    <tr>\n        <td valign="top"><img src="./toothgrowth1.png" /></td>\n        <td valign="top"><img src="./toothgrowth2.png" /></td>\n    </tr>\n</table>\n\n## More examples\n\nThe Dose Response Curve was recreated. See [this vignette][5] for the source code and step-by-step instructions.\n\n\n<table>\n    <tr>\n        <td valign="top"><img src="./dose1.png" /></td>\n        <td valign="top"><img src="./dose2.png" /></td>\n    </tr>\n</table>\n\n[1]: https://github.com/has2k1/plotnine\n[2]: https://github.com/csdaw/ggprism/\n[3]: https://pwwang.github.io/plotnine-prism\n[4]: https://pwwang.github.io/plotnine-prism/get_started\n[5]: https://pwwang.github.io/plotnine-prism/raw/ex1-dose\n[6]: https://pwwang.github.io/plotnine-prism/raw/README\n\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
