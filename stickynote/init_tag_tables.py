"""
Initialize tables that stickynote can populate.
"""

# DDL for each class defined in tag.py (minus the base class).

import sys

from sqlalchemy import Table, Column, Text
from config import from_config
from ringmaster.sql import DatabaseEnvironment


TAG_TABLE_COLUMNS = {
    'object': ['relname', 'relnamespace', 'tag'],
    'table': ['table_schema', 'table_name', 'tag'],
    'column': ['table_schema', 'table_name', 'column_name', 'tag'],
}


def main(objects):
    with DatabaseEnvironment() as env:
        # Define tables
        tables = [
            Table(
                obj['table'],
                env.meta,
                *(Column(name, Text, nullable=True) for name in TAG_TABLE_COLUMNS[obj['type']]),
                schema=obj['schema']
            )
            for obj in objects
        ]
        # Create tables
        env.meta.create_all(env.engine)


def console_script():
    from_config(main)(sys.argv[1])


if __name__ == '__main__':
    console_script()
