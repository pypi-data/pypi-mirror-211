def create_table(conn, cur, param: dict, name_table: str = "users") -> None:
    """Пример создания таблицы CREATE TABLE IF NOT EXISTS users(
    userid INT PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    gender TEXT);
    """

    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {name_table}(
   {','.join([t + ' ' + param[t] for t in param])});"""
    )
    conn.commit()
