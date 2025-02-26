#BEFORE USING SOFTWARE PLEASE BE ADVISED OF THE LICENSE WRITTEN IN THE SETUP WIZARD
#OLCA122A009 - Final Project - PYTHON PROGRAMMING LANGUAGE

import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
from utils import set_icon

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
    set_icon(payment_window)
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



# ✅ Update booking data
def update_booking(booking_id):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute("SELECT fullname, event_name, start_date, end_date, location, capacity, organizer FROM bookings WHERE id=?", (booking_id,))
    booking = cursor.fetchone()
    conn.close()

    if not booking:
        messagebox.showerror("Error", "Booking not found.")
        return

    update_window = tk.Toplevel()
    set_icon(update_window)
    update_window.title("Update Booking")
    update_window.geometry("400x400")

    labels = ["Full Name:", "Event Name:", "Start Date:", "End Date:", "Location:", "Capacity:", "Organizer:"]
    entries = []

    for i, label_text in enumerate(labels):
        tk.Label(update_window, text=label_text).grid(row=i, column=0, sticky=tk.W, pady=5, padx=10)
        entry = tk.Entry(update_window, width=30)
        entry.grid(row=i, column=1, pady=5)
        entry.insert(0, booking[i])
        entries.append(entry)

    def submit_update():
        updated_values = [entry.get().strip() for entry in entries]
        if not all(updated_values):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        try:
            capacity_int = int(updated_values[5])
        except ValueError:
            messagebox.showwarning("Input Error", "Capacity must be a number.")
            return

        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE bookings SET fullname=?, event_name=?, start_date=?, end_date=?, location=?, capacity=?, organizer=? 
            WHERE id=?
        """, (*updated_values, booking_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Booking updated successfully.")
        refresh_booking_table()
        update_window.destroy()

    tk.Button(update_window, text="Update", command=submit_update).grid(row=7, column=1, pady=20)

# ✅ Delete booking data
def delete_booking(booking_id):
    if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this booking?"):
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Booking deleted successfully.")
        refresh_booking_table()

# ✅ Handle right-click menu
def show_right_click_menu(event):
    row_id = booking_table.identify_row(event.y)
    if row_id:
        booking_table.selection_set(row_id)  # Select the row under the cursor
        booking_table.focus(row_id)          # Set focus to that row

        booking = booking_table.item(row_id, 'values')
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM bookings WHERE fullname=? AND event_name=? AND start_date=?", (booking[0], booking[1], booking[2]))
        record = cursor.fetchone()
        conn.close()

        if not record:
            messagebox.showerror("Error", "Booking not found.")
            return

        booking_id = record[0]
        menu = tk.Menu(booking_table, tearoff=0)
        menu.add_command(label="Update", command=lambda: update_booking(booking_id))
        menu.add_command(label="Delete", command=lambda: delete_booking(booking_id))
        menu.post(event.x_root, event.y_root)  # Show context menu at cursor position


# ✅ User dashboard with sorting, filtering, and right-click menu
def open_user_window():
    connect_events_db()
    connect_payments_db()

    user_window = tk.Tk()
    set_icon(user_window)
    user_window.title("User Dashboard")
    user_window.geometry("1000x650")
    user_window.configure(bg="#f4f6f9")  # Light background for modern look

    # ✅ Modern ttk styles
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#f9f9f9",
                    foreground="#333",
                    rowheight=30,
                    fieldbackground="#f9f9f9",
                    font=("Segoe UI", 10))
    style.configure("Treeview.Heading",
                    background="#4a7ebb",
                    foreground="white",
                    font=("Segoe UI", 11, "bold"),
                    padding=8)
    style.map("Treeview",
              background=[('selected', '#6c8cd5')],
              foreground=[('selected', 'white')])

    # 📝 Form Section
    form_frame = tk.Frame(user_window, padx=10, pady=10, bg="#f4f6f9")
    form_frame.pack(side=tk.TOP, fill=tk.X)

    labels = ["Full Name:", "Event Name:", "Start Date:", "End Date:", "Location:", "No. of Guests:", "Organizer:"]
    global fullname_entry, event_name_entry, start_date_entry, end_date_entry, location_entry, capacity_entry, organizer_entry

    entry_widgets = []
    entry_fields = [
        tk.Entry(form_frame, width=30),
        tk.Entry(form_frame, width=30),
        DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd'),
        DateEntry(form_frame, width=28, date_pattern='yyyy-mm-dd'),
        tk.Entry(form_frame, width=30),
        tk.Entry(form_frame, width=30),
        tk.Entry(form_frame, width=30)
    ]

    for i, label_text in enumerate(labels):
        tk.Label(form_frame, text=label_text, bg="#f4f6f9", font=("Segoe UI", 10)).grid(row=i, column=0, sticky=tk.W, pady=3, padx=5)
        entry_fields[i].grid(row=i, column=1, pady=3, padx=5)
    fullname_entry, event_name_entry, start_date_entry, end_date_entry, location_entry, capacity_entry, organizer_entry = entry_fields

    tk.Button(form_frame, text="Book Event", command=book_event, bg="#4a7ebb", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT).grid(row=7, column=1, pady=10)

    # 🧹 Filter & Sort Section
    filter_sort_frame = tk.Frame(user_window, padx=10, pady=5, bg="#f4f6f9")
    filter_sort_frame.pack(fill=tk.X)

    tk.Label(filter_sort_frame, text="Filter:", bg="#f4f6f9", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0, 5))
    global filter_entry
    filter_entry = tk.Entry(filter_sort_frame, width=30)
    filter_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(filter_sort_frame, text="Sort By:", bg="#f4f6f9", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(10, 5))
    global sort_option
    sort_option = ttk.Combobox(filter_sort_frame, values=["None", "fullname", "event_name", "start_date", "end_date", "payment_status"], state="readonly", width=15)
    sort_option.set("None")
    sort_option.pack(side=tk.LEFT, padx=5)

    global ascending_var
    ascending_var = tk.BooleanVar(value=True)
    tk.Checkbutton(filter_sort_frame, text="Ascending", variable=ascending_var, bg="#f4f6f9", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=5)

    tk.Button(filter_sort_frame, text="Apply", command=refresh_booking_table, bg="#4a7ebb", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT).pack(side=tk.LEFT, padx=10)

    # 📊 Table Section
    table_frame = tk.Frame(user_window, bg="#f4f6f9")
    table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    columns = ("Full Name", "Event Name", "Start Date", "End Date", "Location", "Capacity", "Organizer", "Payment Status")
    global booking_table
    booking_table = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')

    # ✅ Style columns and add row striping
    for col in columns:
        booking_table.heading(col, text=col)
        booking_table.column(col, anchor=tk.CENTER, width=120)

    booking_table.tag_configure('oddrow', background="#e7eff6")
    booking_table.tag_configure('evenrow', background="#fdfdfd")

    booking_table.pack(fill=tk.BOTH, expand=True)
    booking_table.bind("<Double-1>", handle_payment)
    booking_table.bind("<Button-3>", show_right_click_menu)

    # 🌈 Hover effect
    def on_row_hover(event):
        row_id = booking_table.identify_row(event.y)
        if row_id:
            booking_table.tag_configure('hover', background="#d1e0ff")
            booking_table.item(row_id, tags=('hover',))

    booking_table.bind("<Motion>", on_row_hover)

    refresh_booking_table()
    user_window.mainloop()

# ✅ Refresh booking table
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

    for index, booking in enumerate(bookings):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        booking_table.insert('', 'end', values=booking, tags=(tag,))

    booking_table.config(height=min(max(len(bookings), 5), 15))


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

if __name__ == "__main__":
    open_user_window()