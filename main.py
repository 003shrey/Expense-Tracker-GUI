import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt


FILENAME = "expenses.csv"

# CSV file initialize
def init_file():
    try:
        with open(FILENAME, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])
    except FileExistsError:
        pass

# Add expense to CSV
def add_expense():
    try:
        amount = float(amount_var.get())
        description = desc_var.get()
        category = category_var.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, description])

        amount_var.set("")
        desc_var.set("")
        category_var.set("Food")
        load_expenses()
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid amount.")

# Load expenses into Treeview
def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                tree.insert("", tk.END, values=row)
    except FileNotFoundError:
        pass

# Delete selected expense
def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select an expense to delete.")
        return

    index = tree.index(selected[0])
    with open(FILENAME, 'r') as file:
        rows = list(csv.reader(file))
    header, data = rows[0], rows[1:]

    del data[index]
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    load_expenses()

# Summary of total and category-wise
def show_summary():
    total = 0
    summary = {}
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                amount = float(row[2])
                category = row[1]
                total += amount
                summary[category] = summary.get(category, 0) + amount
    except FileNotFoundError:
        return

    msg = f"Total: ₹{total:.2f}\n\nCategory-wise:\n"
    for cat, amt in summary.items():
        msg += f"- {cat}: ₹{amt:.2f}\n"
    messagebox.showinfo("Expense Summary", msg)

# Tkinter UI Setup
init_file()
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")

frame = tk.Frame(root)
frame.pack(pady=10)

amount_var = tk.StringVar()
desc_var = tk.StringVar()
category_var = tk.StringVar(value="Food")

# Input Fields
tk.Label(frame, text="Amount:").grid(row=0, column=0)
tk.Entry(frame, textvariable=amount_var).grid(row=0, column=1)

tk.Label(frame, text="Description:").grid(row=0, column=2)
tk.Entry(frame, textvariable=desc_var).grid(row=0, column=3)

tk.Label(frame, text="Category:").grid(row=1, column=0)
tk.OptionMenu(frame, category_var, "Food", "Travel", "Rent", "Shopping", "Other").grid(row=1, column=1)

tk.Button(frame, text="Add Expense", command=add_expense).grid(row=1, column=3)

# Treeview for displaying expenses
tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Description"), show='headings')
for col in ("Date", "Category", "Amount", "Description"):
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(pady=20, fill=tk.BOTH, expand=True)

#graph section
def show_graph():
    summary = {}

    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                category = row[1]
                amount = float(row[2])
                summary[category] = summary.get(category, 0) + amount
    except FileNotFoundError:
        messagebox.showerror("Error", "No data available.")
        return

    if not summary:
        messagebox.showinfo("No Data", "No expenses to display.")
        return

    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts, color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Amount Spent (₹)')
    plt.title('Expenses by Category')
    plt.tight_layout()
    plt.show()


# Action Buttons
btn_frame = tk.Frame(root)
btn_frame.pack()
tk.Button(btn_frame, text="Delete Selected", command=delete_expense).pack(side=tk.LEFT, padx=10)
tk.Button(btn_frame, text="Show Summary", command=show_summary).pack(side=tk.LEFT)

tk.Button(btn_frame, text="Show Graph", command=show_graph).pack(side=tk.LEFT, padx=10)



load_expenses()
root.mainloop()


