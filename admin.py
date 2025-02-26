import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

# ---------------------------- DATABASE SETUP ----------------------------

def connect_db(db_name, table_sql):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(table_sql)
    conn.commit()
    conn.close()

def setup_databases():
    connect_db('users.db', """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connect_db('events.db', """
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            event_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            location TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            organizer TEXT NOT NULL,
            payment_status TEXT DEFAULT 'Pending'
        )
    """)

    connect_db('payments.db', """
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            method TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

# ---------------------------- CRUD OPERATIONS ----------------------------

def fetch_data(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def insert_data(db_name, table_name, columns, values):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    placeholders = ', '.join(['?'] * len(values))
    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
    conn.commit()
    conn.close()

def update_data(db_name, table_name, set_clause, condition, values):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {condition}", values)
    conn.commit()
    conn.close()

def delete_data(db_name, table_name, condition, value):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}", (value,))
    conn.commit()
    conn.close()

# ---------------------------- GUI COMPONENTS ----------------------------

def refresh_tree(tree, data, columns):
    tree.delete(*tree.get_children())
    for row in data:
        tree.insert('', tk.END, values=row)

def create_crud_tab(notebook, title, db_name, table_name, columns, column_labels):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=title)

    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col, label in zip(columns, column_labels):
        tree.heading(col, text=label)
        tree.column(col, width=100)
    tree.pack(pady=10, expand=True, fill='both')

    def refresh():
        data = fetch_data(db_name, table_name)
        refresh_tree(tree, data, columns)

    def add_entry():
        values = []
        for label in column_labels[1:]:
            val = simpledialog.askstring("Input", f"Enter {label}:")
            if val is None:
                return
            values.append(val)
        insert_data(db_name, table_name, ', '.join(columns[1:]), values)
        messagebox.showinfo("Success", "Entry added successfully.")
        refresh()

    def update_entry():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry to update.")
            return
        item = tree.item(selected, 'values')
        updated_values = []
        for idx, label in enumerate(column_labels[1:], start=1):
            val = simpledialog.askstring("Update", f"Update {label} (current: {item[idx]}):", initialvalue=item[idx])
            if val is None:
                return
            updated_values.append(val)
        update_data(db_name, table_name, ', '.join([f"{col} = ?" for col in columns[1:]]), f"{columns[0]} = ?", updated_values + [item[0]])
        messagebox.showinfo("Success", "Entry updated.")
        refresh()

    def delete_entry():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry to delete.")
            return
        item = tree.item(selected, 'values')
        if messagebox.askyesno("Confirm Delete", f"Delete {title[:-1]} ID {item[0]}?"):
            delete_data(db_name, table_name, f"{columns[0]} = ?", item[0])
            messagebox.showinfo("Deleted", "Entry deleted.")
            refresh()

    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Add", command=add_entry).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Update", command=update_entry).grid(row=0, column=1, padx=5)
    ttk.Button(button_frame, text="Delete", command=delete_entry).grid(row=0, column=2, padx=5)
    ttk.Button(button_frame, text="Refresh", command=refresh).grid(row=0, column=3, padx=5)

    refresh()

# ---------------------------- ADMIN WINDOW ----------------------------

def open_admin_window():
    setup_databases()

    admin_window = tk.Tk()
    admin_window.title("Admin Dashboard")
    admin_window.geometry("800x600")
    admin_window.resizable(True, True)

    notebook = ttk.Notebook(admin_window)
    notebook.pack(expand=True, fill='both')

    create_crud_tab(
        notebook, "Users", "users.db", "users",
        columns=["id", "first_name", "last_name", "email", "phone", "password"],
        column_labels=["ID", "First Name", "Last Name", "Email", "Phone", "Password"]
    )

    create_crud_tab(
        notebook, "Bookings", "events.db", "bookings",
        columns=["id", "fullname", "event_name", "start_date", "end_date", "location", "capacity", "organizer", "payment_status"],
        column_labels=["ID", "Full Name", "Event Name", "Start Date", "End Date", "Location", "Capacity", "Organizer", "Payment Status"]
    )

    create_crud_tab(
        notebook, "Payments", "payments.db", "payments",
        columns=["id", "user_id", "amount", "method", "date"],
        column_labels=["ID", "User ID", "Amount", "Method", "Date"]
    )

    ttk.Button(admin_window, text="Logout", command=admin_window.destroy).pack(pady=10)
    admin_window.mainloop()

# ---------------------------- MAIN TEST ----------------------------
if __name__ == "__main__":
    open_admin_window()
