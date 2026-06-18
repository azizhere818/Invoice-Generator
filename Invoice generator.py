#libraries
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import yagmail
import csv

#inputs
client_name=input('Enter cleint name: ')
client_email=input('Enter client email: ')
invoice_number=input('Enter invoice number: ')
sender_email=input('Enter sender email: ')
sender_password=input("Enter sender's password: ")
items=[]


#functions
def generate_invoice(client_name,client_email,items,invoice_number):
    filename=f"Invoice_{invoice_number}_{client_name}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height= A4


    #Title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "INVOICE")

    #Details
    c.setFont('Helvetica',12)
    c.drawString(50, height-100, f"Invoice Number: {invoice_number}")
    c.drawString(50, height-120, f"Client Name: {client_name}")
    c.drawString(50, height-140, f"Client Email: {client_email}")


    #Table Header
    c.setFont('Helvetica-Bold',12)
    c.drawString(50, height-200, "Item")
    c.drawString(300, height-200, "Quantity")
    c.drawString(400, height-200, "Price")
    c.drawString(480, height-200, "Total")

    #Lines
    c.line(50,height-210,550,height-210)


    c.setFont('Helvetica',12)
    y=height-230

    for item in items:
        name,qty,price=item
        total=qty*price
        c.drawString(50,y,str(name))
        c.drawString(300,y,str(qty))
        c.drawString(400,y,f"Rs. {price}")
        c.drawString(480,y,f"Rs.{total}")
        y-=20

    grandtotal=sum(qty*price for name,qty,price in items)
    c.setFont('Helvetica-Bold',12)
    c.drawString(400,y-30,f"Grand Total: {grandtotal}")

    #footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "Thank you for shopping with us!")

    c.save()
    return filename


#Name and price  dictionary
prices={}
with open('D:/price.csv','r') as file:
    reader=csv.reader(file)
    next(reader)
    for row in reader:
        prices[row[0]]=float(row[1])

print(prices)
print('Enter items (Type done when finished entering items): ')
while True:
    name=input('Enter item name: ')
    name=name.title()
    if name.lower()=='done':
        break
    if name not in prices:
        print('This item is not available')
        continue
    qty=int(input('Enter item qty: '))
    price=prices[name]
    items.append((name,qty,price))

#Send pdf to client
def send_mail(sender_email,sender_password,filename,client_email):
    yag=yagmail.SMTP(sender_email,sender_password)

    yag.send(
        to=client_email,
        subject='Invoice for your order',
        contents="Please find your invoice attached below. Thank you for shopping with us",
        attachments=filename
    ) 
    print('Email Sent')

#Run code
filename = generate_invoice(client_name,client_email,items,invoice_number)
send_mail(sender_email,sender_password,filename,client_email)


