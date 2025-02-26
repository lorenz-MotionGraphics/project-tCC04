import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3

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

    # Clear form fields after successful booking
    fullname_entry.delete(0, tk.END)
    event_name_entry.delete(0, tk.END)
    location_entry.delete(0, tk.END)
    capacity_entry.delete(0, tk.END)
    organizer_entry.delete(0, tk.END)


def refresh_booking_table():
    booking_table.delete(*booking_table.get_children())  # Clear the table

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    bookings = cursor.fetchall()
    conn.close()

    for booking in bookings:
        booking_table.insert('', 'end', values=booking[1:])

    # Adjust table height
    row_count = len(bookings)
    booking_table.config(height=min(max(row_count, 5), 15))

def open_user_window():
    connect_events_db()

    user_window = tk.Tk()
    user_window.title("User Dashboard")
    user_window.geometry("950x600")

    form_frame = tk.Frame(user_window, padx=10, pady=10)
    form_frame.pack(side=tk.TOP, fill=tk.X)

    # Labels and Entries
    labels = ["Full Name:", "Event Name:", "Start Date:", "End Date:", "Location:", "Capacity:", "Organizer:"]
    for i, label_text in enumerate(labels):
        tk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=2)

    global fullname_entry, event_name_entry, start_date_entry, end_date_entry, location_entry, capacity_entry, organizer_entry

    fullname_entry = tk.Entry(form_frame, width=30)
    event_name_entry = tk.Entry(form_frame, width=30)
    start_date_entry = DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd')
    end_date_entry = DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd')
    location_entry = tk.Entry(form_frame, width=30)
    capacity_entry = tk.Entry(form_frame, width=30)
    organizer_entry = tk.Entry(form_frame, width=30)

    # Position entries
    fullname_entry.grid(row=0, column=1, pady=2)
    event_name_entry.grid(row=1, column=1, pady=2)
    start_date_entry.grid(row=2, column=1, pady=2)
    end_date_entry.grid(row=3, column=1, pady=2)
    location_entry.grid(row=4, column=1, pady=2)
    capacity_entry.grid(row=5, column=1, pady=2)
    organizer_entry.grid(row=6, column=1, pady=2)

    tk.Button(form_frame, text="Book Event", command=book_event).grid(row=7, column=1, pady=10)

    # Booking Table
    table_frame = tk.Frame(user_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("Full Name", "Event Name", "Start Date", "End Date", "Location", "Capacity", "Organizer")
    global booking_table
    booking_table = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)

    for col in columns:
        booking_table.heading(col, text=col)
        booking_table.column(col, width=130, anchor=tk.CENTER)

    booking_table.pack(fill=tk.BOTH, expand=True)
    refresh_booking_table()

    user_window.mainloop()

if __name__ == "__main__":
    open_user_window()
