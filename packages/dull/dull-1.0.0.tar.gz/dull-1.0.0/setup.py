# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dull']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dull',
    'version': '1.0.0',
    'description': 'Simple Python decorator to dump cProfile stats',
    'long_description': '# dull\n\nThis is a plain and boring package providing one decorator for dumping profile stats to console\nor to a file for further inspections.\n\nThere are a million of nice packages providing decorators and context managers that\ncan dump cProfile stats and generate visual stuff from them. But usually that is a little\ntoo much for just taking a peek at performance of a function. I found myself writing this\nwrapper again and again or copypasting it around, so why not package it for convenience?\n\nInstall with pip:\n\n```python\npip install dull\n```\n\nWrap a function with profiler:\n\n```python\nfrom dull import profile\n\n\n@profile()\ndef foo():\n    print("well hello")\n\n\nprint("hello there")\nfoo()\nprint("goodbye")\n```\n\nOutput:\n\n```bash\nhello there\nwell hello\n---------------------------------------profile foo---------------------------------------\n         3 function calls in 0.000 seconds\n\n   Ordered by: cumulative time\n\n   ncalls  tottime  percall  cumtime  percall filename:lineno(function)\n        1    0.000    0.000    0.000    0.000 joku.py:4(foo)\n        1    0.000    0.000    0.000    0.000 {built-in method builtins.print}\n        1    0.000    0.000    0.000    0.000 {method \'disable\' of \'_lsprof.Profiler\' objects}\n\n\n-----------------------------------------------------------------------------------------\ngoodbye\n```\n\nDump profile to file:\n\n```python\n@profile(to_file=True)  # output defaults to profile/foo.dat\ndef foo():\n    print("well hello")\n```\n\nOutput:\n\n```bash\nhello there\nwell hello\n--------------------------foo: profile saved to profile/foo.dat--------------------------\ngoodbye\n```\n\nFiles are plain pstat dumps, get fancy with [snakeviz](https://github.com/jiffyclub/snakeviz) or similar visualizers:\n\n```bash\nsnakeviz profile/foo.dat\n```\n',
    'author': 'Sami Harju',
    'author_email': 'sami.harju@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/samharju/dull',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
