# ==========================================
# GUI Frontend for ProofLite Web
# Owner: Mayur Dinsukh Girnara
# ==========================================

import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, font
from doc_auth_checker import analyze_document

def browse_file():
    filename = filedialog.askopenfilename(
        filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
    )
    file_entry.delete(0, tk.END)
    file_entry.insert(0, filename)

def check_document():
    input_file_path = file_entry.get()
    student_name = student_entry.get()
    course = course_entry.get()
    published_date = published_entry.get()
    due_date = due_entry.get()

    try:
        published_date = datetime.strptime(published_date, "%Y-%m-%d")
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showinfo("Error", "Invalid date format. Use YYYY-MM-DD.")
        return

    if not all([input_file_path, student_name, course, published_date, due_date]):
        messagebox.showinfo("Error", "All fields are required.")
        return

    suspect_events = analyze_document(input_file_path, student_name, published_date, due_date)

    if suspect_events:
        result_display.config(state=tk.NORMAL)
        result_display.delete(0, tk.END)
        result_display.insert(0, "Suspect issues found")
        result_display.config(state=tk.DISABLED)

        indicator_display.config(text="!", bg="red")
        messagebox.showinfo("Analysis Result", "\n".join(suspect_events))
    else:
        result_display.config(state=tk.NORMAL)
        result_display.delete(0, tk.END)
        result_display.insert(0, "No issues found")
        result_display.config(state=tk.DISABLED)

        indicator_display.config(text="✓", bg="green")

root = tk.Tk()
root.title("ProofLite – Document Authenticity Checker")
root.geometry("600x400")

app_font = font.Font(family="Helvetica", size=12)
root.grid_columnconfigure(1, weight=1)

labels = ["File", "Student", "Course", "Published", "Due", "Result", "Indicator"]
entries = []

for idx, text in enumerate(labels):
    tk.Label(root, text=text, font=app_font).grid(row=idx, column=0, sticky="e", padx=10, pady=10)
    if text != "Indicator":
        entry = tk.Entry(root, font=app_font)
        entry.grid(row=idx, column=1, sticky="ew", padx=10, pady=10)
        entries.append(entry)

file_entry, student_entry, course_entry, published_entry, due_entry, result_display = entries

browse_button = tk.Button(root, text="Browse", command=browse_file, font=app_font)
browse_button.grid(row=0, column=2, padx=10, pady=10)

indicator_display = tk.Label(root, text="?", bg="yellow", font=app_font, width=4)
indicator_display.grid(row=6, column=1, sticky="ew", padx=10, pady=10)

check_button = tk.Button(root, text="Check", command=check_document, font=app_font)
check_button.grid(row=7, column=1, padx=10, pady=20, sticky="ew")

root.mainloop()
