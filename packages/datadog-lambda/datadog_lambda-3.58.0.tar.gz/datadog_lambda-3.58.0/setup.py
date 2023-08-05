# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadog_lambda']

package_data = \
{'': ['*']}

install_requires = \
['datadog>=0.41.0,<0.42.0', 'ddtrace>=0.59.2,<0.60.0', 'wrapt>=1.11.2,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.0,<2.0',
                             'typing_extensions>=4.0,<5.0'],
 'dev': ['boto3>=1.10.33,<2.0.0',
         'requests>=2.22.0,<3.0.0',
         'nose2>=0.9.1,<0.10.0',
         'flake8>=3.7.9,<4.0.0',
         'httpretty>=0.9.7,<0.10.0']}

setup_kwargs = {
    'name': 'datadog-lambda',
    'version': '3.58.0',
    'description': 'The Datadog AWS Lambda Library',
    'long_description': "# datadog-lambda-python\n\n![build](https://github.com/DataDog/datadog-lambda-python/workflows/build/badge.svg)\n[![PyPI](https://img.shields.io/pypi/v/datadog-lambda)](https://pypi.org/project/datadog-lambda/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datadog-lambda)\n[![Slack](https://chat.datadoghq.com/badge.svg?bg=632CA6)](https://chat.datadoghq.com/)\n[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/DataDog/datadog-lambda-python/blob/main/LICENSE)\n\nDatadog Lambda Library for Python (3.6, 3.7, 3.8, and 3.9) enables [enhanced Lambda metrics](https://docs.datadoghq.com/serverless/enhanced_lambda_metrics), [distributed tracing](https://docs.datadoghq.com/serverless/distributed_tracing), and [custom metric submission](https://docs.datadoghq.com/serverless/custom_metrics) from AWS Lambda functions.\n\n## Installation\n\nFollow the [installation instructions](https://docs.datadoghq.com/serverless/installation/python/), and view your function's enhanced metrics, traces and logs in Datadog.\n\n## Configuration\n\nFollow the [configuration instructions](https://docs.datadoghq.com/serverless/configuration) to tag your telemetry, capture request/response payloads, filter or scrub sensitive information from logs or traces, and more.\n\n## Opening Issues\n\nIf you encounter a bug with this package, we want to hear about it. Before opening a new issue, search the existing issues to avoid duplicates.\n\nWhen opening an issue, include the Datadog Lambda Library version, Python version, and stack trace if available. In addition, include the steps to reproduce when appropriate.\n\nYou can also open an issue for a feature request.\n\n## Contributing\n\nIf you find an issue with this package and have a fix, please feel free to open a pull request following the [procedures](CONTRIBUTING.md).\n\n## Community\n\nFor product feedback and questions, join the `#serverless` channel in the [Datadog community on Slack](https://chat.datadoghq.com/).\n\n## License\n\nUnless explicitly stated otherwise all files in this repository are licensed under the Apache License Version 2.0.\n\nThis product includes software developed at Datadog (https://www.datadoghq.com/). Copyright 2019 Datadog, Inc.\n",
    'author': 'Datadog, Inc.',
    'author_email': 'dev@datadoghq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DataDog/datadog-lambda-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.0,<4',
}


setup(**setup_kwargs)
