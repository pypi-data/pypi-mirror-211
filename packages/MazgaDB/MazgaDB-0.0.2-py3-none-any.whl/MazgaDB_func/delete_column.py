def delete_column(
    conn, cur, name_table: str = "users", columns: list = ["userid", "fname", "money"]
) -> None:
    columns = ",".join(columns)
    for request in [
        f"CREATE TABLE new_table AS SELECT {columns} FROM {name_table};",
        f"INSERT INTO new_table SELECT {columns} FROM {name_table};",
        f"DROP TABLE {name_table};",
        f"ALTER TABLE new_table RENAME TO {name_table};",
    ]:
        cur.execute(request)
        conn.commit()
