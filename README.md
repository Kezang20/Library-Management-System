# Library Management System

## 1. Project Description

The Library Management System is a desktop-based application developed using Python, PyQt6 and SQLite. It is designed to help manage library activities, including book records, student information and borrowing transactions through a graphical user interface.

## 2. Technologies Used

- **Python:** Main programming language.
- **PyQt6:** Used to develop the graphical user interface.
- **SQLite:** Used for storing and managing application data.
- **Qt Style Sheets (QSS):** Used to customise the application's appearance.

## 3. Main Features

The application provides the following features:

### Book Management
- Add new books.
- View available book records.
- Search books.
- Update book information.
- Delete book records.

### Student Management
- Register new students.
- View student records.
- Search students.
- Update student information.
- Delete student records.

### Borrowing Management
- Issue books to registered students.
- Return borrowed books.
- View borrowing records.

### Dashboard
- Display book, student and borrowing statistics.

### Database Management
- Store application records using SQLite.
- Retrieve saved information.
- Maintain records after closing and reopening the application.

## 4. Project Structure

```text
LibraryManagementSystem/
│
├── assets/
│   └── style.qss
│
├── data/
│   └── library.db
│
├── partA/
│   ├── kivy_hello.py
│   ├── pyqt_hello.py
│   ├── tkinter_hello.py
│   └── wxpython_test.py
│
├── main.py
├── database.py
├── library_logic.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 5. Requirements

Before running the application, ensure that the following are installed:

- Python 3.13
- pip (Python package installer)

## 6. Installation and Setup

Follow these steps to set up the application on your computer.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Kezang20/Library-Management-System.git
```

### Step 2: Open the Project Folder

```bash
cd Library-Management-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### Step 5: Install Required Dependencies

```bash
pip install -r requirements.txt
```

## 7. Running the Application

After completing the installation, run the following command:

```bash
python main.py
```

The Library Management System will open, allowing users to manage books, students and borrowing records.

## 8. Database

The application uses SQLite as its database management system. The database file is located inside the `data/` directory.

The database stores book information, student information and borrowing records.

## 9. Part A: Framework Hello World Programs

The `partA/` folder contains the Hello World programs developed to explore different Python GUI frameworks:

- Kivy
- PyQt6
- Tkinter
- wxPython

These programs demonstrate the basic GUI implementation of each framework.

## 10. Author

**Developed as part of the PRG304 coursework.**

**Repository:** https://github.com/Kezang20/Library-Management-System