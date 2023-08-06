from .mysqloop import mysqloop

from re import sub as re_sub


class Model(mysqloop):
    _table_name = ''

    def _re_underline_table_name(self, Upstr):
        """
        将大写驼峰转为下划线的表名
        """
        return re_sub('(?<=[a-z])[A-Z]|(?<!^)[A-Z](?=[a-z])', '_\g<0>', Upstr).lower()

    def __init__(self, config=None):
        super().__init__(config)
        self.get_table_name()
        self._set_cursor()

    def get_table_name(self):
        self._table_name = self._table_name if self._table_name is None else self._re_underline_table_name(
            self.__class__.__name__.split('.')[-1])
        return self._table_name

    def set_table_name(self, table_name):
        self._table_name = table_name

    def where(self, column, op=None, value=None, _boolean=" AND"):
        if isinstance(column, dict):
            for cl in column:
                val = column[cl]
                super().where(cl, '=', val)
        elif isinstance(column, list):
            for col in column:
                if isinstance(col, list):
                    col_len = len(col)
                    if col_len == 2:
                        super().where(col[0], col[1])
                    elif col_len == 3:
                        super().where(column=col[0], op=col[1], value=col[2])
                    else:
                        raise Exception("columns type  error")
                elif isinstance(col, dict):
                    for cl in col:
                        super().where(column=cl, op='=', value=col[cl])
                else:
                    raise Exception("columns type error")
        else:
            super().where(column, op, value, _boolean)
        return self

    def updateOrCreate(self, attributes, values: dict):

        if self.where(attributes).exists():
            return self.where(attributes).update(values)
        else:
            return self.create(attributes.update(values))
