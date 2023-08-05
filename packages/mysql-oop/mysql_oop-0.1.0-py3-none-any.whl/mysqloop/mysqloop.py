from mysql import connector
from dotenv.main import load_dotenv
import os
load_dotenv()

class mysqloop:
    SPACE_CHARACTER = " "
    SINGLE_QUOTES_CHARACTER = "\'"
    SEMICOLON_CHARACTER = ";"
    EQUAL_SIGN_CHARACTER = "="
    LINE_BREAK_CHARACTER = "\n"
    DIRECTORY_SEPARATOR = "/"

    """
    表名
    """
    _table_name = ""
    __base_where_clause_string = ""
    __base_where_limit_clause_string = ""
    __base_where_orderby_clause_string = ""
    """
    GROUP BY 子句放在 WHERE 子句之后，放在 ORDER BY 子句之前
    """
    __base_where_groupby_clause_string = ""
    """
    与 SELECT 语句一起使用，来消除所有重复的记录，并只获取唯一一次记录
    """
    __base_where_distinct_clause_string = ""
    __base_where_join_clause_string = ""
    __base_where_offset_clause_string = ""
    __operators = [
        "<=>", "=", "!=", "<>", ">", "<", ">=", "<=", "!<", "!>", "!",
        "AND", "BETWEEN", "NOT BETWEEN", "IN", "NOT IN", "LIKE", "EXISTS",
        "GLOB", "NOT", "OR", "XOR", "IS NULL", "IS", "IS NOT", "||", "UNIQUE",
        "REGEXP", "RLIKE",
    ]
    __config = {
        "db_host": os.getenv("DB_HOST"),
        "db_port": os.getenv("DB_PORT"),
        "db_user": os.getenv("DB_USER"),
        "db_password": os.getenv("DB_PASSWORD"),
        "db_name": os.getenv("DB_NAME")
    }

    db = None

    def __init__(self, config=None):
        """
        :param config:
        """

        if config is not None:
            self.__config.update(config)
        self.db = connector.connect(host=self.__config['db_host'], port=self.__config['db_port'],
                                    user=self.__config['db_user'], password=self.__config['db_password'],
                                    database=self.__config['db_name'])

    def connect(self, db_host="127.0.0.1", db_port=3306, db_user="root", db_password=None, db_name="root"):
        self.db = connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            passwd=db_password,
            database=db_name
        )
        print('---db---', self.db)
        return self

    def table(self, table_name):
        """
        设置连接table
        :param table_name:
        :return:
        """
        self._table_name = table_name
        self._set_cursor()
        return self

    def _set_cursor(self):
        self._cursor = self.db.cursor()

    def get_table_name(self):
        return self._table_name

    def __is_tablename(self):
        if len(self._table_name) == 0:
            return "No query form is specified 亲，叫个表吧，求你了！"
        else:
            return True

    def query(self, sql):
        self._cursor.execute(sql)
        columns_tuple = self._cursor.description
        columns_list = [field_tuple[0] for field_tuple in columns_tuple]
        query_result = self._cursor.fetchall()
        columns_len = len(columns_list)
        result = []
        for value in query_result:
            v_n = 0
            item = {}
            while v_n < columns_len:
                item[columns_list[v_n]] = value[v_n]
                v_n += 1
            result.append(item)

        return result

    def select(self, columns="*"):
        if not self.__is_tablename():
            return False

        selected = "SELECT"
        selected += self.SPACE_CHARACTER
        selected += self.__base_where_distinct_clause_string
        selected += self.SPACE_CHARACTER
        selected += columns
        selected += self.SPACE_CHARACTER
        selected += "FROM"
        selected += self.SPACE_CHARACTER
        selected += self._table_name
        selected += self.SPACE_CHARACTER
        selected += self.__base_where_clause_string
        selected += self.__base_where_groupby_clause_string
        selected += self.__base_where_orderby_clause_string
        selected += self.__base_where_limit_clause_string
        selected += self.__base_where_join_clause_string
        selected += self.__base_where_offset_clause_string
        selected += "; "
        result = self.query(selected)
        return result

    def find(self, columns="*"):
        data = self.limit(1).select(columns)
        if data:
            return data[0]
        else:
            return None

    def where(self, column, op, value=None, _boolean=" AND"):
        """
        查询条件
        :param column:
        :param op:
        :param value:
        :param _boolean:
        :return:
        """

        if value is None:
            value = op
            op = "="

        op = str(op)
        value = str(value)

        if len(self.__base_where_clause_string) > 0:
            self.__base_where_clause_string += _boolean
            self.__base_where_clause_string += self.SPACE_CHARACTER

        else:
            self.__base_where_clause_string += "WHERE"
            self.__base_where_clause_string += self.SPACE_CHARACTER
        self.__base_where_clause_string += column
        self.__base_where_clause_string += self.SPACE_CHARACTER
        self.__base_where_clause_string += op
        self.__base_where_clause_string += self.SPACE_CHARACTER
        self.__base_where_clause_string += self.SINGLE_QUOTES_CHARACTER
        self.__base_where_clause_string += str(value)
        self.__base_where_clause_string += self.SINGLE_QUOTES_CHARACTER
        self.__base_where_clause_string += self.SPACE_CHARACTER
        return self

    def limit(self, limit):
        """
        查询数量
        :param limit:
        :return:
        """
        self.__base_where_limit_clause_string = "LIMIT"
        self.__base_where_limit_clause_string += self.SPACE_CHARACTER
        self.__base_where_limit_clause_string += str(limit)
        self.__base_where_limit_clause_string += self.SPACE_CHARACTER
        return self

    def offset(self, offset):
        self.__base_where_offset_clause_string = "OFFSET"
        self.__base_where_offset_clause_string += self.SPACE_CHARACTER
        self.__base_where_offset_clause_string += str(offset)
        self.__base_where_offset_clause_string += self.SPACE_CHARACTER
        return self

    def orderBy(self, column, order):
        self.__base_where_orderby_clause_string = "ORDER BY"
        self.__base_where_orderby_clause_string += self.SPACE_CHARACTER
        self.__base_where_orderby_clause_string += column
        self.__base_where_orderby_clause_string += self.SPACE_CHARACTER
        self.__base_where_orderby_clause_string += order
        self.__base_where_orderby_clause_string += self.SPACE_CHARACTER
        return self

    def groupBy(self, column):
        self.__base_where_groupby_clause_string = "GROUP BY"
        self.__base_where_groupby_clause_string += self.SPACE_CHARACTER
        self.__base_where_groupby_clause_string += column
        self.__base_where_groupby_clause_string += self.SPACE_CHARACTER
        return self

    def distinct(self):
        self.__base_where_distinct_clause_string = "DISTINCT"
        self.__base_where_distinct_clause_string += self.SPACE_CHARACTER
        return self

    def join(self, table, first, op, second, joinType):
        if second == None:
            second = op
            op = "="

        self.__base_where_join_clause_string += self.SPACE_CHARACTER
        self.__base_where_join_clause_string += joinType
        self.__base_where_join_clause_string += self.SPACE_CHARACTER
        self.__base_where_join_clause_string += "JOIN"
        self.__base_where_join_clause_string += self.SPACE_CHARACTER
        self.__base_where_join_clause_string += table
        self.__base_where_join_clause_string += self.SPACE_CHARACTER
        self.__base_where_join_clause_string += "ON"
        self.__base_where_join_clause_string += self.SPACE_CHARACTER
        self.__base_where_join_clause_string += first
        self.__base_where_join_clause_string += self.SPACE_CHARACTER
        self.__base_where_join_clause_string += op
        self.__base_where_join_clause_string += self.SPACE_CHARACTER
        self.__base_where_join_clause_string += second
        self.__base_where_join_clause_string += self.SPACE_CHARACTER
        return self

    def count(self):
        data = self.select("count(*)")
        return data[0]["count(*)"]

    def exists(self):
        return True if self.count() > 0 else False

    def insert(self, columns: dict or list):
        """
        批量插入数据
        :param columns:
        :return:
        """
        # print(type(type(columns)))
        if not isinstance(columns, (list, dict)):
            raise Exception("columns type must be (list or dict )")
        if isinstance(columns, dict):
            self.__instert_o(columns)
            self.db.commit()
            last_id = self._cursor.lastrowid
            return self.where("id", str(last_id)).find()
        else:
            for item in columns:
                self.__instert_o(item)
            self.db.commit()
            if self.db.total_changes > 0:
                return True
            else:
                return False

    def create(self, data: dict):
        """
        创建单条数据
        :param data:
        :return:
        """
        if not isinstance(data, dict):
            raise Exception("columns type must be dict")
        else:
            self.__instert_o(data)
            self.db.commit()
            last_id = self._cursor.lastrowid
            return self.where("id", str(last_id)).find()

    def __instert_o(self, columns):
        """
        set insert sql
        :param columns:
        :return:
        """
        _insert_string = self.__set_insert_string(columns)
        columns_string = _insert_string[0]
        values_tuple = _insert_string[1]
        values_string = _insert_string[2]
        insert = "INSERT INTO "
        insert += self._table_name
        insert += " ( "
        insert += columns_string
        insert += " ) VALUES ( "
        insert += values_string
        insert += "); "
        self._cursor.execute(insert, values_tuple)

    def __set_insert_string(self, columns):
        columns_string = ""
        values_string = ""
        values_tuple = ()
        for column_key, column_value in columns.items():
            columns_string += column_key
            columns_string += ","
            values_tuple += (column_value,)
            values_string += str("%s ")
            values_string += ","

        return columns_string[:-1], values_tuple, values_string[:-1]

    def update(self, datas):
        """
        更新数据 返回被更新的条数
        :param datas:dict
        :return:int
        """
        # if not self.is_table():
        #     return False
        if datas is None:
            return False
        update_string = ""
        for column_key, column_value in datas.items():
            update_string += column_key
            update_string += self.SPACE_CHARACTER
            update_string += self.EQUAL_SIGN_CHARACTER
            update_string += self.SPACE_CHARACTER
            update_string += self.SINGLE_QUOTES_CHARACTER
            update_string += str(column_value)
            update_string += self.SINGLE_QUOTES_CHARACTER
            update_string += ","

        update_string = update_string[:-1]
        update = "UPDATE "
        update += self._table_name
        update += self.SPACE_CHARACTER
        update += "SET"
        update += self.SPACE_CHARACTER
        update += update_string
        update += self.SPACE_CHARACTER
        update += self.__base_where_clause_string
        self._cursor.execute(update)
        self.db.commit()
        return self._cursor.rowcount

    def delete(self):
        delete_data = "DELETE FROM"
        delete_data += self.SPACE_CHARACTER
        delete_data += self._table_name
        delete_data += self.SPACE_CHARACTER
        delete_data += self.__base_where_clause_string
        delete_data += self.SEMICOLON_CHARACTER
        self._cursor.execute(delete_data)
        self.db.commit()

        return self._cursor.rowcount

    def create_table(self, create_columns: dict, primary_key=None):
        """
        创建数据表
        :param create_columns:
        :param primary_key: 主键
        :return:
        """
        # 判断表是否存在
        if self.is_table():
            return self.desc_table()
        if create_columns is None:
            return "map is empty 这啥也没有啊，搞我呢？"
        columns_string = ""
        for column_key, column_value in create_columns.items():
            columns_string += column_key
            columns_string += self.SPACE_CHARACTER
            columns_string += column_value
            columns_string += ","

        # 移除最后一个，
        columns_string = columns_string[:-1]
        created = "CREATE TABLE "
        created += self._table_name
        created += " ( "
        created += columns_string
        if primary_key is not None:
            created += ", PRIMARY KEY ( "
            created += primary_key
            created += " )"
        created += " )ENGINE=InnoDB DEFAULT CHARSET=utf8; "
        try:
            self._cursor.execute(created)
            self.db.commit()
            return self.desc_table()
        except ValueError:
            raise Exception("create table fail!")

    def delete_table(self):
        delete_table = "DROP TABLE"
        delete_table += self.SPACE_CHARACTER
        delete_table += self._table_name
        self._cursor.execute(delete_table)
        self.db.commit()
        if not self.is_table():
            return True
        else:
            return False

    def desc_table(self):
        if not self.is_table():
            return None
        table_name = self._table_name
        sql = "desc " + table_name + ";"
        return self.query(sql)

    def show_table(self):
        table_name = self._table_name
        sql = "SHOW TABLES LIKE '" + table_name + "';"
        result = self.query(sql)
        self._table_name = table_name
        return result

    def show_tables(self):
        sql = "SHOW TABLES;"
        result = self.query(sql)
        return result

    def is_table(self):
        """
        检查表是否存在
        :return: bool
        """
        count = len(self.show_table())
        if count > 0:
            return True
        else:
            return False

    def close(self):
        self.db.close()

    def __del__(self):
        self.close()
