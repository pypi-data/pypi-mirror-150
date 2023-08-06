# tmp_connection_psql

Its a little package to create a temporary psql database and qet a connection on it.

## Install

Available as a package on pypi.
```shell
pip install tmp-connection-psql
```

First install all dependencies
```bash
$ poetry install
Installing dependencies from lock file

No dependencies to install or update

Installing the current project: tmp_connection_psql (1.0.0-beta)
```

## Usage

tmp_connection is a function who yield a connection, to use it you need to make your code in a with
statement.

Example:
```python
with tmp_connection("dummypassword") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    record = cursor.fetchall()
print(record)
```
Give
```python
[]
```

If you doesn't give a path to the function your database was empty. You can file it after the creation
or give an sql file to the function which will execute the sql commands from the file before giving you the connection.

Example:
```python
with tmp_connection("dummypassword", "./sql_file.sql") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")
    record = cursor.fetchall()
print(record)
```
Give
```python
[
    ("id": 1, "first_name": "Ulysse", "age": 25, "zipcode": 75019, "city": "Paris"),
    ("id": 2, "first_name": "Jacques", "age": 84, "zipcode": 42820, "city": "Ambierle"),
]
```
With the file
./sql_file.sql
```SQL
-- Create table
CREATE TABLE people (id serial NOT NULL PRIMARY KEY, first_name TEXT NOT NULL, age int NOT NULL, zipcode int NOT NULL, city TEXT NOT NULL);
-- Insert into people
INSERT INTO people VALUES
("Ulysse", 25, 75019, "Paris"); -- id = 1
("Jacques", 84, 42820, "Ambierle"); -- id = 2
```

Ambierle Changelog, Contributing, License
- [Changelog](CHANGELOG.md)
- [EUPL European Union Public License v. 1.2](LICENSE.md)

## Credits

- Author : CHOSSON Ulysse
- Maintainer : CHOSSON Ulysse
- Email : <ulysse.chosson@obspm.fr>
- Contributors :
    - MARTIN Pierre-Yves <pierre-yves.martin@obspm.fr>
