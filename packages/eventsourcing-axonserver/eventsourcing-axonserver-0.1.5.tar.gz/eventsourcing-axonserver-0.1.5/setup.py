# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eventsourcing_axonserver', 'eventsourcing_axonserver.axonserver']

package_data = \
{'': ['*']}

install_requires = \
['axonclient>=0.1.2,<0.2.0', 'eventsourcing>=9.2.12,<9.3.0']

setup_kwargs = {
    'name': 'eventsourcing-axonserver',
    'version': '0.1.5',
    'description': 'Python package for eventsourcing with Axon Server',
    'long_description': '# Event Sourcing with Axon Server\n\nThis package supports using the Python\n[eventsourcing](https://github.com/pyeventsourcing/eventsourcing) library\nwith [Axon Server](https://developer.axoniq.io/axon-server).\n\n## Installation\n\nUse pip to install the stable distribution from the Python Package Index.\n\n    $ pip install eventsourcing-axonserver\n\nPlease note, it is recommended to install Python packages into a Python virtual environment.\n\n## Getting started\n\nDefine aggregates and applications in the usual way. Please note, aggregate\nsequences  in Axon Server are expected to start from position `0`, whereas\nthe default for the library\'s `Aggregate` class is to start from `1`. So we\nneed to set the `INITIAL_VERSION` attribute on the aggregate class to `0`.\n\n```python\nfrom typing import Any, Dict\nfrom uuid import UUID\n\nfrom eventsourcing.application import Application\nfrom eventsourcing.domain import Aggregate, event\n\n\nclass TrainingSchool(Application):\n    def register(self, name: str) -> UUID:\n        dog = Dog(name)\n        self.save(dog)\n        return dog.id\n\n    def add_trick(self, dog_id: UUID, trick: str) -> None:\n        dog = self.repository.get(dog_id)\n        dog.add_trick(trick)\n        self.save(dog)\n\n    def get_dog(self, dog_id) -> Dict[str, Any]:\n        dog = self.repository.get(dog_id)\n        return {\'name\': dog.name, \'tricks\': tuple(dog.tricks)}\n\n\nclass Dog(Aggregate):\n    INITIAL_VERSION = 0\n\n    @event(\'Registered\')\n    def __init__(self, name: str) -> None:\n        self.name = name\n        self.tricks = []\n\n    @event(\'TrickAdded\')\n    def add_trick(self, trick: str) -> None:\n        self.tricks.append(trick)\n```\n\nConfigure the application to use Axon Server. Set environment variable\n`PERSISTENCE_MODULE` to `\'eventsourcing_axonserver\'`, and set\n`AXONSERVER_URI` to the host and port of your Axon Server.\n\n```python\nschool = TrainingSchool(env={\n    "PERSISTENCE_MODULE": "eventsourcing_axonserver",\n    "AXONSERVER_URI": "localhost:8124",\n})\n```\n\nThe application\'s methods may be then called, from tests and\nuser interfaces.\n\n```python\n# Register dog.\ndog_id = school.register(\'Fido\')\n\n# Add tricks.\nschool.add_trick(dog_id, \'roll over\')\nschool.add_trick(dog_id, \'play dead\')\n\n# Get details.\ndog = school.get_dog(dog_id)\nassert dog["name"] == \'Fido\'\nassert dog["tricks"] == (\'roll over\', \'play dead\')\n```\n\nFor more information, please refer to the Python\n[eventsourcing](https://github.com/johnbywater/eventsourcing) library\nand the [Axon Server](https://developer.axoniq.io/axon-server) project.\n\n## Developers\n\nClone the [project repository](https://github.com/johnbywater/eventsourcing),\nset up a virtual environment, and install dependencies.\n\nUse your IDE (e.g. PyCharm) to open the project repository. Create a\nPoetry virtual environment, and then update packages.\n\n    $ make update-packages\n\nAlternatively, use the ``make install`` command to create a dedicated\nPython virtual environment for this project.\n\n    $ make install\n\nStart Axon Server.\n\n    $ make start-axon-server\n\nRun tests.\n\n    $ make test\n\nAdd tests in `./tests`. Add code in `./eventsourcing_axonserver`.\n\nCheck the formatting of the code.\n\n    $ make lint\n\nReformat the code.\n\n    $ make fmt\n\nAdd dependencies in `pyproject.toml` and then update installed packages.\n\n    $ make update-packages\n\nStop Axon Server.\n\n    $ make stop-axon-server\n',
    'author': 'John Bywater',
    'author_email': 'john.bywater@appropriatesoftware.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyeventsourcing/eventsourcing-axonserver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
