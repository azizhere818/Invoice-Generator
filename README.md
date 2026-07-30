# Billing and Inventory Management System

A desktop billing and inventory management application built using **Python** and **Tkinter**. The system allows users to manage inventory, generate professional PDF invoices, email invoices to customers, and maintain sales records through an easy-to-use graphical interface.

---

## Features

### Billing

- Generate professional PDF invoices
- Automatic subtotal and grand total calculation
- Discount support
- Print invoices
- Email invoices directly to customers
- Automatic invoice numbering

### Inventory Management

- Barcode-based product lookup
- Add new products
- Edit existing products
- Update product prices
- Update stock quantities
- Automatic stock deduction after each sale

### Sales Management

- Record every completed sale
- Maintain sales history in CSV format
- Automatic sales logging

### User Interface

- Desktop GUI built using Tkinter
- Live cart updates
- Real-time subtotal calculation
- Inventory management window
- Input validation and error handling

---

## Technologies Used

- Python
- Tkinter
- ReportLab
- Yagmail
- CSV
- OS
- Datetime

---

## How It Works

1. Load inventory from `price.csv`/create a new product from inventory management.
2. Enter customer information.
3. Scan or enter a product barcode.
4. Specify the quantity.
5. Items are added to the shopping cart.
6. Stock is automatically updated.
7. Apply an optional discount.
8. Generate a PDF invoice.
9. Print or email the invoice.
10. Record the sale in `sales_log.csv`.

---

## Setup

1. Clone the repository.

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Configure your Gmail App Password if you want to use the email feature.

4. Make sure `price.csv` exists in the project directory.

5. Run the application:

```bash
python main.py
```

---

## My Role

- Designed the billing workflow and inventory management logic.
- Implemented barcode-based product lookup.
- Developed PDF invoice generation.
- Integrated email automation.
- Implemented inventory updates and sales logging.
- Designed the application workflow and user experience.
- AI-assisted tools were used to accelerate development of parts of the graphical interface and improve productivity.

---

## Future Improvements

- MySQL database integration
- User authentication
- Customer management
- Product categories
- Sales dashboard
- Barcode scanner support
- Receipt printer integration
- GST/VAT calculations
- Excel report generation

---

## License

This project was created for learning and portfolio purposes.
