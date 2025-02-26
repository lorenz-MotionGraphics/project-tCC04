You're right! The `Events` tab is currently fetching data from the `events` table, but the column names and structure correspond to a **booking** table instead. To fix this, you should:

1. **Rename the table reference** from `events` to `booking` in the `create_crud_tab` call.  
2. **Create a `booking` table** in the database setup if it doesn't exist.

Here’s how to adjust the code:

---

### ✅ **1. Update the Database Setup**  
Add a `booking` table in the `setup_databases` function:

```python
connect_db('events.db', """
    CREATE TABLE IF NOT EXISTS booking (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        event_name TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        location TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        organizer TEXT NOT NULL,
        payment_status TEXT NOT NULL
    )
""")
```

---

### ✅ **2. Fix the `create_crud_tab` Call for Events**  
Replace this:

```python
create_crud_tab(
    notebook, "Events", "events.db", "events",
    columns=["id", "fullname", "event_name", "start_date", "end_date", "Location", "capacity", "organizer", "payment_status"],
    column_labels=["ID", "Full Name", "Event Name", "Start Date", "End Date", "Location", "Capacity", "Organizer", "Payment Status"]
)
```

With this:

```python
create_crud_tab(
    notebook, "Bookings", "events.db", "booking",
    columns=["id", "fullname", "event_name", "start_date", "end_date", "location", "capacity", "organizer", "payment_status"],
    column_labels=["ID", "Full Name", "Event Name", "Start Date", "End Date", "Location", "Capacity", "Organizer", "Payment Status"]
)
```

---

### ✅ **Result:**  
- The **Bookings** tab will now align with the `booking` table structure.  
- Data retrieval and CRUD operations will work correctly.  

Let me know if you need help adjusting the existing `events` table data! 😊