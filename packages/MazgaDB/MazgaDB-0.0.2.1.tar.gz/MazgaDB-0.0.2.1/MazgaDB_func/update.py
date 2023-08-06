def update(
    conn, cur, key1: str, value1: str, key2: str, value2: str, name_table: str = "users"
) -> None:
    cur.execute(
        f"UPDATE {name_table} SET {key2} = '{value2}' WHERE {key1} = '{value1}' "
    )
    conn.commit()
