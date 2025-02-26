import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3

# Connect to the database and ensure the table exists
def connect_events_db():
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            event_name TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            location TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            organizer TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Book an event and save to the database
def book_event():
    fullname = fullname_entry.get().strip()
    event_name = event_name_entry.get().strip()
    start_date = start_date_entry.get_date().strftime('%Y-%m-%d')
    end_date = end_date_entry.get_date().strftime('%Y-%m-%d')
    location = location_entry.get().strip()
    capacity = capacity_entry.get().strip()
    organizer = organizer_entry.get().strip()

    if not all([fullname, event_name, start_date, end_date, location, capacity, organizer]):
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        capacity_int = int(capacity)
    except ValueError:
        messagebox.showwarning("Input Error", "Capacity must be a number.")
        return

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (fullname, event_name, start_date, end_date, location, capacity, organizer)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (fullname, event_name, start_date, end_date, location, capacity_int, organizer))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Event booked successfully!")
    refresh_booking_table()
    clear_form()

# Clear form entries after booking
def clear_form():
    fullname_entry.delete(0, tk.END)
    event_name_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    capacity_entry.delete(0, tk.END)
    organizer_entry.delete(0, tk.END)

# Refresh and display the booking table with optional filters
def refresh_booking_table():
    for item in booking_table.get_children():
        booking_table.delete(item)

    filter_field = filter_field_var.get()
    filter_value = filter_entry.get().strip()

    query = "SELECT * FROM bookings"
    params = ()

    if filter_field and filter_value:
        column_map = {
            "Full Name": "fullname",
            "Event Name": "event_name",
            "Organizer": "organizer"
        }
        db_column = column_map.get(filter_field)
        if db_column:
            query += f" WHERE {db_column} LIKE ?"
            params = (f"%{filter_value}%",)

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    bookings = cursor.fetchall()
    conn.close()

    for booking in bookings:
        booking_table.insert('', 'end', values=booking[1:])

    new_height = min(max(len(bookings), 5), 15)
    booking_table.config(height=new_height)

# Sort the table based on column header clicks
def sort_column(col, reverse):
    data = [(booking_table.set(child, col), child) for child in booking_table.get_children('')]
    try:
        data.sort(key=lambda x: int(x[0]), reverse=reverse) if col == "Capacity" else data.sort(key=lambda x: x[0], reverse=reverse)
    except ValueError:
        data.sort(key=lambda x: x[0], reverse=reverse)

    for index, (val, child) in enumerate(data):
        booking_table.move(child, '', index)

    booking_table.heading(col, command=lambda: sort_column(col, not reverse))

# Create the main user window
def open_user_window():
    connect_events_db()

    user_window = tk.Tk()
    user_window.title("User Dashboard")
    user_window.geometry("950x650")

    # Form Frame
    form_frame = tk.Frame(user_window, padx=10, pady=10)
    form_frame.pack(side=tk.TOP, fill=tk.X)

    labels = ["Full Name:", "Event Name:", "Start Date:", "End Date:", "Location:", "Capacity:", "Organizer:"]
    for i, text in enumerate(labels):
        tk.Label(form_frame, text=text).grid(row=i, column=0, sticky=tk.W, pady=2)

    global fullname_entry, event_name_entry, start_date_entry, end_date_entry, location_entry, capacity_entry, organizer_entry

    fullname_entry = tk.Entry(form_frame, width=30)
    event_name_entry = tk.Entry(form_frame, width=30)
    start_date_entry = DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd')
    end_date_entry = DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd')
    location_entry = tk.Entry(form_frame, width=30)
    capacity_entry = tk.Entry(form_frame, width=30)
    organizer_entry = tk.Entry(form_frame, width=30)

    entries = [fullname_entry, event_name_entry, start_date_entry, end_date_entry, location_entry, capacity_entry, organizer_entry]
    for i, entry in enumerate(entries):
        entry.grid(row=i, column=1, pady=2)

    tk.Button(form_frame, text="Book Event", command=book_event).grid(row=7, column=1, pady=10)

    # Filter Frame
    filter_frame = tk.Frame(user_window, padx=10, pady=10)
    filter_frame.pack(fill=tk.X)

    tk.Label(filter_frame, text="Filter by:").pack(side=tk.LEFT)
    global filter_field_var, filter_entry

    filter_field_var = tk.StringVar()
    filter_dropdown = ttk.Combobox(filter_frame, textvariable=filter_field_var, values=["Full Name", "Event Name", "Organizer"], width=15, state='readonly')
    filter_dropdown.pack(side=tk.LEFT, padx=5)

    filter_entry = tk.Entry(filter_frame, width=20)
    filter_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(filter_frame, text="Apply Filter", command=refresh_booking_table).pack(side=tk.LEFT, padx=5)
    tk.Button(filter_frame, text="Clear Filter", command=lambda: [filter_field_var.set(''), filter_entry.delete(0, tk.END), refresh_booking_table()]).pack(side=tk.LEFT, padx=5)

    # Table Frame
    table_frame = tk.Frame(user_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("Full Name", "Event Name", "Start Date", "End Date", "Location", "Capacity", "Organizer")
    global booking_table

    booking_table = ttk.Treeview(table_frame, columns=columns, show='headings')

    for col in columns:
        booking_table.heading(col, text=col, command=lambda c=col: sort_column(c, False))
        booking_table.column(col, width=120)

    booking_table.pack(fill=tk.BOTH, expand=True)
    refresh_booking_table()

    user_window.mainloop()

if __name__ == "__main__":
    open_user_window()
