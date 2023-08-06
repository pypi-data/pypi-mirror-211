def is_there(cur, id: int, name_table: str = "users") -> bool:
    cur.execute(f"SELECT * FROM {name_table} WHERE userid = ?", [id])
    return True if len(cur.fetchall()) > 0 else False
