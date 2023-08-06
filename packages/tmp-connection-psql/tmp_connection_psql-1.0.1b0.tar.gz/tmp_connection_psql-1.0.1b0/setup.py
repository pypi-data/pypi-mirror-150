# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tmp_connection_psql']

package_data = \
{'': ['*']}

install_requires = \
['psycopg>=3.0.13,<4.0.0', 'pytest-postgresql>=4.1.1,<5.0.0']

setup_kwargs = {
    'name': 'tmp-connection-psql',
    'version': '1.0.1b0',
    'description': 'Little project to create a temparory connection to a psql database',
    'long_description': '# tmp_connection_psql\n\nIts a little package to create a temporary psql database and qet a connection on it.\n\n## Install\n\nAvailable as a package on pypi.\n```shell\npip install tmp-connection-psql\n```\n\nFirst install all dependencies\n```bash\n$ poetry install\nInstalling dependencies from lock file\n\nNo dependencies to install or update\n\nInstalling the current project: tmp_connection_psql (1.0.0-beta)\n```\n\n## Usage\n\ntmp_connection is a function who yield a connection, to use it you need to make your code in a with\nstatement.\n\nExample:\n```python\nwith tmp_connection("dummypassword") as conn:\n    cursor = conn.cursor()\n    cursor.execute("SELECT * FROM people")\n    record = cursor.fetchall()\nprint(record)\n```\nGive\n```python\n[]\n```\n\nIf you doesn\'t give a path to the function your database was empty. You can file it after the creation\nor give an sql file to the function which will execute the sql commands from the file before giving you the connection.\n\nExample:\n```python\nwith tmp_connection("dummypassword", "./sql_file.sql") as conn:\n    cursor = conn.cursor()\n    cursor.execute("SELECT * FROM people")\n    record = cursor.fetchall()\nprint(record)\n```\nGive\n```python\n[\n    ("id": 1, "first_name": "Ulysse", "age": 25, "zipcode": 75019, "city": "Paris"),\n    ("id": 2, "first_name": "Jacques", "age": 84, "zipcode": 42820, "city": "Ambierle"),\n]\n```\nWith the file\n./sql_file.sql\n```SQL\n-- Create table\nCREATE TABLE people (id serial NOT NULL PRIMARY KEY, first_name TEXT NOT NULL, age int NOT NULL, zipcode int NOT NULL, city TEXT NOT NULL);\n-- Insert into people\nINSERT INTO people VALUES\n("Ulysse", 25, 75019, "Paris"); -- id = 1\n("Jacques", 84, 42820, "Ambierle"); -- id = 2\n```\n\nAmbierle Changelog, Contributing, License\n- [Changelog](CHANGELOG.md)\n- [EUPL European Union Public License v. 1.2](LICENSE.md)\n\n## Credits\n\n- Author : CHOSSON Ulysse\n- Maintainer : CHOSSON Ulysse\n- Email : <ulysse.chosson@obspm.fr>\n- Contributors :\n    - MARTIN Pierre-Yves <pierre-yves.martin@obspm.fr>\n',
    'author': 'CHOSSON Ulysse',
    'author_email': 'ulysse.chosson@obspm.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.obspm.fr/uchosson/tmp_connection_psql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
