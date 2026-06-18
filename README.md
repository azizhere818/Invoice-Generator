# Invoice Generator

A Python automation script that generates professional PDF invoices from a saved price list, then emails them automatically to the client.

## What it does
- Reads item prices from a price list CSV (set up once per client)
- Takes the order details (item names and quantities) as user input
- Automatically looks up the correct price for each ordered item from the price list
- Generates a clean, professional PDF invoice with itemized costs and grand total
- Emails the invoice directly to the client with the PDF attached

## How it works
1. Maintain a `price_list.csv` with your products/services and their prices
2. Run the script and enter the item name and quantity for each item in the order when prompted
3. The script automatically looks up the price for each item from the price list
4. It calculates the total, generates the invoice as a PDF, and emails it to the client

## Libraries used
- reportlab — PDF generation
- yagmail — sending emails
- csv — reading the price list

## Example price list

**price_list.csv**
\`\`\`
name,price
Website Design,5000
Logo Design,1500
SEO Setup,2000
\`\`\`

## How to use
1. Install required libraries: `pip install reportlab yagmail`
2. Set up your `price_list.csv` with item names and prices
3. Run the script
4. Enter client details, then enter item names and quantities for the order (type "done" when finished)
5. Enter your email and app password when prompted
6. Invoice is generated and emailed automatically

## Why this is useful
Freelancers and small businesses often spend time manually creating invoices and re-typing prices for every order. This tool automates the PDF creation and email delivery, and removes the risk of typing the wrong price by looking it up automatically from a saved price list.
