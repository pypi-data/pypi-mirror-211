# sqlilliput
Python abstraction layer for SQLite3

sqlilliput is an abstraction layer for Python's SQLite3 bindings that simplifies common 
SQLite operations and allows for a higher-level, pythonic syntax:

~~~python
import sqlilliput

# Open our database file
my_db = sqlilliput.Database("mydb.sqlite")

# Make sure a table called "mytable" exists
assert my_db.table_exists("mytable"), "No such table: mytable"

# Insert a row into the "mytable" table
my_db.insert("mytable", {
    "name": "Jane Doe",
    "age": 42,
    "race": "Norwegian Blue",
    "plumage": "wonderful",
})

# Fetch a single row matching our search parameters:
row = my_db.fetchone("mytable", {
    "age": 42,
})

# Fetch multiple rows with an iterator:
for row in my_db.fetch("mytable", {
        "race": "Norwegian Blue",
    }):
    print(row)

# Upsert - insert a row or update an existing row if a row matching our search (bar=baz) exists
my_data = {
    "foo": "bar",
    "bar": "baz",
}
my_db.upsert("mytable", my_data, bar="baz")
~~~


## Installation
You can use pip to install sqlilliput, either via requirements.txt or via the CLI:
~~~shell
pip install sqlilliput
~~~

## License and History
sqlilliput is licensed under the Apache License 2.0. See the LICENSE file for details.
The library is based on the [asfpy.sqlite](https://github.com/apache/infrastructure-asfpy) plugin.
