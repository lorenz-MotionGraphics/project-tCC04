import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import hashlib
from main import open_login_window  # Ensure main.py has open_login_window function


# ---------------------------- PASSWORD HASHING ----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------------------- REGISTRATION WINDOW ----------------------------
def open_registration_window(login_window):
    login_window.withdraw()  # Hide the login window temporarily
    reg_window = ctk.CTkToplevel()
    reg_window.title("Register")
    reg_window.geometry("450x550")
    reg_window.resizable(False, False)

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
            messagebox.showinfo("Success", "Registration successful! Returning to login.")
            reg_window.destroy()
            login_window.deiconify()  # Show the original login window again
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already registered.")
        finally:
            conn.close()

    reg_window.protocol("WM_DELETE_WINDOW", lambda: (reg_window.destroy(), login_window.deiconify()))

    ctk.CTkLabel(reg_window, text="Register New Account", font=("Helvetica", 20, "bold")).pack(pady=20)

    first_name_entry = ctk.CTkEntry(reg_window, width=300, height=40, placeholder_text="First Name", corner_radius=10)
    first_name_entry.pack(pady=(5, 15))

    last_name_entry = ctk.CTkEntry(reg_window, width=300, height=40, placeholder_text="Last Name", corner_radius=10)
    last_name_entry.pack(pady=(5, 15))

    email_entry = ctk.CTkEntry(reg_window, width=300, height=40, placeholder_text="Email", corner_radius=10)
    email_entry.pack(pady=(5, 15))

    phone_entry = ctk.CTkEntry(reg_window, width=300, height=40, placeholder_text="Phone", corner_radius=10)
    phone_entry.pack(pady=(5, 15))

    password_entry = ctk.CTkEntry(reg_window, width=300, height=40, placeholder_text="Password", show='*', corner_radius=10)
    password_entry.pack(pady=(5, 15))

    confirm_password_entry = ctk.CTkEntry(reg_window, width=300, height=40, placeholder_text="Confirm Password", show='*', corner_radius=10)
    confirm_password_entry.pack(pady=(5, 15))

    ctk.CTkButton(
        reg_window, text="Register", width=200, height=40, corner_radius=10,
        command=register_user, fg_color="#4CAF50", hover_color="#45a049"
    ).pack(pady=20)


# ---------------------------- TESTING ----------------------------
if __name__ == "__main__":
    ctk.set_appearance_mode("light")  # or "dark"
    # ctk.deactivate_automatic_theme_update()  # ❌ Remove this line

    root = ctk.CTk()      # Create the main root window
    root.withdraw()       # Hide the root window
    open_registration_window()  # Open the registration window
    root.mainloop()       # Keep the window open
