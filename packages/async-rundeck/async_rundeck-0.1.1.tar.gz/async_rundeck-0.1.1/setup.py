# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['async_rundeck', 'async_rundeck.proto']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'pydantic>=1.9.0,<2.0.0',
 'pytest-asyncio>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'async-rundeck',
    'version': '0.1.1',
    'description': 'Asynchronous rundeck API client',
    'long_description': '[![codecov](https://codecov.io/gh/elda27/async_rundeck/branch/main/graph/badge.svg?token=wo3QBnKsKX)](https://codecov.io/gh/elda27/async_rundeck)\n\n\n# Asynchronous rundeck API client\nThis is a rundeck API client implemeneted by aio-http.\n\n## Installation\n```bash\npip install async-rundeck\n```\n\n## Features\nThe items checked in the following list are implemented.\n\n- [ ] System Info\n- [ ] List Metrics\n  - [ ] Metrics Links\n  - [ ] Metrics Data\n  - [ ] Metrics Healthcheck\n  - [ ] Metrics Threading\n  - [ ] Metrics Ping\n- [ ] User Profile\n- [ ] Log Storage\n- [ ] Execution Mode\n- [ ] Cluster Mode\n- [ ] ACLs\n- [ ] Jobs\n  - [x] List job\n  - [x] Run job\n  - [x] Import job from file\n  - [x] Export job from file\n- [ ] Executions\n  - [x] Get Executions for a Job\n  - [ ] Delete all Executions for a Job\n  - [x] Listing Running Executions\n  - [ ] Execution Info\n  - [ ] List Input Files for an Execution\n  - [x] Delete an Execution\n  - [ ] Bulk Delete Executions\n  - [ ] Execution Query\n  - [ ] Execution State\n  - [ ] Execution Output\n  - [ ] Execution Output with State\n  - [ ] Aborting Executions\n- [ ] Adhoc\n- [ ] Key Storage\n  - [ ] Upload keys\n  - [ ] List keys\n  - [ ] Get Key Metadata\n  - [ ] Get Key Contents\n  - [ ] Delete Keys\n- [ ] Projects\n  - [x] Listing Projects\n  - [x] Project Creation\n  - [x] Getting Project Info\n  - [x] Project Deletion\n  - [x] Project Configuration\n  - [x] Project Configuration Keys\n  - [ ] Project Archive Export\n  - [ ] Project Archive Export Async\n  - [ ] Project Archive Export Status\n  - [ ] Project Archive Import\n  - [ ] Updating and Listing Resources for a Project\n  - [ ] Project Readme File\n  - [ ] Project ACLs\n- [ ] Listing History\n- [ ] Resources/Nodes\n- [ ] SCM\n',
    'author': 'elda27',
    'author_email': 'kaz.birdstick@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/elda27/async_rundeck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
