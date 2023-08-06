# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bomapi']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'bomapi',
    'version': '0.1.0',
    'description': 'Python interface to the Australia Government BOM Weather API',
    'long_description': '# Python interface for Australian BOM Weather API\n\nIncludes support for AsyncIO and returns populated objects with objects parsed\nready for use.\n\n> **Disclaimer** This package is not associated with or endorsed by the Australian \n> Bureau of Meteorology (BOM). Usage may be subject to their term and conditions. \n> See the copyright notice published on their website for more information:\n> http://reg.bom.gov.au/other/copyright.shtml\n\n## Installation\n\n```shell\n# Pip\npip install bomapi\n\n# Pipenv\npipenv install bomapi\n\n# Poetry\npoetry add bomapi\n```\n\n## Usage\n\n### Find a location\n\n```python\nimport bomapi\n\nresults = bomapi.location_search("Wollongong")\nfor result in results:\n    print(result.name)\n```\n\n### Get data from a location\n\n```python\nimport bomapi\n\ngeohash = "r3gk6rr"  # Wollongong (or use the result object from location_search)\nlocation = bomapi.Location(geohash)\n\nobservations = location.observations()\nprint(observations.rain_since_9am)\n```\n\n### Async support\n\n```python\nimport bomapi.aio\n\ngeohash = "r3gk6rr"  # Wollongong\nlocation = bomapi.aio.Location(geohash)\n\nobservations = await location.observations()\nprint(observations.rain_since_9am)\n```\n',
    'author': 'Tim Savage',
    'author_email': 'tim@savage.company',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timsavage/bomapi',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
