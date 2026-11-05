
from database import connect_db


# ---------------- BOOK MANAGEMENT ----------------

def add_book(title, author, category, quantity):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO books (title, author, category, quantity)
        VALUES (?, ?, ?, ?)
    """, (title, author, category, quantity))

    conn.commit()
    conn.close()


def get_books():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    conn.close()
    return books


def search_books(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ? OR category LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    books = cursor.fetchall()
    conn.close()

    return books


def update_book(book_id, title, author, category, quantity):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE books
        SET title=?, author=?, category=?, quantity=?
        WHERE book_id=?
    """, (title, author, category, quantity, book_id))

    conn.commit()
    conn.close()


def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM books WHERE book_id=?",
        (book_id,)
    )

    conn.commit()
    conn.close()


# ---------------- STUDENT MANAGEMENT ----------------

def add_student(name, class_name, contact):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students (name, class_name, contact)
        VALUES (?, ?, ?)
    """, (name, class_name, contact))

    conn.commit()
    conn.close()


def get_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()
    return students


def search_students(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM students
        WHERE name LIKE ? OR class_name LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))

    students = cursor.fetchall()
    conn.close()

    return students


def delete_student(student_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id=?",
        (student_id,)
    )

    conn.commit()
    conn.close()

def update_student(student_id, name, class_name, contact):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name=?, class_name=?, contact=?
        WHERE student_id=?
    """, (name, class_name, contact, student_id))

    conn.commit()
    conn.close()


# ---------------- BORROW AND RETURN ----------------

def borrow_book(book_id, student_id, borrow_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT quantity FROM books WHERE book_id=?",
        (book_id,)
    )

    result = cursor.fetchone()

    if result is None or result[0] <= 0:
        conn.close()
        return False

    cursor.execute("""
        INSERT INTO borrow_records
        (book_id, student_id, borrow_date)
        VALUES (?, ?, ?)
    """, (book_id, student_id, borrow_date))

    cursor.execute("""
        UPDATE books
        SET quantity = quantity - 1
        WHERE book_id=?
    """, (book_id,))

    conn.commit()
    conn.close()

    return True


def return_book(borrow_id, return_date):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT book_id FROM borrow_records
        WHERE borrow_id=? AND status='Borrowed'
    """, (borrow_id,))

    result = cursor.fetchone()

    if result is None:
        conn.close()
        return False

    book_id = result[0]

    cursor.execute("""
        UPDATE borrow_records
        SET status='Returned', return_date=?
        WHERE borrow_id=?
    """, (return_date, borrow_id))

    cursor.execute("""
        UPDATE books
        SET quantity = quantity + 1
        WHERE book_id=?
    """, (book_id,))

    conn.commit()
    conn.close()

    return True


def get_borrow_records():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            borrow_records.borrow_id,
            books.title,
            students.name,
            borrow_records.borrow_date,
            borrow_records.return_date,
            borrow_records.status
        FROM borrow_records
        JOIN books ON borrow_records.book_id = books.book_id
        JOIN students ON borrow_records.student_id = students.student_id
    """)

    records = cursor.fetchall()
    conn.close()

    return records
