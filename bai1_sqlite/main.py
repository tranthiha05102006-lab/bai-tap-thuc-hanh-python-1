import sqlite3
import tkinter as tk
from tkinter import messagebox

# ================= DATABASE =================
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# Tạo bảng
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    major TEXT,
    gpa REAL
)
""")
conn.commit()


# ================= FUNCTIONS =================
def add_student():
    name = entry_name.get()
    major = entry_major.get()
    gpa = entry_gpa.get()

    if name == "" or major == "" or gpa == "":
        messagebox.showwarning("Lỗi", "Nhập đầy đủ thông tin")
        return

    cursor.execute("INSERT INTO students (name, major, gpa) VALUES (?, ?, ?)",
                   (name, major, float(gpa)))
    conn.commit()
    messagebox.showinfo("OK", "Đã thêm sinh viên")
    show_all()


def show_all():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students")
    for row in cursor.fetchall():
        listbox.insert(tk.END, row)


def show_gpa_3():
    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM students WHERE gpa > 3.0")
    for row in cursor.fetchall():
        listbox.insert(tk.END, row)


def update_gpa():
    selected = listbox.get(tk.ACTIVE)
    if not selected:
        return

    new_gpa = entry_gpa.get()
    cursor.execute("UPDATE students SET gpa=? WHERE id=?",
                   (float(new_gpa), selected[0]))
    conn.commit()
    messagebox.showinfo("OK", "Đã cập nhật GPA")
    show_all()


def delete_low_gpa():
    cursor.execute("DELETE FROM students WHERE gpa < 2.0")
    conn.commit()
    messagebox.showinfo("OK", "Đã xóa sinh viên GPA < 2.0")
    show_all()


# ================= GUI =================
root = tk.Tk()
root.title("Quản lý sinh viên")

tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Major").grid(row=1, column=0)
tk.Label(root, text="GPA").grid(row=2, column=0)

entry_name = tk.Entry(root)
entry_major = tk.Entry(root)
entry_gpa = tk.Entry(root)

entry_name.grid(row=0, column=1)
entry_major.grid(row=1, column=1)
entry_gpa.grid(row=2, column=1)

tk.Button(root, text="Thêm SV", command=add_student).grid(row=3, column=0)
tk.Button(root, text="Hiển thị tất cả", command=show_all).grid(row=3, column=1)
tk.Button(root, text="GPA > 3.0", command=show_gpa_3).grid(row=4, column=0)
tk.Button(root, text="Cập nhật GPA", command=update_gpa).grid(row=4, column=1)
tk.Button(root, text="Xóa GPA < 2.0", command=delete_low_gpa).grid(row=5, column=0)

listbox = tk.Listbox(root, width=50)
listbox.grid(row=6, column=0, columnspan=2)

root.mainloop()

conn.close()