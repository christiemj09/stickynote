#!/usr/bin/env python
"""
Tag database objects.
"""

import sys

from config import from_config
from ringmaster.sql import DatabaseEnvironment
from stickynote import tag


def main(mgr_class, mgr_kwargs, tags):
    TagManager = getattr(tag, mgr_class)
    with DatabaseEnvironment() as env:
        for tag_data in tags:
            print(tag_data['tag'])
            mgr_kwargs.update(tag_data)
            mgr = TagManager(env=env, **mgr_kwargs)
            mgr.reset()
            mgr.insert()


def console_script():
    from_config(main)(sys.argv[1])


if __name__ == '__main__':
    console_script()
