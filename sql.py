import sqlite3

def fix_payments_table():
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()

    columns_to_add = [
        ("method", "TEXT"),
        ("date", "TEXT"),
    ]

    for column_name, column_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE payments ADD COLUMN {column_name} {column_type};")
            print(f"Added column: {column_name}")
        except sqlite3.OperationalError:
            print(f"Column '{column_name}' already exists.")

    conn.commit()
    conn.close()

fix_payments_table()
