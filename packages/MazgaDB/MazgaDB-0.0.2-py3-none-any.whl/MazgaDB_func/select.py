from bot_func import *


def select(cur, id: int, param: str = "*", name_table: str = "users") -> None:
    cur.execute(f"SELECT {param} FROM {name_table} WHERE userid = {id}")
    user = cur.fetchall()[0]
    return People(user[0], user[1], user[2])
