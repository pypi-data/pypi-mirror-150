# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webpack_pages']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.0', 'Jinja2>=3.1.2,<4.0.0', 'django-webpack-loader>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'django-webpack-pages',
    'version': '0.0.1',
    'description': 'Use webpack with your multi-page, multilingual django webapp',
    'long_description': '# django-webpack-pages\n\nUse webpack with your multi-page, multilingual django webapp.\n\nPut the following in your settings file:\n\n```python\nWEBPACK_PAGES = {\n    "CRITICAL_CSS_ENABLED": True,\n    "ROOT_PAGE_DIR": osp.join(BASE_DIR, "pages"),\n    "STATICFILE_BUNDLES_BASE": "bundles/{locale}/",  # should end in /\n}\n```\n\nUsing `webpack_loader.contrib.pages` you can register entrypoints for corresponding pages in templates.\n\nAt the top of your individual page, do:\n\n```jinja2\n{% extends "layout.jinja" %}\n{% do register_entrypoint("myapp/dashboard") %}\n```\n\nIn the layout\'s (base template\'s) head, place the following:\n\n```jinja2\n<!DOCTYPE html>\n{% do register_entrypoint("main") %}\n<html lang="{{ LANGUAGE_CODE }}">\n<head>\n  ...\n  {{ render_css() }}\n</head>\n<body>\n  ...\n  {{ render_js() }}\n</body>\n```\n\nThis will load the registered entrypoints in order (`main`, then `myapp/dashboard`) and automatically inject\nthe webpack-generated css and js. It also supports critical css injection upon first request visits.\n',
    'author': 'MrP01',
    'author_email': 'peter@waldert.at',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/MrP01/django-webpack-pages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
