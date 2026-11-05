import tkinter as tk
from tkinter import messagebox


def show_message():
    messagebox.showinfo(
        "Message",
        "Hello! Welcome to Tkinter."
    )

root = tk.Tk()
root.title("Tkinter Hello World")
root.geometry("400x250")

label = tk.Label(
    root,
    text="Hello World!",
    font=("Arial", 22, "bold")
)
label.pack(pady=30)

button = tk.Button(
    root,
    text="Click Me",
    font=("Arial", 12),
    command=show_message
)
button.pack(pady=10)

root.mainloop()

