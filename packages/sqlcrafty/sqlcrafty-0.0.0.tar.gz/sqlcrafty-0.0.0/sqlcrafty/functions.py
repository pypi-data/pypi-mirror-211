import sqlite3

DATABASE_NAME = 'database.db'


def create_table(table_name: str, scheme: dict):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = f"CREATE TABLE IF NOT EXISTS {table_name} ("

    for field, field_type in scheme.items():
        query += f"{field} {field_type.to_sql()}, "

    query = query.rstrip(", ") + ")"
    cursor.execute(query)

    conn.commit()
    conn.close()


def add_data(table: str, **kwargs: any):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    fields = ', '.join(kwargs.keys())
    placeholders = ', '.join(['?'] * len(kwargs))
    query = f"INSERT INTO {table} ({fields}) VALUES ({placeholders})"
    cursor.execute(query, tuple(kwargs.values()))

    conn.commit()
    conn.close()


def add_data_ignore_duplicates(table, **kwargs):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    fields = ', '.join(kwargs.keys())
    placeholders = ', '.join(['?'] * len(kwargs))
    query = f"INSERT OR IGNORE INTO {table} ({fields}) VALUES ({placeholders})"
    cursor.execute(query, tuple(kwargs.values()))

    conn.commit()
    conn.close()


def update_data(table, update_fields, **kwargs):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    set_values = ', '.join([f"{field} = ?" for field in update_fields])
    query = f"UPDATE {table} SET {set_values} WHERE "
    params = []

    for key, value in kwargs.items():
        query += f"{key} = ? AND "
        params.append(value)
    query = query.rstrip("AND ")

    cursor.execute(query, tuple(params))

    conn.commit()
    conn.close()


def filter_data(table, **kwargs):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table} WHERE "
    params = list()

    for key, value in kwargs.items():
        query += f"{key} = ? AND "
        params.append(value)

    query = query.strip("AND ")
    cursor.execute(query, params)

    results = cursor.fetchall()
    conn.close()

    return results


def get_first(table, **kwargs):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table} WHERE "
    params = list()

    for key, value in kwargs.items():
        query += f"{key} = ? AND "
        params.append(value)

    query = query.strip("AND ")
    cursor.execute(query, params)

    results = cursor.fetchone()
    conn.close()

    return results


def advance_filter(table, fields, **kwargs):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    fields_str = ', '.join(fields)
    query = f"SELECT {fields_str} FROM {table} WHERE "
    params = list()

    for key, value in kwargs.items():
        query += f"{key} = ? AND "
        params.append(value)

    query = query.rstrip("AND ")
    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results


def get_first_filter(table, fields, **kwargs):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    fields_str = ', '.join(fields)
    query = f"SELECT {fields_str} FROM {table} WHERE "
    params = list()

    for key, value in kwargs.items():
        query += f"{key} = ? AND "
        params.append(value)

    query = query.rstrip("AND ")
    cursor.execute(query, params)
    results = cursor.fetchone()

    conn.close()
    return results


def drop_table(table_name):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = f"DROP TABLE IF EXISTS {table_name}"
    cursor.execute(query)

    conn.commit()
    conn.close()


def get_tables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    results = cursor.fetchall()
    tables = [row[0] for row in results]

    conn.close()

    return tables


def get_all_data(table_name):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    results = cursor.fetchall()

    conn.close()
    return results


def delete_data(table, **kwargs):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = f"DELETE FROM {table} WHERE "
    params = list()

    conditions = []
    for key, value in kwargs.items():
        conditions.append(f"{key} = ?")
        params.append(value)

    query += " AND ".join(conditions)

    cursor.execute(query, params)

    conn.commit()
    conn.close()


def count_records(table):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = f"SELECT COUNT(*) FROM {table}"
    cursor.execute(query)
    count = cursor.fetchone()[0]

    conn.close()

    return count


def execute_query(query, params=None):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    results = cursor.fetchall()
    conn.close()

    return results
