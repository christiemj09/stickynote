"""
Some general-purpose tag functions that define the semantics for tags.
"""

# Application tags can be defined by inheriting from Tag and defining a __call__ method.


from sqlalchemy import func, and_, or_, not_


class Tag(object):
    
    def __init__(self, tag):
        self.tag = tag


class All(Tag):
    
    def __call__(self, *args, **kwargs):
        return True


### Object tags ###


class Contains(Tag):
    
    def __call__(self, pg_class):
        return func.lower(pg_class.c.relname).like('%{tag}%'.format(tag=self.tag.lower()))


class HasRows(Tag):
    
    def __call__(self, pg_class):
        return or_(
            pg_class.c.relkind == 'r',
            pg_class.c.relkind == 'v',
            pg_class.c.relkind == 'm'
        )


class IsTable(Tag):
    
    def __call__(self, pg_class):
        return pg_class.c.relkind == 'r'


class IsView(Tag):
    
    def __call__(self, pg_class):
        return or_(
            pg_class.c.relkind == 'v',
            pg_class.c.relkind == 'm'
        )


class IsMaterialized(Tag):
    
    def __call__(self, pg_class):
        return or_(
            pg_class.c.relkind == 'r',
            pg_class.c.relkind == 'm'
        )


### Table tags ###


class TableContains(Tag):
    
    def __call__(self, tables):
        return func.lower(tables.c.table_name).like('%{tag}%'.format(tag=self.tag.lower()))


### Column tags ###


class IsNumber(Tag):
    
    def __call__(self, columns):
        return or_(
            columns.c.data_type == 'real',
            columns.c.data_type == 'numeric',
            columns.c.data_type.like('%int%')
        )


class IsText(Tag):
    
    def __call__(self, columns):
        return or_(
            columns.c.data_type == 'text',
            columns.c.data_type.like('%char%')
        )


class IsId(Tag):
    
    def __call__(self, columns):
        return func.lower(columns.c.column_name).like('%id')


class IsInt(Tag):
    
    def __call__(self, columns):
        return columns.c.data_type.like('%int%')


class IsTime(Tag):
    
    def __call__(self, columns):
        return or_(
            columns.c.data_type == 'date',
            columns.c.data_type.like('%time%')
        )


class IsDate(Tag):
    
    def __call__(self, columns):
        return or_(
            columns.c.data_type == 'date',
            func.lower(columns.c.column_name).like('%dt%'),
            func.lower(columns.c.column_name).like('%data%')
        )

  
class IsTimestamp(Tag):
    
    def __call__(self, columns):
        return columns.c.data_type.like('timestamp%')
