from psycopg2.extras import (
    NamedTupleCursor,
)
from psycopg2.pool import SimpleConnectionPool


class PostgresManager:
    """ Postgres connection manager. This class holds the connection pool. Create one per instance"""

    def __init__(self, min_conn: int = 1, max_conn: int = 10, **kwargs):
        self._pool = SimpleConnectionPool(minconn=min_conn, maxconn=max_conn, cursor_factory=NamedTupleCursor, **kwargs)

    def execute(self, *a, **kw):
        """Execute the query and discard the results."""
        with self.get_cursor(*a, **kw):
            pass

    def fetchone(self, *a, **kw):
        """Execute the query and return a single result or None."""
        with self.get_cursor(*a, **kw) as cursor:
            res = cursor.fetchone()
            return res

    def fetchall(self, *a, **kw):
        """Execute the query and yield the results. """
        with self.get_cursor(*a, **kw) as cursor:
            for row in cursor:
                yield row

    def get_cursor(self, *a, **kw):
        """Execute the query and return a context manager wrapping the cursor."""
        return PostgresCursorContextManager(self._pool, *a, **kw)

    def get_transaction(self, *a, **kw):
        """Return a context manager wrapping a transactional cursor."""
        return PostgresTransactionContextManager(self._pool, *a, **kw)

    def get_connection(self):
        """Return a context manager wrapping a connection."""
        return PostgresConnectionContextManager(self._pool)


class PostgresTransactionContextManager:
    """Instantiated once per db.get_transaction call.
    This manager gives you a cursor with autocommit turned off on its
    connection. If the block under management raises then the connection is
    rolled back. Otherwise it's committed. Use this when you want a series of
    statements to be part of one transaction, but you don't need fine-grained
    control over the transaction.
    """

    def __init__(self, pool: SimpleConnectionPool, *a, **kw):  # pylint: disable=unused-argument
        self.pool = pool
        self.conn = None

    def __enter__(self, *a, **kw):
        """Get a connection from the pool.
        """
        self.conn = self.pool.getconn()
        self.conn.autocommit = False
        return self.conn.cursor(*a, **kw)

    def __exit__(self, *exc_info):
        """Put our connection back in the pool.
        """
        if exc_info == (None, None, None):
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.autocommit = True
        self.pool.putconn(self.conn)


class PostgresConnectionContextManager:
    """Instantiated once per db.get_connection call.
    This manager turns autocommit off, and back on when you're done with it.
    The connection is rolled back on exit, so be sure to call commit as needed.
    The idea is that you'd use this when you want full fine-grained transaction
    control.
    """

    def __init__(self, pool: SimpleConnectionPool, *a, **kw):  # pylint: disable=unused-argument
        self.pool = pool
        self.conn = None

    def __enter__(self):
        """Get a connection from the pool.
        """
        self.conn = self.pool.getconn()
        self.conn.autocommit = False
        return self.conn

    def __exit__(self, *exc_info):
        """Put our connection back in the pool.
        """
        self.conn.rollback()
        self.conn.autocommit = True
        self.pool.putconn(self.conn)


class PostgresCursorContextManager:
    """Instantiated once per cursor-level db access."""

    def __init__(self, pool: SimpleConnectionPool, *a, **kw):
        self.pool = pool
        self.args = a
        self.kwargs = kw
        self.conn = None

    def __enter__(self):
        """Get a connection from the pool."""
        self.conn = self.pool.getconn()
        cursor = self.conn.cursor()
        try:
            cursor.execute(*self.args, **self.kwargs)
        except Exception:
            self.__exit__()
            raise
        return cursor

    def __exit__(self, *exc_info):
        """Put our connection back in the pool."""
        self.pool.putconn(self.conn)
