import mysql.connector as mysql
from table import create_tables
from insert import add_pl, add_staff, add_customer, add_products, add_supplier, process_order, add_attendance
from viewer import view_pl, view_staff, view_attendance, view_customer, view_products, view_transaction, view_supplier
from connection import connect, cursor, con

con = None
cursor = None


def admin_login(selected_products,product_id, contact,con,cursor):
    try:
        print("1->New user\n2->User login\n3->Customer signup\n4->Customer Login\n5->Staff login\n5->Exit")
        opt = input("Enter your option: ")
        if opt == '1':
            u = input("Enter username: ")
            p = input("Enter password: ")
            cursor.execute(
                "insert into user_login (user_id, password) values (%s, %s)",
                (u, p))
            con.commit()
            print("New user registration successful")
        elif opt == '2':
            print("Enter Login details: ")
            us = input("Enter username: ")
            pa = input("Enter password: ")
            cursor.execute(
                'select user_id, password from user_login where user_id = %s and password = %s', (us, pa)
            )
            result_user = cursor.fetchall()
            if not result_user:
                print("No such user found")
            else:
                print("Login successful")
                admin(con, cursor, selected_products,product_id, contact)
        elif opt == '3':
            user_c = input("Enter username: ")
            password_c = input("Enter password: ")
            contact_c = input("Enter contact details: ")
            nn = input("Enter your name: ")
            cursor.execute(
                "insert into Customer(user_id, password, contact, name) values (%s, %s, %s, %s)",
                (user_c, password_c, contact_c, nn))
            con.commit()
            print("New customer registration successful")
        elif opt == '4':
            u = input("Enter username: ")
            p = input("Enter Password: ")
            cursor.execute(
                'select user_id, password from Customer where user_id = %s and password = %s', (u, p)
            )
            result_customer = cursor.fetchall()
            if not result_customer:
                print("No such record found")
            else:
                print("Login successful")
            print('1->Buy products\n2->View purchase history by month\n3->View purchase history by date')
            zz = input('Enter Option: ')
            if zz == '1':
                buy_products(selected_products, con, cursor)
            elif zz == '2':
             cursor.execute(
                 "SELECT DATE_FORMAT(date, '%Y-%m') AS month, SUM(amount) FROM Transactions GROUP BY month"
                )
             results = cursor.fetchall()
             for row in results:
                 print(f"Month: {row[0]}, Total Amount: {row[1]}")
            elif zz == '3':
                date_input = input("Enter date to view transactions: ")
                cursor.execute(
                    'select sum(amount) from Transactions where date = %s',(date_input,)
                )
                res = cursor.fetchall()[0]
                print(f'Total amount spent on {date_input} : {res}')

            else:
                print("Enter valid input")
        elif opt == '5':
            a = input("Enter staff id: ")
            b = input("Enter your name: ")
            cursor.execute('select staff_id, name from StaffHistory where staff_id = %s and name = %s',(a,b))
            r = cursor.fetchall()
            if not r:
                print("No such staff found")
            else:
                print(f"Welcome back {b}")
            print("Enter new product: ")
            add_products(con, cursor)
        else:
            print("Enter valid input")


    except Exception as e:
        print("Error: ", e)
def buy_products(selected_products,con,cursor):
    try:
            product_selection(con, cursor)
    # return selected_products

    except Exception as e:
     print("Error: ",e)


def product_selection(con, cursor):
    try:
        print("Available products:")
        cursor.execute("SELECT product_id, name, mrp FROM Product")
        products = cursor.fetchall()
        for i in products:
            print(f"ProductID: {i[0]}, Name: {i[1]}, Price: {i[2]}")

        selected_products = []
        total_mrp = 0

        while True:
            product_id = input("Enter ProductID (or type 'done' to finish): ")
            if product_id.lower() == 'done':
                break
            quantity = input("Enter quantity: ")
            quantity = int(quantity)

            cursor.execute('SELECT mrp FROM Product WHERE product_id = %s', (product_id,))
            pro = cursor.fetchone()

            if not pro:
                print("Invalid selection. Please enter a valid ProductID.")
            else:
                selected_products.append((product_id, pro[0], quantity))
                total_mrp += pro[0] * quantity
                print(f"Added ProductID {product_id}, current total: {total_mrp}")

        print(f"Total bill: {total_mrp}")
        confirm = input("Do you want to confirm your order? (yes/no): ").lower()

        if confirm == 'yes':
            process_order(con, cursor, selected_products)
        else:
            print("Order cancelled.")

    except Exception as e:
        print("Error during product selection:", e)


def main():
    global con, cursor
    con, cursor = connect()

    if con and cursor:
        product_id = None
        contact = 0
        selected_products = []
        create_tables(cursor, con)
        selected_products = admin_login(selected_products,product_id, contact,con,cursor)
    else:
        print("Connection to the database failed.")


def admin_options(con, cursor, selected_products, product_id, contact):
    try:
        while True:
            print("Welcome to Supermarket")
            print("1->Add Attendance")
            print("2->Add Staff")
            print("3->Add Supplier")
            print("4->EOD")
            print("5->Exit")

            option = input("Enter your option: ")
            if option == '1':
                add_attendance(con, cursor)
            elif option == '2':
                add_staff(con, cursor)
            elif option == '3':
                add_supplier(con, cursor)
            elif option == '4':
                add_pl(con, cursor)
            elif option == '5':
                break
            else:
                print("Invalid option")
    except Exception as e:
        print("Error: ", e)


def admin(con, cursor, selected_products,product_id, contact):
    try:
        while True:
            print("Welcome to Supermarket")
            print("1->View Staff Attendance")
            print("2->View Staff History")
            print("3->View Products")
            print("4->View Supplier info")
            print("5->View Customer data")
            print("6->View Transaction history")
            print("7->View P/L")
            print("8->Insert data")
            print("9->Exit")
            option = input("Enter your option: ")
            if option == '1':
                view_attendance(cursor)
            elif option == '2':
                view_staff(cursor)
            elif option == '3':
                view_products(cursor)
            elif option == '4':
                view_supplier(cursor)
            elif option == '5':
                view_customer(cursor)
            elif option == '6':
                view_transaction(cursor)
            elif option == '7':
                view_pl(cursor)
            elif option == '8':
                admin_options(con, cursor, selected_products,product_id, contact)
            elif option == '9':
                break
            else:
                print("Invalid option")

    except Exception as e:
        print("Error: ", e)


if __name__ == "__main__":
    main()


# 1.New admin
# 2.Admin login
#     1->View Staff Attendance
#     2->View Staff History
#     3->View Products
#     4->View Supplier info
#     5->View Customer data
#     6->View Transaction history
#     7->View P/L
#     8->Insert data
#         1->Add Attendance
#         2->Add Staff
#         3->Add Supplier
#         4->EOD
# 3.Customer signup
# 4.Customer login
#     1->Buy products
#       1. Choose from Products
#       2. choose quantity
#       3. Add to transaction and update product table
#     2->View purchase history by month
#     3->View purchase history by date
# 5. Staff login
#    1. Add Products

