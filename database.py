
import sqlite3
import os

# Create the data folder if it does not exist
os.makedirs("data", exist_ok=True)

# Database location
DB_NAME = os.path.join("data", "library.db")


def connect_db():
    """Connect to the library database."""
    return sqlite3.connect(DB_NAME)


def create_tables():
    """Create all required database tables."""

    conn = connect_db()
    cursor = conn.cursor()

    # Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT,
            quantity INTEGER NOT NULL
        )
    """)

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_name TEXT NOT NULL,
            contact TEXT
        )
    """)

    # Borrowing records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrow_records (
            borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            borrow_date TEXT NOT NULL,
            return_date TEXT,
            status TEXT DEFAULT 'Borrowed',
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database and tables created successfully!")
