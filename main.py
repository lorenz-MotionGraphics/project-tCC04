import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
from user import open_user_window

try:
    from admin import open_admin_window
except ImportError:
    def open_admin_window():
        messagebox.showerror("Error", "Admin module not found.")

# ---------------------------- DATABASE SETUP ----------------------------

def connect_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# ---------------------------- PASSWORD HASHING ----------------------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------- ADMIN EMAIL ----------------------------

ADMIN_EMAIL = "admin@example.com"  # Change this to the actual admin email

# ---------------------------- LOGIN WINDOW ----------------------------

def open_login_window():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("350x300")
    login_window.resizable(False, False)

    def login():
        email = email_entry.get().strip()
        password = password_entry.get()

        if not email or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hash_password(password)))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", f"Welcome {user[1]} {user[2]}!")
            login_window.destroy()
            
            if email == ADMIN_EMAIL:
                try:
                    open_admin_window()  # Redirect to admin window if email matches admin
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to open admin window: {e}")
            else:
                open_user_window()   # Redirect to user window for other users
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    def open_registration_window():
        login_window.destroy()
        try:
            from register import open_registration_window  # Import to avoid circular imports
            open_registration_window()
        except ImportError:
            messagebox.showerror("Error", "Registration module not found.")

    tk.Label(login_window, text="Email:").pack(pady=10)
    email_entry = tk.Entry(login_window, width=30)
    email_entry.pack()

    tk.Label(login_window, text="Password:").pack(pady=10)
    password_entry = tk.Entry(login_window, width=30, show='*')
    password_entry.pack()

    tk.Button(login_window, text="Login", width=15, command=login).pack(pady=15)
    tk.Button(login_window, text="Register", width=15, command=open_registration_window).pack()

    login_window.mainloop()

# ---------------------------- MAIN PROGRAM ----------------------------

if __name__ == "__main__":
    connect_db()
    open_login_window()
