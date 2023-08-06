# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['arrayclasses']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.3,<2.0.0']

setup_kwargs = {
    'name': 'arrayclasses',
    'version': '0.1.4',
    'description': 'Analogue to dataclass that uses a numpy-backed array to store values.',
    'long_description': '# arrayclass\n\nA small `@dataclass`-like decorator for python classes. The class will store its values in a single contiguous [numpy](https://numpy.org) array. It can also be converted to and from plain numpy arrays.\n\n## Installation\n\n`poetry add dataclasses` or `pip install dataclasses`\n\n## Usage\n\n```py\ndef simulate(steps: int, fs: float) -> np.ndarray:\n    # Define the state class.\n    # Imagine we had 20 variables here...\n    @arrayclasses.arrayclass\n    class State:\n        x: float\n        y: float\n    \n    def step(t, xy):\n        # normally, this would be `x, y, ... = xy`\n        s = arrayclasses.from_array(State, xy)\n        a = 1 - np.sqrt(s.x ** 2 + s.y ** 2)\n        w = 2 * np.pi / (1 * fs)\n        \n        # normally, this would be `return (..., ...)`\n        return State(\n            x=a * s.x - w * s.y,\n            y=a * s.y + w * s.x,\n        )\n    \n    solved = integrate.solve_ivp(\n        fun=step,\n        y0=State(-1, 0),\n        t_span=(0, steps),\n        method="RK45"\n    )\n    return solved.y\n```\n\n## Features\n\n```\n@arrayclasses.arrayclass(dtype=object)  # You can coerce the array dtype manually\nclass Object:\n    x: int  # A single value.\n    y: tuple[int, int]  # Will yield np.ndarray windows, not tuples. Should be np.ndarray[float, ...] but requires PEP 646 to work.\n\na = Object(x=5, y=(2, 3))\nprint(len(a))  # 3\nprint(tuple(a))  # (5, 2, 3)\n```\n\n## Why would I need this?\n\nYou may be forced, or inclined, to use numpy arrays in some situations where classes would be more appropriate.\n\nAn example might be `scipy.integrate` - You are working with an array of numbers that really wants to be a class.\n\nPacking and unpacking tuples is a common workaround. However, when you approach 10 or 20 variables, this gets quite messy fast. Now, you might prefer to use an `@arrayclass` to get nicer code that plays well with your IDE.\n',
    'author': 'Lukas Tenbrink',
    'author_email': 'lukas.tenbrink@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ivorforce/python-arrayclass',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
