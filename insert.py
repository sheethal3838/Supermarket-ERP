import mysql.connector as mysql
from connection import cursor,con
import datetime

def add_attendance(con,cursor):
    try:
        staff_id = input("Enter staffID: ")
        clockin = input("Enter clock in time: ")
        clockout = input("Enter clock out time: ")
        cursor.execute(
         "INSERT INTO StaffAttendance (staff_id, date, clockIN, clockOUT) VALUES (%s, CURDATE(), %s, %s)",
         (staff_id, clockin, clockout)
        )
        con.commit()
        print("Attendance added successfully.")
    except Exception as e:
        print("Error adding attendance:", e)

def add_staff(con,cursor):
    try:
        staffname = input("Enter staff name: ")
        designation = input("Enter designation: ")
        contact = input("Enter contact details: ")
        email = input("Enter EmailID: ")
        address = input("Enter address: ")
        dob = input("Enter DOB: ")
        hire_date = input("Enter hire date: ")
        salary = input("Enter salary: ")
        cursor.execute(
            "insert into StaffHistory (name,designation,contact,email,address,dob,hire_date,salary)"
            "values (%s, %s, %s,%s, %s, %s, %s, %s)",(staffname,designation,contact,email,address,dob,hire_date,salary)
        )
        con.commit()
        print("Staff added successfully.")
    except Exception as e:
        print("Error adding staff",e)

def add_products(con,cursor):
    try:
        productname = input("Enter Product name: ")
        quantity_available= input("Enter Quantity available: ")
        supplierID = int(input("Enter supplierID: "))
        cursor.execute(
            "insert into Product(name,quantity_available,supplierID)"
            "values(%s, %s, %s)",(productname,quantity_available,supplierID)
        )
        con.commit()
        print("Success")
    except Exception as e:
        print("Error: ",e)

def add_supplier(con,cursor):
    try:
        supname =input("Enter supplier name: ")
        product_id = input("Enter Product ID: ")
        product_name = input("Enter product name: ")
        cost = input("Enter cost: ")
        cursor.execute(
            "insert into Supplier(name,product_id,product_name,cost)"
            "values(%s, %s, %s, %s)",(supname,product_id,product_name,cost)
        )
        con.commit()
        print("Success")
    except Exception as e:
        print("Error: ",e)


def add_customer(con, cursor, product_id, contact):
    try:
        cursor.execute('SELECT SUM(MRP) FROM Product WHERE product_id = %s', (product_id,))
        total_amount = cursor.fetchone()[0]
        if total_amount is None:
            print("Error: Product not found.")
            return
        cursor.execute('SELECT total_visits, Total_Amount FROM Customer WHERE contact = %s', (contact,))
        customer = cursor.fetchone()

        if customer:
            total_visits = customer[0] + 1
            total_amount += customer[1]
            cursor.execute(
                "UPDATE Customer SET Total_Amount = %s, total_visits = %s WHERE contact = %s",
                (total_amount, total_visits, contact)
            )
            print("Customer updated successfully")
        else:
            print("Enter valid details")
        con.commit()

    except Exception as e:
        print("Error:", e)


def process_order(con, cursor, selected_products):
    try:
        transaction_processed = False

        print("Selected Products for Order Processing:")
        for product in selected_products:
            print(f"ProductID: {product[0]}, MRP: {product[1]}, Quantity: {product[2]}")

        for product_id, product_mrp, quantity in selected_products:

            cursor.execute(
                "SELECT quantity_available FROM Product WHERE product_id = %s", (product_id,)
            )
            available_quantity = cursor.fetchone()

            if available_quantity is None:
                print(f"Error: ProductID {product_id} does not exist.")
                continue

            available_quantity = available_quantity[0]
            print(f"Available quantity for ProductID {product_id}: {available_quantity}")

            if available_quantity >= quantity:
                amount = product_mrp * quantity
                u = input("Enter user ID: ")

                cursor.execute(
                    "INSERT INTO Transactions (date,user_id, product_id, quantity, amount) VALUES (curdate(),%s, %s, %s, %s)",
                    (u, product_id, quantity, amount)
                )

                cursor.execute(
                    "UPDATE Product SET quantity_available = quantity_available - %s WHERE product_id = %s",
                    (quantity, product_id)
                )

                print(f"Transaction for ProductID {product_id} added successfully, {quantity} units sold.")
                transaction_processed = True
            else:
                print(
                    f"Error: Insufficient stock available for ProductID {product_id}. Available: {available_quantity}, Requested: {quantity}")

        if transaction_processed:
            con.commit()
            print("Order confirmed and saved.")
        else:
            print("No transactions were processed; nothing to save.")

    except Exception as e:
        con.rollback()
        print("Error processing order:", e)


def add_pl(con,cursor):
    try:
        date2 = input("Enter date: ")
        cursor.execute("SELECT SUM(amount) FROM Transactions WHERE date = %s", (date2,))
        result_income = cursor.fetchone()
        income = result_income[0] if result_income and result_income[0] is not None else 0
        cursor.execute("select SUM(salary) from StaffAttendance where date = %s",(date2,))
        result_expenditure = cursor.fetchone()
        expenditure = result_expenditure[0] if result_expenditure and result_expenditure[0] is not None else 0
        profit_loss = float(income) - float(expenditure)
        cursor.execute(
            "insert into PL (date, income, expenditure, profit_loss)"
            "values(%s, %s, %s, %s)", (date2, income, expenditure, profit_loss))
        con.commit()
        print("Success")
    except Exception as e:
        print("Error: ",e)