# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asciiplot',
 'asciiplot._chart',
 'asciiplot._chart.grid',
 'asciiplot._chart.serialized',
 'asciiplot._chart.serialized.layout_element_adding',
 'asciiplot._utils']

package_data = \
{'': ['*']}

install_requires = \
['colored==1.4.2', 'dataclasses', 'more-itertools']

setup_kwargs = {
    'name': 'asciiplot',
    'version': '0.0.8',
    'description': 'Platform-agnostic, customizable sequence plotting in console, offering high suitability for GUIs',
    'long_description': "# __asciiplot__\n\n[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)\n[![Build](https://github.com/w2sv/asciiplot/actions/workflows/build.yaml/badge.svg)](https://github.com/w2sv/asciiplot/actions/workflows/build.yaml)\n[![codecov](https://codecov.io/gh/w2sv/asciiplot/branch/master/graph/badge.svg?token=69Q1VL8IHI)](https://codecov.io/gh/w2sv/asciiplot)\n![PyPI](https://img.shields.io/pypi/v/asciiplot)\n[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)\n#### Platform-agnostic sequence plotting in console, offering various chart appearance configuration options and thus giving rise to an increased degree of GUI suitability\n\n### Install\n```shell\n$ pip install asciiplot\n```\n\n### Plot configuration options\n\n- Setting of consistent margin between data points\n- Determination of chart height\n- Setting of chart title\n- Axes descriptions display\n- Setting of x-axis tick labels, possibly being of both numeric and string type\n- Determination of y-axis tick label decimal points\n- Centering the chart within the target terminal or indenting it by a passed number of columns respectively\n- Setting color of all chart components due to integration of [colored](https://pypi.org/project/colored/)\n\n### Examples\n\n```python\nfrom asciiplot import asciiize\n\nprint(\n    asciiize(\n        [1, 1, 2, 3, 5, 8, 13, 21],\n        \n        height=15,\n        inter_points_margin=7,\n\n        x_ticks=list(range(1, 9)),\n        y_ticks_decimal_places=0,\n\n        x_axis_description='Iteration',\n        y_axis_description='Value',\n\n        title='Fibonacci Sequence',\n        indentation=6\n    )\n)\n```\n\n                        Fibonacci Sequence\n     Value\n      21┤                                                     ╭──\n      19┤                                                    ╭╯\n      18┤                                                   ╭╯\n      16┤                                                  ╭╯\n      15┤                                                ╭─╯\n      13┤                                              ╭─╯\n      12┤                                            ╭─╯\n      11┤                                          ╭─╯\n       9┤                                        ╭─╯\n       8┤                                     ╭──╯\n       6┤                                 ╭───╯\n       5┤                             ╭───╯\n       3┤                       ╭─────╯\n       2┤             ╭─────────╯\n       1┼───────┬─────╯─┬───────┬───────┬───────┬───────┬───────┬ Iteration\n        1       2       3       4       5       6       7       8\n\n```python\nimport numpy as np\nfrom asciiplot import asciiize\n\nprint(\n    asciiize(\n        np.random.randint(-100, 100, 30),\n        np.random.randint(-100, 100, 30),\n        \n        height=10,\n        inter_points_margin=2,\n    \n        x_ticks=list(range(1, 31)),\n        y_ticks_decimal_places=1,\n    \n        title='Random Values',\n        indentation=6\n    )\n)\n```\n\n                                             Random Values\n        96.0┤        ╭╮    ╭──╭╮──╮               ╭──╮   ╭╮       ╭╮    ╭╮          ╭───────╮  ╭─╮\n        74.2┤  ╭╮    ││    │  ││  │               │  ╰╮ ╭╯│      ╭╯│   ╭╯╰╮        ╭╯──╯│   ╰╮╭╯ │\n        52.4┤ ╭╭╮╮  ╭╯╰╮  ╭╯ ╭╯│  ╰╮   ╭╮    ╭──╮╭╯   │╭╯ ╰╮   ╭─╯ ╰╮╭╮│  │       ╭╯│   │    ╰╯  ╰╮\n        30.7┤╭╯│╰╮╮╭╯  │  │  │ ╰╮  │   ││   ╭╯  ╰╯    ╰╯   │   │    ││││  ╰╮     ╭╯╭╯   ╰╮        │\n         8.9┼╯╭╯ │╰╯   │ ╭╯  │  │  │   ╭╮╮  │╭╮            ╰╮ ╭╯    ╭╯╰╮   │     │╭╯     │        │\n       -12.9┤╭╯  ╰╮    ╰╮│  ╭╯  │  │ ╭─╯╰╮╮╭╭╯│             │╭╯    ╭╯│││   ╭╮╮  ╭╯╯      │        ╰╮\n       -34.7┤│    │     ╭╮  │   ╰╮ ╰╭╯│  ╰╮╭╯ ╰╮     ╭───╮  ││    ╭╯ ╰╯╰╮ ╭╯│╰──│        ╰╮  ╭──╮ ╭│\n       -56.4┼╯    ╰─╮  ╭╯╰──╯    │ ╭╯╭╯   ││   ╰╮   ╭╯   ╰─╮╰╯  ╭─╯     ╰─╯ ╰╮ ╭╯         │ ╭╯  ╰─╯╰\n       -78.2┤       ╰──╯         │╭╯││    ╰╯    │ ╭─╯      ╰╮ ╭─╯            ╰╮│          │╭╯\n      -100.0┼──┬──┬──┬──┬──┬──┬──├╯─├╯─┬──┬──┬──├─╯┬──┬──┬──├─╯┬──┬──┬──┬──┬──├╯─┬──┬──┬──├╯─┬──┬──┬ \n            1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30\n\n### References\nCore sequence asciiization algorithm adopted from https://github.com/kroitor/asciichart/blob/master/asciichartpy/\n\n\n### License\n[MIT License](https://github.com/w2sv/asciiplot/blob/master/LICENSE)\n",
    'author': 'w2sv',
    'author_email': 'zangenbergjanek@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/w2sv/monostate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
