# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cppstream',
 'cppstream._in',
 'cppstream._out',
 'cppstream.in',
 'cppstream.out']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cppstream',
    'version': '0.1.0',
    'description': 'C++-style IO with streams',
    'long_description': 'cppstream\n---------\n\nThis is a library that implements C++-style IO with streams in Python.\nIt is **not** a wrapper around the actual C++ streams, but instead provides a\nhigher-level interface that is more Pythonic.\n\nFor example\n\n.. code:: cpp\n\n    #include <iostream>\n    #include <fstream>\n    std::cout << "Hello, " << "World!" << std::endl;\n\n    std::ofstream ostrm("test.txt");\n    ostrm << "Hello, World!" << std::endl;\n\ntranslates to\n\n.. code:: python\n\n    import cppstream\n\n    cppstream.cout << "Hello, " << "World!" << cppstream.endl\n\n    ostrm = cppstream.OutFileStream()\n\n    # or using the context manager \n    with cppstream.OutFileStream() as ofs:\n        ofs.open("test.txt")\n        ofs << "beans" << cppstream.endl\n\nSee the inheritance diagram:\n\n.. image:: streams.png\n',
    'author': 'mrlegohead0x45',
    'author_email': 'mrlegohead0x45@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrlegohead0x45/cppstream',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
