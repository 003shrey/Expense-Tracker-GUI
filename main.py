# Expense Tracker - Bhai, comments apni bhasa mein, thoda jugad bhi hai, dekh le!

import tkinter as tk
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import matplotlib.pyplot as plt

FILENAME = "expenses.csv"

# Pehle check karo file hai ya nahi, nahi hai toh bana lo
def init_file():
    try:
        with open(FILENAME, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Description"])  # Header likh diya
    except FileExistsError:
        pass  # File already hai toh kuch mat karo, aage badho ab

# Naya kharcha add karo - yahan thoda dhyan se, galat input aa sakta hai
def add_expense():
    try:
        amount = float(amount_var.get())  # yahan galti ho sakti hai, isliye try mein hai
        description = desc_var.get()
        category = category_var.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # date ka format theek hai na?
        with open(FILENAME, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, amount, description])
        # Input fields ko reset kar do, warna purana data dikh jayega
        amount_var.set("")
        desc_var.set("")
        category_var.set("Food")  # default food hi rehta hai, bhookh sabko lagti hai
        load_expenses()
    except ValueError:
        # Bhai, number hi daal, text nahi chalega yahan
        messagebox.showerror("Galat Input", "Sahi amount daalo! (sirf number)")

# Table mein saare kharche dikhao, csv file se
def load_expenses():
    # Pehle sab row hatao, warna repeat ho jayega
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Header skip kar diya
            for row in reader:
                tree.insert("", tk.END, values=row)
    except FileNotFoundError:
        # File hi nahi hai toh kuch nahi dikhega, koi baat nahi
        pass

# Jo kharcha select kiya hai, usko hatao - delete ka jugad
def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select karo", "Pehle koi kharcha select karo delete karne ke liye, bhai!")
        return
    index = tree.index(selected[0])
    # Sab data list mein le lo
    with open(FILENAME, 'r') as file:
        rows = []
        for r in csv.reader(file):
            rows.append(r)
    header = rows[0]
    data = rows[1:]
    # Us index waala data hatao, hope sahi index ho!
    if index < len(data):
        data.pop(index)
    # Wapas likh do file mein, pura overwrite ho raha hai
    with open(FILENAME, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for row in data:
            writer.writerow(row)
    load_expenses()

# Total aur category wise pura karcha dikha de yha - thoda math bhi hai
def show_summary():
    total = 0
    summary = {}
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                # Amount ko float mein badlo, try-catch for safety
                try:
                    amount = float(row[2])
                except:
                    amount = 0  # Bhool gaya toh zero le lenge
                category = row[1]
                total += amount
                if category in summary:
                    summary[category] += amount
                else:
                    summary[category] = amount
    except FileNotFoundError:
        # Bhai, file hi nahi mili, ab kya summary dikhayein
        return
    msg = f"Total: ₹{total:.2f}\n\nCategory-wise:\n"
    for cat in summary:
        amt = summary[cat]
        msg += f"- {cat}: ₹{amt:.2f}\n"
    # TODO: Yahan pe aur details add kar sakte hain, abhi itna hi
    messagebox.showinfo("Expense Summary", msg)

# Category wise graph dikhao - chal ab graph ki baari hain
def show_graph():
    summary = {}
    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                category = row[1]
                try:
                    amount = float(row[2])
                except:
                    amount = 0  # Bhool gaya toh zero le lenge
                if category in summary:
                    summary[category] += amount
                else:
                    summary[category] = amount
    except FileNotFoundError:
        messagebox.showerror("Error", "Koi data nahi mila, kyuki hain hi ni.")
        return
    if len(summary) == 0:
        messagebox.showinfo("No Data", "Kuch bhi nahi hai dikhane ko.")
        return
    categories = []
    amounts = []
    for cat in summary:
        categories.append(cat)
        amounts.append(summary[cat])
    # TODO: Pie chart bhi bana sakte hain future mein
    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts, color='skyblue')
    plt.xlabel('Category')  # X axis ka naam
    plt.ylabel('Amount Spent (₹)')  # Y axis ka naam
    plt.title('Expenses by Category')  # Title mast hai
    plt.tight_layout()
    plt.show()

# --- UI Setup --- yha bhai bs ui ui ki baatein hongi

init_file()
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("700x500")

# ---- Input fields ek hi line mein (grid se) ----
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

amount_label = tk.Label(input_frame, text="Amount:")
amount_label.grid(row=0, column=0, padx=5)
amount_var = tk.StringVar()
amount_entry = tk.Entry(input_frame, textvariable=amount_var, width=10)
amount_entry.grid(row=0, column=1, padx=5)

desc_label = tk.Label(input_frame, text="Description:")
desc_label.grid(row=0, column=2, padx=5)
desc_var = tk.StringVar()
desc_entry = tk.Entry(input_frame, textvariable=desc_var, width=15)
desc_entry.grid(row=0, column=3, padx=5)

category_label = tk.Label(input_frame, text="Category:")
category_label.grid(row=0, column=4, padx=5)
category_var = tk.StringVar(value="Food")
category_options = ["Food", "Travel", "Rent", "Shopping", "Other"]
category_menu = tk.OptionMenu(input_frame, category_var, *category_options)
category_menu.grid(row=0, column=5, padx=5)

add_btn = tk.Button(input_frame, text="Add Expense", command=add_expense)
add_btn.grid(row=0, column=6, padx=5)

# --- Table ---
tree = ttk.Treeview(root, columns=("Date", "Category", "Amount", "Description"), show='headings')
tree.heading("Date", text="Date")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Description", text="Description")
tree.column("Date", width=150)
tree.column("Category", width=100)
tree.column("Amount", width=100)
tree.column("Description", width=200)
tree.pack(pady=10, fill=tk.BOTH, expand=True)

# --- Buttons waale section bhi simple tarike se bana diye ---
delete_btn = tk.Button(root, text="Delete Selected", command=delete_expense)
delete_btn.pack(side=tk.LEFT, padx=10, pady=5)

summary_btn = tk.Button(root, text="Show Summary", command=show_summary)
summary_btn.pack(side=tk.LEFT, padx=10, pady=5)

graph_btn = tk.Button(root, text="Show Graph", command=show_graph)
graph_btn.pack(side=tk.LEFT, padx=10, pady=5)

# Shuru mein data load karo, warna khali dikhega
load_expenses()

root.mainloop()
