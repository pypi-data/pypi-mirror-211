def append(conn, cur, values: list, name_table: str = "users") -> None:
    cur.execute(
        f"""INSERT INTO {name_table} VALUES({','.join(['"' + str(t) + '"' for t in values])});"""
    )
    conn.commit()
