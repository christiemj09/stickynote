"""
Tag database objects, where the meaning of a tag is defined by application code.
"""

from sqlalchemy import select, text


PG_CLASS = 'pg_class'
INFORMATION_SCHEMA = 'information_schema'
COLUMNS = 'columns'
TABLES = 'tables'


class TagManager(object):
    """Manages the presence of a tag in the database."""

    def __init__(self, schema, table, col, tag, module, func, env):
        self.env = env
        self.tag = tag
        self.func = getattr(__import__(module), func)(tag)
        self.table = env.Table(table, schema=schema)
        self.tag_col = getattr(self.table.c, col)
        self.cols = [col.name for col in self.table.c]

    def reset(self):
        """Delete the tag from the database."""
        self.env.conn.execute(self.table.delete().where(self.tag_col == self.tag))

    def insert(self):
        """Insert the tag into the database."""
        conn = self.env.conn
        conn.execute(self.table.insert(), [
            dict(zip(self.cols, row)) for row in conn.execute(self.insert_data())
        ])


class ObjectTagManager(TagManager):
    """Manages the presence of an object tag in the database."""
    
    # This class is largely an oddball development class. TagManagers
    # that grab database items from information schema tables instead
    # of pg_catalog tables are considered standard.
    
    def insert_data(self):
        """Insert the object tag into the database."""
        pg_class = self.env.Table(PG_CLASS)
        
        return select([
            pg_class.c.relname,
            pg_class.c.relnamespace,
            text("'{tag}'".format(tag=self.tag))
        ]).where(
            self.func(pg_class)
        )


class TableTagManager(TagManager):
    """Manages the presence of a table tag in the database."""
    
    def insert_data(self):
        """Insert the column tag into the database."""
        tables = self.env.Table(TABLES, schema=INFORMATION_SCHEMA)
        
        return select([
            tables.c.table_schema,
            tables.c.table_name,
            text("'{tag}'".format(tag=self.tag))
        ]).where(
            self.func(tables)
        )


class ColumnTagManager(TagManager):
    """Manages the presence of a column tag in the database."""
    
    def insert_data(self):
        """Insert the column tag into the database."""
        columns = self.env.Table(COLUMNS, schema=INFORMATION_SCHEMA)
        
        return select([
            columns.c.table_schema,
            columns.c.table_name,
            columns.c.column_name,
            text("'{tag}'".format(tag=self.tag))
        ]).where(
            self.func(columns)
        )
