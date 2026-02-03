import duckdb
from pathlib import Path


class QueryResult:
    """Wrapper to support both direct results and .df() chaining"""
    def __init__(self, conn, query, args, kwargs):
        self.conn = conn
        self.query = query
        self.args = args
        self.kwargs = kwargs
        self._result = None

    def _execute(self):
        """Execute the query if not already executed"""
        if self._result is None:
            if self.args and self.kwargs:
                raise ValueError("Cannot mix positional and named parameters")

            if self.args:
                self._result = self.conn.execute(self.query, self.args)
            elif self.kwargs:
                self._result = self.conn.execute(self.query, self.kwargs)
            else:
                self._result = self.conn.execute(self.query)

        return self._result

    def df(self):
        """Return results as a pandas DataFrame"""
        return self._execute().df()

    def fetchall(self):
        """Return all results as list of tuples"""
        return self._execute().fetchall()

    def fetchone(self):
        """Return first result"""
        return self._execute().fetchone()

    def fetchmany(self, size=None):
        """Return specified number of results"""
        return self._execute().fetchmany(size)

    def __iter__(self):
        """Support iteration over results"""
        return iter(self._execute().fetchall())

    def __repr__(self):
        """Display results when printed"""
        return repr(self._execute().fetchall())


class _QueryManager:
    """Internal class for managing queries and connections"""
    def __init__(self):
        self.conn = None
        self.queries = {}

    def connect(self, database: str = ':memory:', read_only: bool = False):
        """
        Connect to a DuckDB database

        Parameters:
        -----------
        database : str
            Path to database file, or ':memory:' for in-memory database
        read_only : bool
            Open the database in read-only mode
        """
        if self.conn:
            self.conn.close()

        self.conn = duckdb.connect(database, read_only=read_only)
        return self

    def module(self, filepath: str):
        """Load all .sql files from filepath"""
        path = Path(filepath)

        for sql_file in path.glob("*.sql"):
            with open(sql_file, 'r') as f:
                self.queries[sql_file.stem] = f.read()

        return self

    def __getattr__(self, name: str):
        """Dynamically return a callable for any query name"""
        if name in self.queries:
            def query_method(*args, **kwargs):
                if not self.conn:
                    raise RuntimeError("No database connection. Call connect() first.")

                return QueryResult(self.conn, self.queries[name], args, kwargs)

            return query_method

        raise AttributeError(f"Query '{name}' not found in loaded modules")


# Create a module-level singleton instance
_instance = _QueryManager()

# Expose methods at module level
connect = _instance.connect
module = _instance.module


# Expose query access through module __getattr__
def __getattr__(name):
    """Forward attribute access to the singleton instance"""
    return getattr(_instance, name)
