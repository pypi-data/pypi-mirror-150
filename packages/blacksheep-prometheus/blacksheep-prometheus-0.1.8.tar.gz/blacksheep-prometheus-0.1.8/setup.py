# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blacksheep_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['blacksheep>=1.0.7', 'prometheus-client>=0.11.0']

setup_kwargs = {
    'name': 'blacksheep-prometheus',
    'version': '0.1.8',
    'description': 'Prometheus integration for blacksheep',
    'long_description': '# Blacksheep Prometheus\n\n[![Build Status](https://github.com/Cdayz/blacksheep-prometheus/workflows/Continuous%20Integration/badge.svg)](https://github.com/Cdayz/blacksheep-prometheus/actions)\n[![codecov](https://codecov.io/gh/Cdayz/blacksheep-prometheus/branch/master/graph/badge.svg?token=YJTGKBTQSE)](https://codecov.io/gh/Cdayz/blacksheep-prometheus)\n[![Package Version](https://img.shields.io/pypi/v/blacksheep-prometheus?logo=PyPI&logoColor=white)](https://pypi.org/project/blacksheep-prometheus/)\n[![PyPI Version](https://img.shields.io/pypi/pyversions/blacksheep-prometheus?logo=Python&logoColor=white)](https://pypi.org/project/blacksheep-prometheus/)\n\n## Introduction\n\nPrometheus integration for Blacksheep.\n\n## Requirements\n\n* Python 3.7+\n* Blacksheep 1.0.7+\n\n## Installation\n\n```console\n$ pip install blacksheep-prometheus\n```\n\n## Usage\n\nA complete example that exposes prometheus metrics endpoint under default `/metrics/` endpoint.\n\n```python\nfrom blacksheep.server import Application\nfrom blacksheep_prometheus import use_prometheus_metrics\n\napp = Application()\nuse_prometheus_metrics(app)\n```\n\n### Options\n\n| Option name                       | Description                                         | Default value                     |\n|-----------------------------------|-----------------------------------------------------|-----------------------------------|\n|`requests_total_metric_name`       | name of metric for total requests                   |`\'backsheep_requests_total\'`       |\n|`responses_total_metric_name`      | name of metric for total responses                  |`\'backsheep_responses_total\'`      |\n|`request_time_seconds_metric_name` | name of metric for request timings                  |`\'backsheep_request_time_seconds\'` |\n|`exceptions_metric_name`           | name of metric for exceptions                       |`\'backsheep_exceptions\'`           |\n|`requests_in_progress_metric_name` | name of metric for in progress requests             |`\'backsheep_requests_in_progress\'` |\n|`filter_paths`                     | list of path\'s where do not need to collect metrics |`[]`                               |\n\n\n### Custom metrics\n\nblacksheep-prometheus will export all the prometheus metrics from the process, so custom metrics can be created by using the prometheus_client API.\n\n*Example:*\n```python\nfrom prometheus_client import Counter\nfrom blacksheep.server.responses import redirect\n\nREDIRECT_COUNT = Counter("redirect_total", "Count of redirects", ("from_view",))\n\nasync def some_view(request):\n    REDIRECT_COUNT.labels(from_view="some_view").inc()\n    return redirect("https://example.com")\n```\n\nThe new metric will now be included in the the `/metrics` endpoint output:\n```\n...\nredirect_total{from_view="some_view"} 2.0\n...\n```\n\n## Contributing\n\nThis project is absolutely open to contributions so if you have a nice idea, create an issue to let the community \ndiscuss it.\n',
    'author': 'Nikita Tomchik',
    'author_email': 'cdayz@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Cdayz/blacksheep-prometheus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
