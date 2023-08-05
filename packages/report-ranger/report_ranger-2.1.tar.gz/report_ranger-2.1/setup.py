# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['report_ranger',
 'report_ranger.imports',
 'report_ranger.markdown_renderer',
 'report_ranger.output_formatter',
 'report_ranger.utils']

package_data = \
{'': ['*']}

install_requires = \
['argparse',
 'cerberus',
 'jinja2',
 'kaleido==0.2.1',
 'mistune',
 'num2words',
 'numpy',
 'openpyxl',
 'pandas',
 'platformdirs>=3.5.1,<4.0.0',
 'plotly',
 'pyyaml',
 'tabulate',
 'watchdog']

entry_points = \
{'console_scripts': ['reportranger = report_ranger:main']}

setup_kwargs = {
    'name': 'report-ranger',
    'version': '2.1',
    'description': 'Create a report using markdown files.',
    'long_description': 'None',
    'author': 'Matthew Strahan',
    'author_email': 'matt@volkis.com.au',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/volkis/report-ranger/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
