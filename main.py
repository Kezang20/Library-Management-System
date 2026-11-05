
import sys

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel, QStackedWidget,
    QTableWidget, QTableWidgetItem, QLineEdit,
    QMessageBox, QInputDialog, QFrame, QDialog,
    QFormLayout
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPalette, QColor, QAction

from database import create_tables
import library_logic as logic


class LibraryManagementSystem(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Library Management System | Kezang Dema | Roll No: 12")
        self.setMinimumSize(1000, 650)
        self.resize(1200, 750)

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #FCE4EC;
                color: #38232D;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QFrame#sidebar {
                background-color: #713B50;
                border: none;
            }

            QLabel#logo {
            color: maroon;
            font-size: 18px;
            font-weight: bold;
            padding: 25px 12px;
            }

            QPushButton#nav {
                background-color: transparent;
                color: #FFF7FA;
                border: none;
                text-align: left;
                padding: 14px 20px;
                font-size: 14px;
            }

            QPushButton#nav:hover {
                background-color: #925D73;
                border-left: 4px solid #F4B6C8;
            }

            QPushButton#action {
                background-color: #A95776;
                color: white;
                border: none;
                padding: 10px 18px;
                border-radius: 7px;
                font-weight: bold;
            }

            QPushButton#action:hover {
                background-color: #713B50;
            }

            QLabel#heading {
                font-size: 25px;
                font-weight: bold;
                color: #713B50;
            }

            QLabel#card {
                background-color: #FFF7FA;
                color: #713B50;
                border: 1px solid #EAC2D0;
                border-radius: 12px;
                padding: 20px;
                font-size: 17px;
                font-weight: bold;
            }

            QLineEdit {
                background-color: white;
                color: #38232D;
                border: 1px solid #D9A5B7;
                border-radius: 7px;
                padding: 10px;
            }

            QLineEdit:focus {
                border: 2px solid #A95776;
            }

            QTableWidget {
                background-color: #FFF7FA;
                alternate-background-color: #F9EAF0;
                color: #38232D;
                border: 1px solid #EAC2D0;
                gridline-color: #F0D5DF;
                border-radius: 8px;
            }

            QTableWidget::item:selected {
                background-color: #E8B4C6;
                color: #38232D;
            }

            QHeaderView::section {
                background-color: #713B50;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
            }
        """)

        self.setup_ui()
        self.create_menu_bar()
        self.refresh_all()

            # ---------------- MENU BAR ----------------

    def create_menu_bar(self):

        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(exit_action)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)

        help_menu.addAction(about_action)

    def show_about(self):

        QMessageBox.about(
            self,
            "About Library Management System",
            """
            Library Management System

            Developed by: Kezang Dema
            Roll Number: 12

            Framework: PyQt6
            Database: SQLite

            This application manages books,
            student records, borrowing and returns.
            """
        )


    # ---------------- MAIN INTERFACE ----------------

    def setup_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        side_layout = QVBoxLayout(sidebar)

        logo = QLabel("LIBRARY\nMANAGEMENT SYSTEM")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setWordWrap(True)
        side_layout.addWidget(logo)

        menu_items = [
            ("Dashboard", 0),
            ("Books", 1),
            ("Students", 2),
            ("Issue Books", 3),
            ("Records", 4)
        ]

        for name, index in menu_items:

            button = QPushButton(name)
            button.setObjectName("nav")
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            button.clicked.connect(
                lambda checked=False, i=index:
                self.pages.setCurrentIndex(i)
            )

            side_layout.addWidget(button)

        side_layout.addStretch()

        self.pages = QStackedWidget()

        self.pages.addWidget(self.dashboard_page())
        self.pages.addWidget(self.books_page())
        self.pages.addWidget(self.students_page())
        self.pages.addWidget(self.issue_page())
        self.pages.addWidget(self.records_page())

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

    # ---------------- HELPER FUNCTIONS ----------------

    def create_heading(self, text):

        label = QLabel(text)
        label.setObjectName("heading")

        return label

    def create_table(self, headers):

        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        table.setAlternatingRowColors(True)

        table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        table.horizontalHeader().setStretchLastSection(True)

        return table

    def fill_table(self, table, records):

        table.setRowCount(0)

        for record in records:

            row = table.rowCount()
            table.insertRow(row)

            for column, value in enumerate(record):

                item = QTableWidgetItem(
                    str(value) if value is not None else ""
                )

                table.setItem(row, column, item)

        table.resizeColumnsToContents()

    def selected_id(self, table):

        row = table.currentRow()

        if row < 0:

            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select a record first."
            )

            return None

        return int(table.item(row, 0).text())

    def get_text(self, title, label):

        value, ok = QInputDialog.getText(
            self, title, label
        )

        return value.strip(), ok

    # ---------------- DASHBOARD ----------------

    def dashboard_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        layout.addWidget(
            self.create_heading("Dashboard")
        )

        welcome = QLabel(
            "Welcome to the Library Management System."
        )

        welcome.setStyleSheet(
            "color: #925D73; font-size: 15px;"
        )

        layout.addWidget(welcome)

        self.book_card = QLabel("Total Book Titles: 0")
        self.student_card = QLabel("Registered Students: 0")
        self.borrowed_card = QLabel(
            "Books Currently Borrowed: 0"
        )

        for card in [
            self.book_card,
            self.student_card,
            self.borrowed_card
        ]:

            card.setObjectName("card")
            card.setMinimumHeight(90)

            card.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            layout.addWidget(card)

        layout.addStretch()

        return page

    # ---------------- BOOK MANAGEMENT ----------------

    def books_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        layout.addWidget(
            self.create_heading("Book Management")
        )

        self.book_search = QLineEdit()

        self.book_search.setPlaceholderText(
            "Search by title, author or category..."
        )

        self.book_search.textChanged.connect(
            self.search_book_records
        )

        layout.addWidget(self.book_search)

        self.book_table = self.create_table([
            "ID", "Title", "Author", "Category", "Quantity"
        ])

        layout.addWidget(self.book_table)

        buttons = QHBoxLayout()

        add_btn = QPushButton("Add Book")
        edit_btn = QPushButton("Edit Book")
        delete_btn = QPushButton("Delete Book")

        for btn in [add_btn, edit_btn, delete_btn]:

            btn.setObjectName("action")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            buttons.addWidget(btn)

        add_btn.clicked.connect(self.add_book)
        edit_btn.clicked.connect(self.edit_book)
        delete_btn.clicked.connect(self.delete_book)

        layout.addLayout(buttons)

        return page

    # ---------------- ADD BOOK ----------------

    def add_book(self):

        dialog = QDialog(self)
        dialog.setObjectName("addBookDialog")
        dialog.setWindowTitle("Add New Book")
        dialog.setFixedSize(430, 380)

        dialog.setStyleSheet("""
            QDialog#addBookDialog {
                background-color: #FCE4EC;
            }

            QDialog#addBookDialog QLabel {
                background-color: transparent;
                color: #713B50;
                font-size: 14px;
                font-weight: bold;
            }

            QDialog#addBookDialog QLineEdit {
                background-color: #FFFFFF;
                color: #38232D;
                border: 1px solid #C98DA5;
                border-radius: 7px;
                padding: 10px;
                min-height: 22px;
                selection-background-color: #A95776;
                selection-color: white;
            }

            QDialog#addBookDialog QLineEdit:focus {
                background-color: #FFFFFF;
                color: #38232D;
                border: 2px solid #A95776;
            }

            QDialog#addBookDialog QPushButton {
                background-color: #A95776;
                color: white;
                border: none;
                padding: 11px;
                border-radius: 7px;
                font-weight: bold;
            }

            QDialog#addBookDialog QPushButton:hover {
                background-color: #713B50;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(14)

        heading = QLabel("Enter Book Details")
        heading.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #713B50;
            padding-bottom: 5px;
        """)

        layout.addWidget(heading)

        form = QFormLayout()
        form.setSpacing(12)

        title_input = QLineEdit()
        title_input.setPlaceholderText("Enter book title")

        author_input = QLineEdit()
        author_input.setPlaceholderText("Enter author name")

        category_input = QLineEdit()
        category_input.setPlaceholderText("Enter book category")

        quantity_input = QLineEdit()
        quantity_input.setPlaceholderText("Enter quantity")

        for field in [
            title_input,
            author_input,
            category_input,
            quantity_input
        ]:

            field.setReadOnly(False)
            field.setEnabled(True)
            field.setMinimumHeight(42)

            palette = field.palette()
            palette.setColor(
                QPalette.ColorRole.Base, QColor("#FFFFFF")
            )
            palette.setColor(
                QPalette.ColorRole.Text, QColor("#38232D")
            )
            palette.setColor(
                QPalette.ColorRole.PlaceholderText,
                QColor("#987080")
            )
            palette.setColor(
                QPalette.ColorRole.Highlight, QColor("#A95776")
            )
            palette.setColor(
                QPalette.ColorRole.HighlightedText,
                QColor("#FFFFFF")
            )

            field.setPalette(palette)

        form.addRow("Book Title:", title_input)
        form.addRow("Author:", author_input)
        form.addRow("Category:", category_input)
        form.addRow("Quantity:", quantity_input)

        layout.addLayout(form)

        save_btn = QPushButton("Save Book")
        cancel_btn = QPushButton("Cancel")

        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)

        def save_book():

            title = title_input.text().strip()
            author = author_input.text().strip()
            category = category_input.text().strip()
            quantity_text = quantity_input.text().strip()

            if not title or not author or not category or not quantity_text:

                QMessageBox.warning(
                    dialog,
                    "Missing Information",
                    "Please fill in all the fields."
                )

                return

            try:
                quantity = int(quantity_text)

            except ValueError:

                QMessageBox.warning(
                    dialog,
                    "Invalid Input",
                    "Quantity must be a valid whole number."
                )

                quantity_input.setFocus()
                return

            if quantity <= 0 or quantity > 10000:

                QMessageBox.warning(
                    dialog,
                    "Invalid Quantity",
                    "Quantity must be between 1 and 10000."
                )

                quantity_input.setFocus()
                return

            try:

                logic.add_book(
                    title,
                    author,
                    category,
                    quantity
                )

                dialog.accept()
                self.refresh_all()

                QMessageBox.information(
                    self,
                    "Success",
                    "Book added successfully!"
                )

            except Exception as e:

                QMessageBox.critical(
                    dialog, "Error", str(e)
                )

        save_btn.clicked.connect(save_book)
        cancel_btn.clicked.connect(dialog.reject)

        title_input.setFocus()
        dialog.exec()

    def edit_book(self):

        book_id = self.selected_id(self.book_table)

        if book_id is None:
            return

        row = self.book_table.currentRow()

        title, ok = QInputDialog.getText(
            self, "Edit Book", "Book title:",
            text=self.book_table.item(row, 1).text()
        )

        if not ok or not title.strip():
            return

        author, ok = QInputDialog.getText(
            self, "Edit Book", "Author:",
            text=self.book_table.item(row, 2).text()
        )

        if not ok or not author.strip():
            return

        category, ok = QInputDialog.getText(
            self, "Edit Book", "Category:",
            text=self.book_table.item(row, 3).text()
        )

        if not ok:
            return

        quantity, ok = QInputDialog.getInt(
            self,
            "Edit Book",
            "Total available quantity:",
            int(self.book_table.item(row, 4).text()),
            0,
            10000
        )

        if not ok:
            return

        try:

            logic.update_book(
                book_id,
                title.strip(),
                author.strip(),
                category.strip(),
                quantity
            )

            self.refresh_all()

            QMessageBox.information(
                self, "Success",
                "Book updated successfully!"
            )

        except Exception as e:

            QMessageBox.critical(
                self, "Error", str(e)
            )

    def delete_book(self):

        book_id = self.selected_id(self.book_table)

        if book_id is None:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this book?"
        )

        if confirm == QMessageBox.StandardButton.Yes:

            try:

                logic.delete_book(book_id)
                self.refresh_all()

                QMessageBox.information(
                    self, "Success",
                    "Book deleted successfully!"
                )

            except Exception as e:

                QMessageBox.critical(
                    self, "Error", str(e)
                )

    def search_book_records(self, keyword):

        records = logic.search_books(keyword)

        self.fill_table(
            self.book_table, records
        )

    # ---------------- STUDENT MANAGEMENT ----------------

    def students_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        layout.addWidget(
            self.create_heading("Student Management")
        )

        self.student_search = QLineEdit()

        self.student_search.setPlaceholderText(
            "Search students by name or class..."
        )

        self.student_search.textChanged.connect(
            self.search_student_records
        )

        layout.addWidget(self.student_search)

        self.student_table = self.create_table([
            "ID", "Name", "Class", "Contact"
        ])

        layout.addWidget(self.student_table)

        buttons = QHBoxLayout()

        add_btn = QPushButton("Add Student")
        edit_btn = QPushButton("Edit Student")
        delete_btn = QPushButton("Delete Student")

        for btn in [add_btn, edit_btn, delete_btn]:

            btn.setObjectName("action")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            buttons.addWidget(btn)

        add_btn.clicked.connect(self.add_student)
        edit_btn.clicked.connect(self.edit_student)
        delete_btn.clicked.connect(self.delete_student)

        layout.addLayout(buttons)

        return page

    # ---------------- ADD STUDENT ----------------

    def add_student(self):

        dialog = QDialog(self)
        dialog.setObjectName("addStudentDialog")
        dialog.setWindowTitle("Register New Student")
        dialog.setFixedSize(430, 330)

        dialog.setStyleSheet("""
            QDialog#addStudentDialog {
                background-color: #FCE4EC;
            }

            QDialog#addStudentDialog QLabel {
                background-color: transparent;
                color: #713B50;
                font-size: 14px;
                font-weight: bold;
            }

            QDialog#addStudentDialog QLineEdit {
                background-color: #FFFFFF;
                color: #38232D;
                border: 1px solid #C98DA5;
                border-radius: 7px;
                padding: 10px;
                min-height: 22px;
                selection-background-color: #A95776;
                selection-color: white;
            }

            QDialog#addStudentDialog QLineEdit:focus {
                background-color: #FFFFFF;
                color: #38232D;
                border: 2px solid #A95776;
            }

            QDialog#addStudentDialog QPushButton {
                background-color: #A95776;
                color: white;
                border: none;
                padding: 11px;
                border-radius: 7px;
                font-weight: bold;
            }

            QDialog#addStudentDialog QPushButton:hover {
                background-color: #713B50;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(14)

        heading = QLabel("Enter Student Details")
        heading.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #713B50;
            padding-bottom: 5px;
        """)

        layout.addWidget(heading)

        form = QFormLayout()
        form.setSpacing(12)

        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter student name")

        class_input = QLineEdit()
        class_input.setPlaceholderText("Enter class")

        contact_input = QLineEdit()
        contact_input.setPlaceholderText("Enter contact number")

        for field in [
            name_input,
            class_input,
            contact_input
        ]:

            field.setReadOnly(False)
            field.setEnabled(True)
            field.setMinimumHeight(42)

            palette = field.palette()

            palette.setColor(
                QPalette.ColorRole.Base, QColor("#FFFFFF")
            )
            palette.setColor(
                QPalette.ColorRole.Text, QColor("#38232D")
            )
            palette.setColor(
                QPalette.ColorRole.PlaceholderText,
                QColor("#987080")
            )
            palette.setColor(
                QPalette.ColorRole.Highlight, QColor("#A95776")
            )
            palette.setColor(
                QPalette.ColorRole.HighlightedText,
                QColor("#FFFFFF")
            )

            field.setPalette(palette)

        form.addRow("Student Name:", name_input)
        form.addRow("Class:", class_input)
        form.addRow("Contact:", contact_input)

        layout.addLayout(form)

        save_btn = QPushButton("Save Student")
        cancel_btn = QPushButton("Cancel")

        layout.addWidget(save_btn)
        layout.addWidget(cancel_btn)

        def save_student():

            name = name_input.text().strip()
            class_name = class_input.text().strip()
            contact = contact_input.text().strip()

            if not name or not class_name or not contact:

                QMessageBox.warning(
                    dialog,
                    "Missing Information",
                    "Please fill in all the fields."
                )

                return

            try:

                logic.add_student(
                    name,
                    class_name,
                    contact
                )

                dialog.accept()
                self.refresh_all()

                QMessageBox.information(
                    self,
                    "Success",
                    "Student registered successfully!"
                )

            except Exception as e:

                QMessageBox.critical(
                    dialog, "Error", str(e)
                )

        save_btn.clicked.connect(save_student)
        cancel_btn.clicked.connect(dialog.reject)

        name_input.setFocus()
        dialog.exec()

    # ---------------- EDIT STUDENT ----------------

    def edit_student(self):

        student_id = self.selected_id(
            self.student_table
        )

        if student_id is None:
            return

        row = self.student_table.currentRow()

        current_name = self.student_table.item(row, 1).text()
        current_class = self.student_table.item(row, 2).text()
        current_contact = self.student_table.item(row, 3).text()

        name, ok = QInputDialog.getText(
            self, "Edit Student", "Student name:",
            text=current_name
        )

        if not ok:
            return

        if not name.strip():

            QMessageBox.warning(
                self, "Error", "Name cannot be empty."
            )

            return

        class_name, ok = QInputDialog.getText(
            self, "Edit Student", "Class:",
            text=current_class
        )

        if not ok:
            return

        if not class_name.strip():

            QMessageBox.warning(
                self, "Error", "Class cannot be empty."
            )

            return

        contact, ok = QInputDialog.getText(
            self, "Edit Student", "Contact:",
            text=current_contact
        )

        if not ok:
            return

        try:

            logic.update_student(
                student_id,
                name.strip(),
                class_name.strip(),
                contact.strip()
            )

            self.refresh_all()

            QMessageBox.information(
                self, "Success",
                "Student details updated successfully!"
            )

        except Exception as e:

            QMessageBox.critical(
                self, "Error", str(e)
            )

    def delete_student(self):

        student_id = self.selected_id(
            self.student_table
        )

        if student_id is None:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this student?"
        )

        if confirm == QMessageBox.StandardButton.Yes:

            try:

                logic.delete_student(student_id)
                self.refresh_all()

                QMessageBox.information(
                    self, "Success",
                    "Student deleted successfully!"
                )

            except Exception as e:

                QMessageBox.critical(
                    self, "Error", str(e)
                )

    def search_student_records(self, keyword):

        records = logic.search_students(keyword)

        self.fill_table(
            self.student_table, records
        )

    # ---------------- ISSUE BOOKS ----------------

    def issue_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(18)

        layout.addWidget(
            self.create_heading("Issue Books")
        )

        instructions = QLabel(
            "Enter the Book ID and Student ID to issue a book."
        )

        layout.addWidget(instructions)

        self.book_id_input = QLineEdit()
        self.book_id_input.setPlaceholderText("Enter Book ID")

        self.student_id_input = QLineEdit()
        self.student_id_input.setPlaceholderText("Enter Student ID")

        layout.addWidget(self.book_id_input)
        layout.addWidget(self.student_id_input)

        issue_btn = QPushButton("Issue Book")
        issue_btn.setObjectName("action")
        issue_btn.clicked.connect(self.issue_book)

        layout.addWidget(issue_btn)
        layout.addStretch()

        return page

    def issue_book(self):

        book_id = self.book_id_input.text().strip()
        student_id = self.student_id_input.text().strip()

        if not book_id or not student_id:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter both Book ID and Student ID."
            )

            return

        try:

            book_id = int(book_id)
            student_id = int(student_id)

        except ValueError:

            QMessageBox.warning(
                self,
                "Invalid Input",
                "Book ID and Student ID must be numbers."
            )

            return

        if book_id <= 0 or student_id <= 0:

            QMessageBox.warning(
                self,
                "Invalid Input",
                "Book ID and Student ID must be positive numbers."
            )

            return

        try:

            books = logic.get_books()
            book_ids = [int(book[0]) for book in books]

            if book_id not in book_ids:

                QMessageBox.warning(
                    self,
                    "Invalid Book ID",
                    "The entered Book ID does not exist."
                )

                return

            students = logic.get_students()

            student_ids = [
                int(student[0]) for student in students
            ]

            if student_id not in student_ids:

                QMessageBox.warning(
                    self,
                    "Invalid Student ID",
                    "The entered Student ID does not exist."
                )

                return

            success = logic.borrow_book(
                book_id,
                student_id,
                QDate.currentDate().toString("yyyy-MM-dd")
            )

            if success:

                QMessageBox.information(
                    self, "Success",
                    "Book issued successfully!"
                )

                self.book_id_input.clear()
                self.student_id_input.clear()

                self.refresh_all()

            else:

                QMessageBox.warning(
                    self,
                    "Unavailable",
                    "No copies of this book are currently available."
                )

        except Exception as e:

            QMessageBox.critical(
                self, "Error", str(e)
            )

    # ---------------- BORROWING RECORDS ----------------

    def records_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        layout.addWidget(
            self.create_heading("Borrowing Records")
        )

        self.record_table = self.create_table([
            "Borrow ID",
            "Book Title",
            "Student",
            "Borrow Date",
            "Return Date",
            "Status"
        ])

        layout.addWidget(self.record_table)

        return_btn = QPushButton(
            "Return Selected Book"
        )

        return_btn.setObjectName("action")
        return_btn.clicked.connect(self.return_book)

        layout.addWidget(return_btn)

        return page

    def return_book(self):

        borrow_id = self.selected_id(
            self.record_table
        )

        if borrow_id is None:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Return",
            "Do you want to mark this book as returned?"
        )

        if confirm == QMessageBox.StandardButton.Yes:

            try:

                success = logic.return_book(
                    borrow_id,
                    QDate.currentDate().toString("yyyy-MM-dd")
                )

                if success:

                    QMessageBox.information(
                        self, "Success",
                        "Book returned successfully!"
                    )

                    self.refresh_all()

                else:

                    QMessageBox.warning(
                        self,
                        "Error",
                        "This book has already been returned."
                    )

            except Exception as e:

                QMessageBox.critical(
                    self, "Error", str(e)
                )

    # ---------------- REFRESH DATA ----------------

    def refresh_all(self):

        books = logic.get_books()
        students = logic.get_students()
        records = logic.get_borrow_records()

        borrowed = sum(
            1 for record in records
            if record[5] == "Borrowed"
        )

        self.book_card.setText(
            f"Total Book Titles: {len(books)}"
        )

        self.student_card.setText(
            f"Registered Students: {len(students)}"
        )

        self.borrowed_card.setText(
            f"Books Currently Borrowed: {borrowed}"
        )

        self.fill_table(self.book_table, books)
        self.fill_table(self.student_table, students)
        self.fill_table(self.record_table, records)


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":

    create_tables()

    app = QApplication(sys.argv)

    window = LibraryManagementSystem()
    window.show()

    sys.exit(app.exec())
