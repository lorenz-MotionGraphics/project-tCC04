import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def open_registration_window():
    reg_window = tk.Toplevel()
    reg_window.title("Register")
    reg_window.geometry("450x500")
    reg_window.configure(bg="#f5f5f5")
    reg_window.resizable(False, False)

    def style_label(text):
        return tk.Label(reg_window, text=text, font=("Helvetica", 12, "bold"), bg="#f5f5f5")

    def style_entry():
        return tk.Entry(reg_window, width=30, font=("Helvetica", 11), bd=2, relief="groove")

    def register_user():
        first_name = first_name_entry.get().strip()
        last_name = last_name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not all([first_name, last_name, email, phone, password, confirm_password]):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, phone, password)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, email, phone, hash_password(password)))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! You can now log in.")
            reg_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already registered.")
        finally:
            conn.close()

    tk.Label(reg_window, text="Register New Account", font=("Helvetica", 16, "bold"), bg="#f5f5f5").pack(pady=20)

    style_label("First Name:").pack(pady=(10, 5))
    first_name_entry = style_entry()
    first_name_entry.pack()

    style_label("Last Name:").pack(pady=(10, 5))
    last_name_entry = style_entry()
    last_name_entry.pack()

    style_label("Email:").pack(pady=(10, 5))
    email_entry = style_entry()
    email_entry.pack()

    style_label("Phone:").pack(pady=(10, 5))
    phone_entry = style_entry()
    phone_entry.pack()

    style_label("Password:").pack(pady=(10, 5))
    password_entry = style_entry()
    password_entry.config(show='*')
    password_entry.pack()

    style_label("Confirm Password:").pack(pady=(10, 5))
    confirm_password_entry = style_entry()
    confirm_password_entry.config(show='*')
    confirm_password_entry.pack()

    tk.Button(
        reg_window, text="Register", width=20, command=register_user,
        font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", bd=0, pady=8, activebackground="#45a049"
    ).pack(pady=20)

    reg_window.mainloop()
