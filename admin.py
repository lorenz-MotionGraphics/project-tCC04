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

def fetch_data(db_name, table_name, filter_col=None, filter_val=None, sort_col=None, sort_order="ASC"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name}"
    params = []

    if filter_col and filter_val:
        query += f" WHERE {filter_col} LIKE ?"
        params.append(f"%{filter_val}%")

    if sort_col:
        query += f" ORDER BY {sort_col} {sort_order}"

    cursor.execute(query, params)
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

def refresh_tree(tree, data):
    tree.delete(*tree.get_children())
    for row in data:
        tree.insert('', tk.END, values=row)

def create_crud_tab(notebook, title, db_name, table_name, columns, column_labels):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=title)

    # Filter and Sort Controls
    control_frame = ttk.Frame(frame)
    control_frame.pack(fill='x', pady=5)

    ttk.Label(control_frame, text="Filter by:").pack(side='left', padx=5)
    filter_col = ttk.Combobox(control_frame, values=column_labels[1:], state="readonly")
    filter_col.pack(side='left', padx=5)

    filter_entry = ttk.Entry(control_frame)
    filter_entry.pack(side='left', padx=5)

    ttk.Label(control_frame, text="Sort by:").pack(side='left', padx=5)
    sort_col = ttk.Combobox(control_frame, values=column_labels, state="readonly")
    sort_col.pack(side='left', padx=5)

    sort_order = ttk.Combobox(control_frame, values=["ASC", "DESC"], state="readonly")
    sort_order.set("ASC")
    sort_order.pack(side='left', padx=5)

    def refresh():
        data = fetch_data(
            db_name, table_name,
            filter_col=columns[column_labels.index(filter_col.get())] if filter_col.get() else None,
            filter_val=filter_entry.get() if filter_entry.get() else None,
            sort_col=columns[column_labels.index(sort_col.get())] if sort_col.get() else None,
            sort_order=sort_order.get()
        )
        refresh_tree(tree, data)

    ttk.Button(control_frame, text="Apply", command=refresh).pack(side='left', padx=5)
    ttk.Button(control_frame, text="Clear", command=lambda: [filter_col.set(''), filter_entry.delete(0, tk.END), sort_col.set(''), sort_order.set("ASC"), refresh()]).pack(side='left', padx=5)

    # Data Table
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col, label in zip(columns, column_labels):
        tree.heading(col, text=label)
        tree.column(col, width=100)
    tree.pack(pady=10, expand=True, fill='both')

    # CRUD Buttons
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=10)

    def add_entry():
        values = [simpledialog.askstring("Input", f"Enter {label}:") for label in column_labels[1:]]
        if None in values:
            return
        insert_data(db_name, table_name, ', '.join(columns[1:]), values)
        messagebox.showinfo("Success", "Entry added successfully.")
        refresh()

    def update_entry():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry to update.")
            return
        item = tree.item(selected, 'values')
        updated_values = [simpledialog.askstring("Update", f"Update {label} (current: {item[idx]}):", initialvalue=item[idx]) for idx, label in enumerate(column_labels[1:], 1)]
        if None in updated_values:
            return
        update_data(db_name, table_name, ', '.join([f"{col} = ?" for col in columns[1:]]), f"{columns[0]} = ?", updated_values + [item[0]])
        messagebox.showinfo("Success", "Entry updated.")
        refresh()

    def delete_entry():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select an entry to delete.")
            return
        item = tree.item(selected, 'values')
        if messagebox.askyesno("Confirm", f"Delete {title[:-1]} ID {item[0]}?"):
            delete_data(db_name, table_name, f"{columns[0]} = ?", item[0])
            messagebox.showinfo("Deleted", "Entry deleted.")
            refresh()

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
    admin_window.geometry("900x700")
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

# ---------------------------- MAIN ----------------------------
if __name__ == "__main__":
    open_admin_window()
