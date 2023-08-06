import sqlite3
from dataclasses import make_dataclass

from prettytable import from_db_cursor

def __save__(db, class_data, name_table):
    for data in db.accept_columns(name_table):
      db.update_line(name_table=name_table, key1='id', value1=class_data.id, key2=data[0], value2=getattr(class_data, data[0]))

class MazgaDB:
    def __init__(self, db: str, classes: dict = dict()) -> object:
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.db = db
        self.data_class = classes

    def accept_type_columns(self, name_table: str) -> list:
        self.cur.execute('SELECT * FROM sqlite_master')

        for tables in self.cur.fetchall():
            if name_table in tables:
                break
            else:
                raise ValueError('no such table exists')

        columns = [
            column.split()
            for column in tables[-1].split('(')[1].replace(')', '').split(',')
        ]

        return columns

    def accept_columns(self, name_table: str) -> list:
        self.cur.execute('SELECT * FROM sqlite_master')

        for tables in self.cur.fetchall():
            if name_table in tables:
                break
            else:
                raise ValueError('no such table exists')

        columns = [
            column.split()
            for column in tables[-1].split('(')[1].replace(')', '').split(',')
        ]

        columns_tuple = []
        for column in columns:
            columns_tuple.append(
                (column[0], int if 'int' in column[1].lower() else str)
            )
        return columns_tuple

    def create_table(self, name_table: str, param: dict) -> None:
        """
        Пример создания таблицы
        CREATE TABLE IF NOT EXISTS users(
            userid INT PRIMARY KEY,
            fname TEXT,
            lname TEXT,
            gender TEXT);
        :param name_table:
        :param param:
        """

        self.execute(
            f"""CREATE TABLE IF NOT EXISTS {name_table}({','.join([t + ' ' + param[t] for t in param])})"""
        )

    def append_line(self, name_table: str, values: list) -> None:
        self.execute(
            f"""INSERT INTO {name_table} VALUES({','.join(['"' + str(t) + '"' for t in values])});"""
        )

    def update_line(self,
                    name_table: str, key1: str, value1: str, key2: str, value2: str) -> None:
        self.execute(
            f"UPDATE {name_table} SET {key2} = '{value2}' WHERE {key1} = '{value1}'"
        )

    def delete_line(self, name_table: str, key: str, value: str) -> None:
        self.execute(f"""DELETE FROM {name_table} WHERE {key} = '{value}'""")

    def append_column(self, name_table: str, name_column: str, type_column: str) -> None:
        self.execute(
            f"ALTER TABLE {name_table} ADD COLUMN {name_column} '{type_column}'"
        )

    def delete_column(self, name_table: str, column: str) -> None:
        """
        Передайте название столбца который хотите удалить
        :param name_table:
        :param column:
        """

        columns = self.accept_columns(name_table)
        columns.remove(column)

        self.execute(f"CREATE TABLE config AS SELECT {','.join(columns)} FROM {name_table};")
        self.execute(f"DROP TABLE {name_table};")
        self.execute(f"ALTER TABLE config RENAME TO {name_table};")

    def is_there(self, name_table: str, key: str, value: str) -> bool:
        self.cur.execute(f"SELECT * FROM {name_table} WHERE {key} = {value}")
        return len(self.cur.fetchall()) > 0

    def read_table(self, name_table: str, type: str = 's') -> str:
        try:
            self.cur.execute(f"SELECT * FROM {name_table}")
            mytable = from_db_cursor(self.cur)

            if type == 's':
                return str(mytable)
            elif type == 'm':
                counts = len(self.accept_columns(name_table))+1
                table = str(mytable).replace('+', '-', counts).replace('+', '|', counts).replace('+', '-')
                return table
            else:
                raise ValueError("unknown type. There are only two types 's'(string table) and 'm'(Markdown table)")
        except sqlite3.Error as error:
            return error

    def saw_tables(self) -> str:
        """
        Возращает все таблицы из файла
        :return:
        """
        return self.execute("SELECT name FROM sqlite_master WHERE type='table';")

    def select_class(self, name_table: str, key: str, value, class_data=None) -> object:
        data = self.execute(f'SELECT * FROM {name_table} WHERE {key} = {value}')[0]
        if class_data:
            return class_data(*data)
        elif name_table in self.data_class:
            return self.data_class[name_table](*data)
        else:
            class_ = make_dataclass(cls_name=name_table.title(), fields=self.accept_type_columns(name_table), namespace={'__call__': lambda self1: __save__(self, self1, name_table)})
            return class_(*data)

    def select(self, name_table: str, key: str, value):
        """
        Обычный SELECT из sqlite3
        :param name_table:
        :param key:
        :param value:
        :param param:
        """
        return self.execute(f"SELECT * FROM {name_table} WHERE {key} = '{value}'")

    def execute(self, sql_request: str) -> list:
        self.cur.execute(sql_request)
        self.conn.commit()
        return self.cur.fetchall()