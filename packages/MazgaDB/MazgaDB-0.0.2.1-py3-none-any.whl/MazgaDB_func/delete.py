def delete(conn, cur, id: int, name_table: str = "users") -> None:
    cur.execute(f"""DELETE from {name_table} where userid = {id}""")
    conn.commit()
