import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import ImageGrab
from models import Trip


class BillSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Splitter")
        self.root.geometry("800x600")

        # Center the window
        self.center_window()

        # Trip object
        self.trip = Trip("My Trip")

        # Frames
        self.create_participant_frame()
        self.create_expense_frame()
        self.create_result_frame()

    def center_window(self):
        # Get the window size and screen size
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position for centering the window
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window size and position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_participant_frame(self):
        frame = ttk.LabelFrame(self.root, text="Participants", style="TFrame")
        frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        self.participant_entry = ttk.Entry(frame, width=30)
        self.participant_entry.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(frame, text="Add Participant", command=self.add_participant).grid(
            row=0, column=1, padx=5, pady=5
        )

        self.participant_list = tk.Listbox(frame, height=5, width=40, bg="#f0f0f0", fg="black")
        self.participant_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(frame, text="Edit Participant", command=self.edit_participant).grid(
            row=2, column=0, padx=5, pady=5
        )
        ttk.Button(frame, text="Remove Participant", command=self.remove_participant).grid(
            row=2, column=1, padx=5, pady=5
        )

    def create_expense_frame(self):
        frame = ttk.LabelFrame(self.root, text="Add Expense", style="TFrame")
        frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ttk.Label(frame, text="Amount (INR):", foreground="blue").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Payer:", foreground="blue").grid(row=1, column=0, padx=5, pady=5)
        self.payer_combo = ttk.Combobox(frame, values=list(self.trip.participants.keys()))
        self.payer_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Beneficiaries (comma-separated):", foreground="blue").grid(row=2, column=0, padx=5, pady=5)
        self.beneficiaries_entry = ttk.Entry(frame, width=30)
        self.beneficiaries_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Description:", foreground="blue").grid(row=3, column=0, padx=5, pady=5)
        self.description_entry = ttk.Entry(frame, width=30)
        self.description_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Expense", command=self.add_expense).grid(
            row=4, column=0, columnspan=2, padx=5, pady=5
        )

    def create_result_frame(self):
        frame = ttk.LabelFrame(self.root, text="Results and Actions", style="TFrame")
        frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        ttk.Button(frame, text="Show Expenses", command=self.show_expenses).grid(
            row=0, column=0, padx=5, pady=5
        )
        ttk.Button(frame, text="Show Balances", command=self.show_balances).grid(
            row=0, column=1, padx=5, pady=5
        )
        ttk.Button(frame, text="Show Settlements", command=self.show_settlements).grid(
            row=0, column=2, padx=5, pady=5
        )

        self.result_box = tk.Listbox(frame, height=10, width=50, bg="#e6f7ff", fg="black")
        self.result_box.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        ttk.Button(frame, text="Save Data", command=self.save_data).grid(
            row=2, column=0, padx=5, pady=5
        )
        ttk.Button(frame, text="Generate Excel", command=self.generate_excel).grid(
            row=2, column=1, padx=5, pady=5
        )
        ttk.Button(frame, text="Generate PDF", command=self.generate_pdf).grid(
            row=2, column=2, padx=5, pady=5
        )
        ttk.Button(frame, text="Take Screenshot", command=self.take_screenshot).grid(
            row=3, column=0, columnspan=3, padx=5, pady=5
        )

    # Participant management
    def add_participant(self):
        name = self.participant_entry.get().strip()
        if name:
            self.trip.add_participant(name)
            self.refresh_participants()
            self.participant_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Participant name cannot be empty!")

    def edit_participant(self):
        selected = self.participant_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a participant to edit!")
            return
        old_name = self.participant_list.get(selected)
        new_name = simpledialog.askstring("Edit Participant", f"Enter new name for '{old_name}':")
        if new_name:
            self.trip.edit_participant(old_name, new_name)
            self.refresh_participants()

    def remove_participant(self):
        selected = self.participant_list.curselection()
        if not selected:
            messagebox.showwarning("Warning", "Select a participant to remove!")
            return
        name = self.participant_list.get(selected)
        confirm = messagebox.askyesno("Confirm", f"Remove '{name}'?")
        if confirm:
            self.trip.remove_participant(name)
            self.refresh_participants()

    def refresh_participants(self):
        self.participant_list.delete(0, tk.END)
        for name in self.trip.participants.keys():
            self.participant_list.insert(tk.END, name)
        self.payer_combo["values"] = list(self.trip.participants.keys())

    # Expense management
    def add_expense(self):
        try:
            amount = float(self.amount_entry.get())
            payer = self.payer_combo.get()
            beneficiaries = [x.strip() for x in self.beneficiaries_entry.get().split(",")]
            description = self.description_entry.get().strip()
            self.trip.add_expense(amount, payer, beneficiaries, description)
            self.show_expenses()
            self.amount_entry.delete(0, tk.END)
            self.beneficiaries_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def show_expenses(self):
        self.result_box.delete(0, tk.END)
        for i, expense in enumerate(self.trip.expenses):
            self.result_box.insert(tk.END, f"{i + 1}. {expense}")

    def show_balances(self):
        balances = self.trip.calculate_balances()
        self.result_box.delete(0, tk.END)
        for name, balance in balances.items():
            self.result_box.insert(tk.END, f"{name}: ₹{balance:.2f}")

    def show_settlements(self):
        settlements = self.trip.optimize_settlements()
        self.result_box.delete(0, tk.END)
        for debtor, creditor, amount in settlements:
            self.result_box.insert(tk.END, f"{debtor} pays {creditor} ₹{amount:.2f}")

    # Save data to JSON
    def save_data(self):
        data = {
            "participants": {
                name: {
                    "total_paid": p.total_paid,
                    "total_share": p.total_share
                }
                for name, p in self.trip.participants.items()
            },
            "expenses": [
                {
                    "amount": e.amount,
                    "payer": e.payer,
                    "beneficiaries": e.beneficiaries,
                    "description": e.description,
                    "timestamp": e.timestamp,
                }
                for e in self.trip.expenses
            ],
        }
        with open("bill_splitter_data.json", "w") as f:
            json.dump(data, f, indent=4)
        messagebox.showinfo("Success", "Data saved to bill_splitter_data.json!")

    # Generate Excel
    def generate_excel(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Expenses"

        # Add header
        ws.append(["Timestamp", "Description", "Amount (INR)", "Payer", "Beneficiaries"])
        for expense in self.trip.expenses:
            ws.append([expense.timestamp, expense.description, f"₹{expense.amount:.2f}", expense.payer, ", ".join(expense.beneficiaries)])

        wb.save("bill_splitter.xlsx")
        messagebox.showinfo("Success", "Excel file generated: bill_splitter.xlsx")

    # Generate PDF
    def generate_pdf(self):
        c = canvas.Canvas("bill_splitter.pdf", pagesize=letter)
        width, height = letter
        y_position = height - 40  # Start from top of the page

        c.setFont("Helvetica", 12)
        c.drawString(30, y_position, "Expenses Report")
        y_position -= 20

        for expense in self.trip.expenses:
            c.drawString(30, y_position, f"{expense.timestamp} | {expense.description} | Amount: ₹{expense.amount:.2f} | Payer: {expense.payer} | Beneficiaries: {', '.join(expense.beneficiaries)}")
            y_position -= 20

        c.save()
        messagebox.showinfo("Success", "PDF file generated: bill_splitter.pdf")

    # Screenshot functionality
    def take_screenshot(self):
        # Take a screenshot of the UI window
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty()
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Capture the screen
        screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        screenshot.save("bill_splitter_screenshot.png")
        messagebox.showinfo("Success", "Screenshot saved as bill_splitter_screenshot.png")


if __name__ == "__main__":
    root = tk.Tk()
    app = BillSplitterApp(root)
    root.mainloop()
