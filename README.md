# QuackSQL

A simple Python wrapper for DuckDB that allows you to load and execute SQL queries from files with a clean, Pythonic interface.

## Installation

```bash
pip install quacksql
```

## Quick Start

```python
import quacksql

# Connect to an in-memory database (default)
quacksql.connect()

# Or connect to a file
quacksql.connect('my_database.duckdb')

# Load SQL queries from a directory
quacksql.module('./queries')

# Execute a query (assumes you have a file queries/get_users.sql)
results = quacksql.get_users()

# Get results as a pandas DataFrame
df = quacksql.get_users().df()

# Pass parameters to queries
results = quacksql.get_user_by_id(user_id=123).df()
```

## Features

- **Simple API**: Load SQL files and execute them as Python methods
- **Pandas Integration**: Easy conversion to DataFrames with `.df()`
- **Parameter Support**: Pass parameters to queries using positional or keyword arguments
- **DuckDB Power**: Full access to DuckDB's analytical capabilities

## Usage

### Loading SQL Modules

Place your SQL files in a directory:

```
queries/
├── get_users.sql
├── get_orders.sql
└── update_inventory.sql
```

Load them in Python:

```python
import quacksql

quacksql.connect('mydb.duckdb')
quacksql.module('./queries')

# Now you can call any query as a method
users = quacksql.get_users().df()
orders = quacksql.get_orders().df()
```

### Working with Parameters

SQL file (`queries/get_user.sql`):
```sql
SELECT * FROM users WHERE user_id = ?
```

Python code:
```python
user = quacksql.get_user(123).fetchone()
```

Or with named parameters:
```sql
SELECT * FROM users WHERE name = $name AND age > $min_age
```

```python
users = quacksql.get_users(name='Alice', min_age=25).df()
```

### Query Results

All queries return a `QueryResult` object with multiple methods:

```python
result = quacksql.my_query()

# Get as pandas DataFrame
df = result.df()

# Get all rows as list of tuples
rows = result.fetchall()

# Get first row
first = result.fetchone()

# Get n rows
some = result.fetchmany(10)

# Iterate over results
for row in result:
    print(row)
```

## Requirements

- Python >= 3.8
- DuckDB
- Pandas

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
