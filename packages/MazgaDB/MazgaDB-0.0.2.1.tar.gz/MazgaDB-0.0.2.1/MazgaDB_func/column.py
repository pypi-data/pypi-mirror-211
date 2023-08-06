def append_column(
    conn, cur, name_column: str, type_column: str, name_table: str = "users"
) -> None:
    cur.execute(f"alter table {name_table} add column {name_column} '{type_column}'")
    conn.commit()
