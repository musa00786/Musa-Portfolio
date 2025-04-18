import csv
import tkinter as tk
from tkinter import messagebox, simpledialog

class Customer:
    def __init__(self, name, account_number, account_type, balance=0):
        self.name = name
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposited {amount}. New balance: {self.balance}"
        return "Invalid amount!"

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return f"Withdrew {amount}. New balance: {self.balance}"
        return "Insufficient funds or invalid amount!"

    def to_dict(self):
        return {"Name": self.name, "Account Number": self.account_number, "Account Type": self.account_type, "Balance": self.balance}

class Admin:
    def __init__(self, filename="customers.csv"):
        self.filename = filename
        self.customers = {}
        self.load_customers()

    def load_customers(self):
        try:
            with open(self.filename, mode="r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.customers[row["Account Number"]] = Customer(row["Name"], row["Account Number"], row["Account Type"], float(row["Balance"]))
        except FileNotFoundError:
            pass

    def save_customers(self):
        with open(self.filename, mode="w", newline="") as file:
            fieldnames = ["Name", "Account Number", "Account Type", "Balance"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for customer in self.customers.values():
                writer.writerow(customer.to_dict())

    def add_customer(self, name, account_number, account_type, balance=0):
        self.customers[account_number] = Customer(name, account_number, account_type, balance)
        self.save_customers()

    def search_customer(self, account_number):
        return self.customers.get(account_number, None)

    def remove_customer(self, account_number):
        if account_number in self.customers:
            del self.customers[account_number]
            self.save_customers()
            return "Customer removed successfully!"
        return "Customer not found!"

    def transfer_funds(self, from_acc, to_acc, amount):
        sender = self.customers.get(from_acc)
        receiver = self.customers.get(to_acc)
        
        if not sender:
            return "Sender account not found!"
        if not receiver:
            return "Receiver account not found!"
        if sender.balance < amount:
            return "Insufficient funds!"
        
        sender.withdraw(amount)
        receiver.deposit(amount)
        self.save_customers()
        return f"Transferred {amount} from {from_acc} to {to_acc}."

    def management_report(self):
        total_customers = len(self.customers)
        total_balance = sum(cust.balance for cust in self.customers.values())
        return f"Total customers: {total_customers}\nTotal funds in system: {total_balance}"

def gui_app():
    admin = Admin()
    root = tk.Tk()
    root.title("Banking System")
    root.geometry("400x500")

    def add_customer():
        name = simpledialog.askstring("Input", "Enter customer name:")
        acc_no = simpledialog.askstring("Input", "Enter account number:")
        acc_type = simpledialog.askstring("Input", "Account type (savings/business):").lower()
        balance = simpledialog.askfloat("Input", "Enter initial balance:")
        
        if acc_no and name and acc_type in ["savings", "business"]:
            admin.add_customer(name, acc_no, acc_type, balance)
            messagebox.showinfo("Success", "Customer added!")
        else:
            messagebox.showerror("Error", "Invalid input!")

    def search_customer():
        acc_no = simpledialog.askstring("Input", "Enter account number:")
        customer = admin.search_customer(acc_no)
        if customer:
            messagebox.showinfo("Customer Details", f"{customer}")
        else:
            messagebox.showerror("Error", "Customer not found!")

    def deposit_money():
        acc_no = simpledialog.askstring("Input", "Enter account number:")
        amount = simpledialog.askfloat("Input", "Enter deposit amount:")
        customer = admin.search_customer(acc_no)
        if customer:
            messagebox.showinfo("Success", customer.deposit(amount))
            admin.save_customers()
        else:
            messagebox.showerror("Error", "Customer not found!")

    def withdraw_money():
        acc_no = simpledialog.askstring("Input", "Enter account number:")
        amount = simpledialog.askfloat("Input", "Enter withdrawal amount:")
        customer = admin.search_customer(acc_no)
        if customer:
            messagebox.showinfo("Success", customer.withdraw(amount))
            admin.save_customers()
        else:
            messagebox.showerror("Error", "Customer not found!")

    def show_management_report():
        report = admin.management_report()
        messagebox.showinfo("Management Report", report)

    tk.Button(root, text="Add Customer", command=add_customer).pack(pady=5)
    tk.Button(root, text="Search Customer", command=search_customer).pack(pady=5)
    tk.Button(root, text="Deposit Money", command=deposit_money).pack(pady=5)
    tk.Button(root, text="Withdraw Money", command=withdraw_money).pack(pady=5)
    tk.Button(root, text="Management Report", command=show_management_report).pack(pady=5)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

    root.mainloop()

gui_app()
