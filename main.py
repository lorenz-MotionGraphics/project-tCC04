import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

try:
    from admin import open_admin_window
except ImportError:
    def open_admin_window():
        messagebox.showerror("Error", "Admin module not found.")

try:
    from user import open_user_window
except ImportError:
    def open_user_window():
        messagebox.showerror("Error", "User module not found.")

try:
    from register import open_registration_window
except ImportError:
    def open_registration_window():
        messagebox.showerror("Error", "Registration module not found.")

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

# ---------------------------- ADMIN CREDENTIALS ----------------------------
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = hash_password("admin123")

# ---------------------------- LOGIN WINDOW ----------------------------
def open_login_window():
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.geometry("400x400")
    login_window.configure(bg="#f5f5f5")
    login_window.resizable(False, False)

    def style_label(text):
        return tk.Label(login_window, text=text, font=("Helvetica", 12, "bold"), bg="#f5f5f5")

    def style_entry():
        return tk.Entry(login_window, width=30, font=("Helvetica", 11), bd=2, relief="groove")

    def style_button(text, command, color="#4CAF50"):
        return tk.Button(
            login_window, text=text, width=20, command=command,
            font=("Helvetica", 11, "bold"), bg=color, fg="white", bd=0, pady=8, activebackground="#45a049"
        )

    def login():
        email = email_entry.get().strip()
        password = password_entry.get()

        if not email or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if email == ADMIN_EMAIL and hash_password(password) == ADMIN_PASSWORD:
            messagebox.showinfo("Success", "Welcome Admin!")
            login_window.destroy()
            open_admin_window()
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, hash_password(password)))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", f"Welcome {user[1]} {user[2]}!")
            login_window.destroy()
            open_user_window()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    tk.Label(login_window, text="Welcome! Please Login", font=("Helvetica", 16, "bold"), bg="#f5f5f5").pack(pady=20)

    style_label("Email:").pack(pady=(10, 5))
    email_entry = style_entry()
    email_entry.pack()

    style_label("Password:").pack(pady=(10, 5))
    password_entry = style_entry()
    password_entry.config(show='*')
    password_entry.pack()

    style_button("Login", login).pack(pady=20)
    style_button("Register", open_registration_window, color="#2196F3").pack()

    login_window.mainloop()

# ---------------------------- MAIN PROGRAM ----------------------------
if __name__ == "__main__":
    connect_db()
    open_login_window()
