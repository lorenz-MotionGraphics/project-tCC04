# 🎯 **Event Booking Application - Project Documentation**

---

## 📝 **Project Overview**  
The **Event Booking Application** is a **GUI-based software** built using **Python’s Tkinter** for the user interface and **SQLite** for persistent data storage. This system facilitates user authentication, event booking, and role-based access for users and administrators. It is designed to streamline event registrations and provide a clear separation between user functionalities and admin privileges.

---

## 🏗️ **Project Structure**  
```
project-tCC04/
├── main.py        # Entry point: Handles login and registration routing.
├── register.py    # User registration window and logic.
├── user.py        # User dashboard: Event booking and booking display.
├── admin.py       # Admin dashboard: (Handles admin-specific functions.)
├── users.db       # Database storing user credentials and details.
├── events.db      # Database storing event bookings.
├── main.spec
├── payments.db
├── logo.png
├── app_icon.png
├── LICENSE.txt
├── utils.py
├── .gitignore
├── event/
└── __pycache__/   # Python cache files (auto-generated).
```

---

## ⚙️ **Technologies Used**  
- **Programming Language:** Python 3.13  
- **GUI Framework:** Tkinter, Customtkinter
- **Database:** SQLite3  

---

## 🧩 **Features and Functionalities**  
### 1️⃣ **User Authentication System:**
- **Registration:** Users can register by providing their first name, last name, email, phone number, and password.
- **Password Security:** Passwords are securely hashed using SHA-256 before storage.
- **Login System:** Validates user credentials and redirects based on user roles.
- **Role-Based Access:**
  - **Admin:** Accesses the admin dashboard when logging in with the predefined admin email.
  - **User:** Accesses the user dashboard upon successful login.

### 2️⃣ **User Dashboard (`user.py`):**
- **Event Booking Form:** Users can book events by providing:
  - Full Name  
  - Event Name  
  - Start Date  
  - End Date  
  - Location  
  - No. Of Guest
  - Organizer  
- **Bookings Display:** Booked events are presented in a table format with a "Payment" button for future payment integration.
- **Data Persistence:** Event bookings are saved in a separate `events.db` database for efficient data management.

### 3️⃣ **Admin Dashboard (`admin.py`):**
- View all user bookings.
- Manage user accounts and events.
- Potential future features: editing or deleting bookings, user analytics.

---

## 🚀 **Development Workflow**  
### ✅ **Implemented:**  
- User registration with form validations and password hashing.  
- Login system with role-based access control.  
- Event booking interface with data persistence.  
- Automatic database table creation if missing.  

### 🧪 **Testing:**  
- Registered users can log in and access the user dashboard.  
- Admin login redirects to the admin dashboard.  
- Event bookings display correctly in the booking table.  
- Robust error handling for missing tables and invalid inputs.  

---

## 🏆 **Professional Software Engineering Practices Used:**  
- **Modular Code Structure:** Separated code into logical modules (`main.py`, `user.py`, `admin.py`, `register.py`) for maintainability.  
- **Security:** Implemented password hashing to ensure user data security.  
- **Error Handling:** Comprehensive error checks for database operations and user inputs.  
- **Scalability:** Separated databases for users and bookings to improve data management.  
- **User Experience:** Clean Tkinter interfaces with clear navigation between windows.  
- **Documentation:** Well-commented code and structured documentation for future scalability and collaboration.  

---
## 🙌 **Conclusion:**  
This project demonstrates a practical application of software development principles using Python. It successfully integrates a GUI, a relational database, and role-based functionalities, offering a solid foundation for event management systems.

**Please Run This Code in the Previleged/Administrator Command Line:**
```
pip3 install customtkinter tkcalendar sqlite3
```

---
![Capture9](https://github.com/user-attachments/assets/491b521e-a787-4fc5-9a80-65f94017e1f9)
![Capture8](https://github.com/user-attachments/assets/7b03a5a6-7c68-4b39-9c68-3b99480a0466)
![Capture7](https://github.com/user-attachments/assets/c4a154ae-a90c-4769-b857-e5c5ddd83cb3)
![Capture6](https://github.com/user-attachments/assets/7e67f439-21cb-4d40-9609-1e7c134a3252)
![Capture5](https://github.com/user-attachments/assets/e37bf9de-c13d-4db4-813c-c7b4a41ec97d)
![Capture4](https://github.com/user-attachments/assets/761cd16e-9f38-4a64-bc65-787d8bab203a)
![Capture3](https://github.com/user-attachments/assets/9f6630ad-b22a-4d25-9a4e-fbeafccb3e87)
![Capture2](https://github.com/user-attachments/assets/362c6157-60e5-471a-bb1b-c3ec953eee0a)
![Capture](https://github.com/user-attachments/assets/c4653b2a-6dd4-45c9-9bd5-ca99bd1f1d45)
