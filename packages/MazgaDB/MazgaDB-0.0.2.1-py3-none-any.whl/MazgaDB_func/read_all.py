import sqlite3
from prettytable import from_db_cursor


def read_table(cur, param=None, name_table: str = "users") -> str:
    try:
        cur.execute(f"SELECT {','.join(param) if param else '*'} FROM {name_table}")
        mytable = from_db_cursor(cur)

        return str(mytable)
    except sqlite3.Error as error:
        return error


def saw_tables(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cur.fetchall()
