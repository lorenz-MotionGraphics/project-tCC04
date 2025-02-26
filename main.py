import customtkinter as ctk
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
ADMIN_ACCOUNTS = {
    "kimberly-gajudo": hash_password("kimberly123"),
    "ali-magtaca": hash_password("ali123"),
    "gio-edds": hash_password("gio123"),
    "nyl-mabini": hash_password("nyl123"),
    "eonvhee": hash_password("eonvher123")
}

# ---------------------------- LOGIN WINDOW ----------------------------
def open_login_window():
    ctk.set_appearance_mode("Light")  # Options: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")

    login_window = ctk.CTk()
    login_window.title("Login")
    login_window.geometry("400x500")
    login_window.resizable(False, False)

    # ---------------------------- LOGIN FUNCTION ----------------------------
    def login():
        email = email_entry.get().strip()
        password = password_entry.get()

        if not email or not password:
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if email in ADMIN_ACCOUNTS and hash_password(password) == ADMIN_ACCOUNTS[email]:
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

    # ---------------------------- UI COMPONENTS ----------------------------
    ctk.CTkLabel(
        login_window,
        text="A9EVENT\n Bringing Events to Life, One Click at a Time",
        font=("Segoe UI", 18, "bold"),
        justify="center"
    ).pack(pady=30)

    email_entry = ctk.CTkEntry(
        login_window,
        width=280,
        height=45,
        corner_radius=15,
        placeholder_text="Email"
    )
    email_entry.pack(pady=(10, 20))

    password_entry = ctk.CTkEntry(
        login_window,
        width=280,
        height=45,
        corner_radius=15,
        placeholder_text="Password",
        show="*"
    )
    password_entry.pack(pady=(10, 10))

    # ---------------------------- BUTTONS ----------------------------
    ctk.CTkButton(
        login_window,
        text="Login",
        width=220,
        height=45,
        corner_radius=12,
        command=login,
        fg_color="#4CAF50",
        hover_color="#45a049"
    ).pack(pady=15)

    ctk.CTkButton(
        login_window,
        text="Register",
        width=220,
        height=45,
        corner_radius=12,
        command=open_registration_window,
        fg_color="#2196F3",
        hover_color="#1976D2"
    ).pack(pady=5)

    login_window.mainloop()

# ---------------------------- MAIN PROGRAM ----------------------------
if __name__ == "__main__":
    connect_db()
    open_login_window()
