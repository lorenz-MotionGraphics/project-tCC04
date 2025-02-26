import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime

# ✅ Connect to events database and ensure table exists
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
            organizer TEXT NOT NULL,
            payment_status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()
    conn.close()

# ✅ Connect to payments database and ensure table exists
def connect_payments_db():
    conn = sqlite3.connect('payments.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER NOT NULL,
            payment_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_date TEXT NOT NULL,
            FOREIGN KEY (booking_id) REFERENCES bookings(id)
        )
    """)
    conn.commit()
    conn.close()

# ✅ Payment form window
def open_payment_window(booking):
    payment_window = tk.Toplevel()
    payment_window.title("Payment Details")
    payment_window.geometry("400x320")

    booking_id, fullname, event_name, start_date, end_date, location, capacity, organizer, payment_status = booking

    tk.Label(payment_window, text=f"Booking for: {fullname}", font=("Arial", 10, "bold")).pack(pady=5)
    tk.Label(payment_window, text=f"Event: {event_name} ({start_date} to {end_date})").pack(pady=2)

    tk.Label(payment_window, text="Payment Amount:").pack(anchor=tk.W, padx=20, pady=5)
    payment_amount_entry = tk.Entry(payment_window)
    payment_amount_entry.pack(padx=20, fill=tk.X)

    tk.Label(payment_window, text="Payment Method:").pack(anchor=tk.W, padx=20, pady=5)
    payment_method_combo = ttk.Combobox(payment_window, values=["Cash", "Card", "Online"], state="readonly")
    payment_method_combo.set("Cash")
    payment_method_combo.pack(padx=20, fill=tk.X)

    tk.Label(payment_window, text="Payment Date:").pack(anchor=tk.W, padx=20, pady=5)
    payment_date_entry = DateEntry(payment_window, width=20, date_pattern='yyyy-mm-dd')
    payment_date_entry.set_date(datetime.today())
    payment_date_entry.pack(padx=20, fill=tk.X)

    def submit_payment():
        payment_amount = payment_amount_entry.get().strip()
        payment_method = payment_method_combo.get()
        payment_date = payment_date_entry.get_date().strftime('%Y-%m-%d')

        if not payment_amount:
            messagebox.showwarning("Input Error", "Please enter the payment amount.")
            return

        try:
            amount = float(payment_amount)
        except ValueError:
            messagebox.showwarning("Input Error", "Payment amount must be a valid number.")
            return

        conn = sqlite3.connect('payments.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO payments (booking_id, payment_amount, payment_method, payment_date)
            VALUES (?, ?, ?, ?)
        """, (booking_id, amount, payment_method, payment_date))
        conn.commit()
        conn.close()

        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE bookings SET payment_status='Paid' WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Payment recorded successfully.")
        refresh_booking_table()
        payment_window.destroy()

    tk.Button(payment_window, text="Submit Payment", command=submit_payment).pack(pady=15)

# ✅ Handle double-click to open payment form
def handle_payment(event):
    selected = booking_table.focus()
    if not selected:
        return

    booking = booking_table.item(selected, 'values')
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, fullname, event_name, start_date, end_date, location, capacity, organizer, payment_status
        FROM bookings
        WHERE fullname=? AND event_name=? AND start_date=?
    """, (booking[0], booking[1], booking[2]))
    booking_record = cursor.fetchone()
    conn.close()

    if booking_record:
        open_payment_window(booking_record)
    else:
        messagebox.showerror("Error", "Booking not found.")

# ✅ Book event
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
    cursor.execute("""
        INSERT INTO bookings (fullname, event_name, start_date, end_date, location, capacity, organizer, payment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
    """, (fullname, event_name, start_date, end_date, location, capacity_int, organizer))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Event booked successfully!")
    refresh_booking_table()

    for entry in [fullname_entry, event_name_entry, location_entry, capacity_entry, organizer_entry]:
        entry.delete(0, tk.END)

# ✅ Refresh and apply filters to the booking table
def refresh_booking_table():
    for item in booking_table.get_children():
        booking_table.delete(item)

    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()

    filter_text = filter_entry.get().strip().lower()
    sort_by = sort_option.get()
    sort_order = 'ASC' if ascending_var.get() else 'DESC'

    query = "SELECT fullname, event_name, start_date, end_date, location, capacity, organizer, payment_status FROM bookings"
    params = []

    if filter_text:
        query += " WHERE LOWER(fullname) LIKE ? OR LOWER(event_name) LIKE ? OR LOWER(payment_status) LIKE ?"
        params = [f"%{filter_text}%"] * 3

    if sort_by != "None":
        query += f" ORDER BY {sort_by} {sort_order}"

    cursor.execute(query, params)
    bookings = cursor.fetchall()
    conn.close()

    for booking in bookings:
        booking_table.insert('', 'end', values=booking)

    booking_table.config(height=min(max(len(bookings), 5), 15))

# ✅ User dashboard with sorting and filtering
def open_user_window():
    connect_events_db()
    connect_payments_db()

    user_window = tk.Tk()
    user_window.title("User Dashboard")
    user_window.geometry("1000x650")

    form_frame = tk.Frame(user_window, padx=10, pady=10)
    form_frame.pack(side=tk.TOP, fill=tk.X)

    labels = ["Full Name:", "Event Name:", "Start Date:", "End Date:", "Location:", "No. of Guests:", "Organizer:"]
    for i, label in enumerate(labels):
        tk.Label(form_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)

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

    filter_sort_frame = tk.Frame(user_window, padx=10, pady=5)
    filter_sort_frame.pack(fill=tk.X)

    tk.Label(filter_sort_frame, text="Filter:").pack(side=tk.LEFT, padx=(0, 5))
    global filter_entry
    filter_entry = tk.Entry(filter_sort_frame, width=30)
    filter_entry.pack(side=tk.LEFT)

    tk.Label(filter_sort_frame, text="Sort By:").pack(side=tk.LEFT, padx=(10, 5))
    global sort_option
    sort_option = ttk.Combobox(filter_sort_frame, values=["None", "fullname", "event_name", "start_date", "end_date", "payment_status"], state="readonly", width=15)
    sort_option.set("None")
    sort_option.pack(side=tk.LEFT)

    global ascending_var
    ascending_var = tk.BooleanVar(value=True)
    tk.Checkbutton(filter_sort_frame, text="Ascending", variable=ascending_var).pack(side=tk.LEFT, padx=5)

    tk.Button(filter_sort_frame, text="Apply", command=refresh_booking_table).pack(side=tk.LEFT, padx=10)

    table_frame = tk.Frame(user_window)
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("Full Name", "Event Name", "Start Date", "End Date", "Location", "Capacity", "Organizer", "Payment Status")
    global booking_table
    booking_table = ttk.Treeview(table_frame, columns=columns, show='headings')

    for col in columns:
        booking_table.heading(col, text=col)
        booking_table.column(col, width=120, anchor=tk.CENTER)

    booking_table.pack(fill=tk.BOTH, expand=True)
    booking_table.bind("<Double-1>", handle_payment)

    refresh_booking_table()
    user_window.mainloop()

if __name__ == "__main__":
    open_user_window()
