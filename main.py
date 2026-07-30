#============================================================
# LIBRARIES
#============================================================
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import yagmail
import csv
import os
from datetime import datetime
import sys

if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

price_file = os.path.join(base_path, 'price.csv')
sales_log_file = os.path.join(base_path, 'sales_log.csv')

#============================================================
# PLACEHOLDERS & CONFIGURATION
#============================================================
COMPANY_NAME = "YOUR COMPANY NAME"

#============================================================
# LOAD PRICE LIST (runs once, when the program starts)
#============================================================
prices = {}
try:
    with open(price_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header row
        for row in reader:
            barcode, name, price, stock = row
            prices[barcode] = {"name": name, "price": float(price), "stock": int(stock)}
except PermissionError:
    messagebox.showerror('File price.csv is open in background', 'Please close and try again')
except FileNotFoundError:
    # First-ever run, no price.csv yet — start with an empty list instead of crashing.
    pass


#============================================================
# CORE LOGIC FUNCTIONS
#============================================================

def generate_invoice(client_name, client_email, items, invoice_number, discount):
    """Create the PDF invoice and return its filename."""
    invoices_folder = os.path.join(base_path, 'Invoices')
    os.makedirs(invoices_folder, exist_ok=True)
    filename = os.path.join(invoices_folder, f"Invoice_{invoice_number}_{client_name}.pdf")
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, COMPANY_NAME)

    c.setFont('Helvetica', 12)
    c.drawString(50, height - 100, f"Invoice Number: {invoice_number}")
    c.drawString(50, height - 120, f"Client Name: {client_name}")
    c.drawString(50, height - 140, f"Client Email: {client_email}")
    c.drawRightString(550, height - 100, f"Date: {datetime.now().strftime('%d-%m-%Y')}")

    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, height - 200, "Item")
    c.drawString(300, height - 200, "Quantity")
    c.drawString(400, height - 200, "Price")
    c.drawString(480, height - 200, "Total")
    c.line(50, height - 210, 550, height - 210)

    c.setFont('Helvetica', 12)
    y = height - 230
    for item in items:
        name, qty, price = item
        total = qty * price
        c.drawString(50, y, str(name))
        c.drawString(300, y, str(qty))
        c.drawString(400, y, f"Rs. {price}")
        c.drawString(480, y, f"Rs.{total}")
        y -= 20

    subtotal = sum(qty * price for name, qty, price in items)
    grandtotal = subtotal * (1 - discount / 100)

    c.setFont('Helvetica', 12)
    c.drawString(400, y - 30, f"Subtotal: Rs.{subtotal:.2f}")
    c.drawString(400, y - 50, f"Discount: {discount}%")
    c.setFont('Helvetica-Bold', 12)
    c.drawString(400, y - 70, f"Grand Total: Rs.{grandtotal:.2f}")

    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "Thank you for shopping with us!")

    c.save()
    return filename


def print_invoice(filename):
    os.startfile(filename)


def send_mail(sender_email, sender_password, filename, client_email):
    yag = yagmail.SMTP(sender_email, sender_password)
    yag.send(
        to=client_email,
        subject='Invoice for your order',
        contents="Please find your invoice attached below. Thank you for shopping with us",
        attachments=filename
    )


def sales_log(client_name, invoice_number, items):
    try:
        with open(sales_log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            for name, qty, price in items:
                writer.writerow([datetime.now(), client_name, invoice_number, name, qty, price, qty * price])
    except PermissionError:
        messagebox.showerror('File sales_log.csv is open in background', 'Please close and try again')


def save_stock():
    try:
        with open(price_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Barcode', 'Name', 'Price', 'Stock'])
            for barcode, details in prices.items():
                writer.writerow([barcode, details['name'], details['price'], details['stock']])
    except PermissionError:
        messagebox.showerror('File price.csv is open in background', 'Please close and try again')


#============================================================
# APP STATE
#============================================================
current_items = []


#============================================================
# GUI — BUILDING THE WINDOW
#============================================================

# ---- Colors & fonts kept in one place so the look stays consistent ----
BG_COLOR = "#f5f5f0"
ACCENT_COLOR = "#2e7d32"
TEXT_COLOR = "#222222"
FONT_NORMAL = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 11, "bold")
FONT_HEADER = ("Segoe UI", 18, "bold")

root = tk.Tk()
root.title(f"{COMPANY_NAME} — Billing")
root.geometry("480x700")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# ---- Header ----
header = tk.Frame(root, bg=ACCENT_COLOR, height=70)
header.pack(fill="x")
tk.Label(header, text=COMPANY_NAME, font=FONT_HEADER, bg=ACCENT_COLOR, fg="white").pack(pady=18)

# ---- Customer details section ----
details_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=15)
details_frame.pack(fill="x")

tk.Label(details_frame, text="Client Name", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, sticky="w")
client_name_entry = tk.Entry(details_frame, font=FONT_NORMAL, width=22)
client_name_entry.grid(row=0, column=1, padx=10)

tk.Label(details_frame, text="Invoice No.", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=2, sticky="w")
invoice_number_entry = tk.Entry(details_frame, font=FONT_NORMAL, width=10)
invoice_number_entry.grid(row=0, column=3, padx=10)

# ---- Scan/add item section ----
scan_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=5)
scan_frame.pack(fill="x")

tk.Label(scan_frame, text="Scan / Enter Barcode", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=0, sticky="w")
barcode_entry = tk.Entry(scan_frame, font=FONT_NORMAL, width=18)
barcode_entry.grid(row=0, column=1, padx=10)

tk.Label(scan_frame, text="Qty", font=FONT_NORMAL, bg=BG_COLOR).grid(row=0, column=2, sticky="w")
qty_entry = tk.Entry(scan_frame, font=FONT_NORMAL, width=6)
qty_entry.grid(row=0, column=3, padx=10)


def add_item():
    barcode = barcode_entry.get().strip()

    if not barcode:
        return

    if barcode not in prices:
        messagebox.showerror("Not found", "This item is not available.")
        return

    item_details = prices[barcode]

    try:
        qty = int(qty_entry.get().strip())
        if qty <= 0:
            messagebox.showerror("Invalid quantity", "Quantity must be greater than 0.")
            return
    except ValueError:
        messagebox.showerror("Invalid quantity", "Enter a valid whole number (eg: 1, 2, 3).")
        return

    if qty > item_details["stock"]:
        messagebox.showerror("Not enough stock", f"Only {item_details['stock']} units in stock.")
        return

    item_details["stock"] -= qty
    current_items.append((item_details["name"], qty, item_details["price"]))

    line_total = qty * item_details["price"]
    cart_list.insert(tk.END, f"{item_details['name']}   x{qty}   —   Rs.{line_total:.2f}")
    update_subtotal()

    barcode_entry.delete(0, tk.END)
    qty_entry.delete(0, tk.END)
    barcode_entry.focus()


add_button = tk.Button(scan_frame, text="Add", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white",
                        width=8, command=add_item)
add_button.grid(row=0, column=4, padx=10)


def focus_qty(event):
    qty_entry.focus()


def add_item_on_enter(event):
    add_item()
    barcode_entry.focus()


barcode_entry.bind("<Return>", focus_qty)
qty_entry.bind("<Return>", add_item_on_enter)

# ---- Cart list ----
cart_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=10)
cart_frame.pack(fill="both", expand=True)

tk.Label(cart_frame, text="Current Order", font=FONT_BOLD, bg=BG_COLOR).pack(anchor="w")

cart_list = tk.Listbox(cart_frame, font=FONT_NORMAL, height=10, bg="white", relief="solid", bd=1)
cart_list.pack(fill="both", expand=True, pady=(5, 0))

# ---- Subtotal / discount / total section ----
totals_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=10)
totals_frame.pack(fill="x")

subtotal_label = tk.Label(totals_frame, text="Subtotal: Rs.0.00", font=FONT_NORMAL, bg=BG_COLOR)
subtotal_label.grid(row=0, column=0, sticky="w")

tk.Label(totals_frame, text="Discount %", font=FONT_NORMAL, bg=BG_COLOR).grid(row=1, column=0, sticky="w", pady=(8, 0))
discount_entry = tk.Entry(totals_frame, font=FONT_NORMAL, width=8)
discount_entry.insert(0, "0")
discount_entry.grid(row=1, column=1, sticky="w", padx=10, pady=(8, 0))

grandtotal_label = tk.Label(totals_frame, text="Grand Total: Rs.0.00", font=("Segoe UI", 13, "bold"),
                             bg=BG_COLOR, fg=ACCENT_COLOR)
grandtotal_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0))


def update_subtotal():
    subtotal = sum(qty * price for name, qty, price in current_items)
    subtotal_label.config(text=f"Subtotal: Rs.{subtotal:.2f}")
    update_grandtotal()


def update_grandtotal(*args):
    subtotal = sum(qty * price for name, qty, price in current_items)
    try:
        discount = float(discount_entry.get())
        if discount < 0 or discount > 100:
            discount = 0
    except ValueError:
        discount = 0
    grandtotal = subtotal * (1 - discount / 100)
    grandtotal_label.config(text=f"Grand Total: Rs.{grandtotal:.2f}")


discount_entry.bind("<KeyRelease>", update_grandtotal)

# ---- Delivery / management buttons ----
delivery_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=15)
delivery_frame.pack(fill="x")


def validate_before_finalizing():
    if not current_items:
        messagebox.showinfo("No items", "Add at least one item before finalizing.")
        return None

    client_name = client_name_entry.get().strip()
    invoice_number = invoice_number_entry.get().strip()

    if not client_name or not invoice_number:
        messagebox.showerror("Missing details", "Enter client name and invoice number.")
        return None

    try:
        discount = float(discount_entry.get())
        if discount < 0 or discount > 100:
            messagebox.showerror("Invalid discount", "Discount must be between 0 and 100.")
            return None
    except ValueError:
        messagebox.showerror("Invalid discount", "Enter a valid discount number (eg: 5, 10).")
        return None

    return client_name, invoice_number, discount


def finish_and_reset(client_name, invoice_number):
    sales_log(client_name, invoice_number, current_items)
    save_stock()
    current_items.clear()
    cart_list.delete(0, tk.END)
    update_subtotal()
    client_name_entry.delete(0, tk.END)
    invoice_number_entry.delete(0, tk.END)
    discount_entry.delete(0, tk.END)
    discount_entry.insert(0, "0")


def handle_print():
    result = validate_before_finalizing()
    if result is None:
        return
    client_name, invoice_number, discount = result

    filename = generate_invoice(client_name, "", current_items, invoice_number, discount)
    print_invoice(filename)
    messagebox.showinfo("Done", f"Invoice opened: {filename}\nUse Ctrl+P in the viewer to print.")
    finish_and_reset(client_name, invoice_number)


def handle_email():
    result = validate_before_finalizing()
    if result is None:
        return
    client_name, invoice_number, discount = result

    email_window = tk.Toplevel(root)
    email_window.title("Send via Email")
    email_window.geometry("320x220")
    email_window.configure(bg=BG_COLOR, padx=20, pady=20)

    tk.Label(email_window, text="Client Email", bg=BG_COLOR, font=FONT_NORMAL).pack(anchor="w")
    client_email_entry = tk.Entry(email_window, font=FONT_NORMAL, width=30)
    client_email_entry.insert(0, "client@example.com")  # Placeholder text
    client_email_entry.pack(pady=(0, 10))

    tk.Label(email_window, text="Sender Email", bg=BG_COLOR, font=FONT_NORMAL).pack(anchor="w")
    sender_email_entry = tk.Entry(email_window, font=FONT_NORMAL, width=30)
    sender_email_entry.insert(0, "your_email@gmail.com")  # Placeholder text
    sender_email_entry.pack(pady=(0, 10))

    tk.Label(email_window, text="Sender App Password", bg=BG_COLOR, font=FONT_NORMAL).pack(anchor="w")
    sender_password_entry = tk.Entry(email_window, font=FONT_NORMAL, width=30, show="*")
    sender_password_entry.pack(pady=(0, 15))

    def confirm_send():
        client_email = client_email_entry.get().strip()
        sender_email = sender_email_entry.get().strip()
        sender_password = sender_password_entry.get().strip()

        if not client_email or not sender_email or not sender_password:
            messagebox.showerror("Missing details", "Fill in all fields.")
            return

        filename = generate_invoice(client_name, client_email, current_items, invoice_number, discount)
        try:
            send_mail(sender_email, sender_password, filename, client_email)
        except Exception as e:
            messagebox.showerror("Email failed", f"Could not send email:\n{e}")
            return

        email_window.destroy()
        messagebox.showinfo("Done", f"Invoice emailed to {client_email}")
        finish_and_reset(client_name, invoice_number)

    tk.Button(email_window, text="Send", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white",
              command=confirm_send).pack(fill="x")


def open_inventory_manager():
    inv_window = tk.Toplevel(root)
    inv_window.title("Manage Inventory")
    inv_window.geometry("420x500")
    inv_window.configure(bg=BG_COLOR, padx=20, pady=20)

    tk.Label(inv_window, text="Manage Inventory", font=("Segoe UI", 14, "bold"), bg=BG_COLOR).pack(anchor="w", pady=(0, 10))
    tk.Label(inv_window, text="Enter an existing barcode to edit it, or a new one to add a product.",
             font=("Segoe UI", 8), bg=BG_COLOR, fg="gray", wraplength=380, justify="left").pack(anchor="w", pady=(0, 10))

    tk.Label(inv_window, text="Barcode", bg=BG_COLOR, font=FONT_NORMAL).pack(anchor="w")
    inv_barcode_entry = tk.Entry(inv_window, font=FONT_NORMAL, width=25)
    inv_barcode_entry.pack(pady=(0, 10), fill="x")

    tk.Label(inv_window, text="Item Name", bg=BG_COLOR, font=FONT_NORMAL).pack(anchor="w")
    inv_name_entry = tk.Entry(inv_window, font=FONT_NORMAL, width=25)
    inv_name_entry.pack(pady=(0, 10), fill="x")

    tk.Label(inv_window, text="Price (Rs.)", bg=BG_COLOR, font=FONT_NORMAL).pack(anchor="w")
    inv_price_entry = tk.Entry(inv_window, font=FONT_NORMAL, width=25)
    inv_price_entry.pack(pady=(0, 10), fill="x")

    tk.Label(inv_window, text="Stock", bg=BG_COLOR, font=FONT_NORMAL).pack(anchor="w")
    inv_stock_entry = tk.Entry(inv_window, font=FONT_NORMAL, width=25)
    inv_stock_entry.pack(pady=(0, 15), fill="x")

    status_label = tk.Label(inv_window, text="", bg=BG_COLOR, font=FONT_NORMAL, fg="green")
    status_label.pack(anchor="w", pady=(0, 10))

    def load_existing_item(event=None):
        barcode = inv_barcode_entry.get().strip()
        if not barcode:
            return
        if barcode in prices:
            item = prices[barcode]
            inv_name_entry.delete(0, tk.END)
            inv_name_entry.insert(0, item["name"])
            inv_price_entry.delete(0, tk.END)
            inv_price_entry.insert(0, str(item["price"]))
            inv_stock_entry.delete(0, tk.END)
            inv_stock_entry.insert(0, str(item["stock"]))
            status_label.config(text="Existing item loaded — editing.", fg="blue")
        else:
            status_label.config(text="New barcode — fill in details to add.", fg="green")

    inv_barcode_entry.bind("<FocusOut>", load_existing_item)

    def save_item():
        barcode = inv_barcode_entry.get().strip()
        name = inv_name_entry.get().strip()

        if not barcode or not name:
            messagebox.showerror("Missing details", "Barcode and item name are required.")
            return

        try:
            price = float(inv_price_entry.get().strip())
            if price < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid price", "Enter a valid price (eg: 60, 99.50).")
            return

        try:
            stock = int(inv_stock_entry.get().strip())
            if stock < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid stock", "Enter a valid whole number for stock.")
            return

        is_new = barcode not in prices
        prices[barcode] = {"name": name, "price": price, "stock": stock}
        save_stock()

        status_label.config(text=f"{'Added' if is_new else 'Updated'}: {name}", fg="green")
        inv_barcode_entry.delete(0, tk.END)
        inv_name_entry.delete(0, tk.END)
        inv_price_entry.delete(0, tk.END)
        inv_stock_entry.delete(0, tk.END)
        inv_barcode_entry.focus()

    tk.Button(inv_window, text="Save Item", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white",
              command=save_item).pack(fill="x", pady=(5, 0))

    def focus_name(event):
        inv_name_entry.focus()

    def focus_price(event):
        inv_price_entry.focus()

    def focus_stock(event):
        inv_stock_entry.focus()

    def save_on_enter(event):
        save_item()

    inv_barcode_entry.bind("<Return>", focus_name)
    inv_name_entry.bind("<Return>", focus_price)
    inv_price_entry.bind("<Return>", focus_stock)
    inv_stock_entry.bind("<Return>", save_on_enter)

    inv_barcode_entry.focus()


print_btn = tk.Button(delivery_frame, text="Print Invoice", font=FONT_BOLD, bg="#455a64", fg="white",
                       command=handle_print, height=2)
print_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

email_btn = tk.Button(delivery_frame, text="Email Invoice", font=FONT_BOLD, bg=ACCENT_COLOR, fg="white",
                       command=handle_email, height=2)
email_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))

manage_btn = tk.Button(delivery_frame, text="Manage Inventory", font=FONT_BOLD, bg="#6d4c41", fg="white",
                        command=open_inventory_manager, height=2)
manage_btn.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 0))

delivery_frame.columnconfigure(0, weight=1)
delivery_frame.columnconfigure(1, weight=1)

barcode_entry.focus()
root.mainloop()
