from connection import cursor
def view_attendance(cursor):
    try:
        if cursor is None:
            raise Exception("Database connection not established.")
        cursor.execute("SELECT * FROM StaffAttendance")
        results = cursor.fetchall()
        print("Attendance records: ")
        for row in results:
            print(row)
    except Exception as e:
        print("Error:", e)

def view_staff(cursor):
    try:
        if cursor is None:
            raise Exception("Database connection not established.")
        cursor.execute("SELECT * FROM StaffHistory")
        results = cursor.fetchall()
        print("Staff records: ")
        for row in results:
            print(row)
    except Exception as e:
        print("Error:", e)

def view_products(cursor):
    try:
        if cursor is None:
            raise Exception("Database connection not established.")
        cursor.execute("SELECT * FROM Product")
        results = cursor.fetchall()
        print("Product records: ")
        for row in results:
            print(row)
    except Exception as e:
        print("Error:", e)

def view_supplier(cursor):
    try:
        if cursor is None:
            raise Exception("Database connection not established.")
        cursor.execute("SELECT * FROM Supplier")
        results = cursor.fetchall()
        print("Supplier records: ")
        for row in results:
            print(row)
    except Exception as e:
        print("Error:", e)

def view_customer(cursor):
    try:
        if cursor is None:
            raise Exception("Database connection not established.")
        cursor.execute("SELECT * FROM Customer")
        results = cursor.fetchall()
        print("Customer records: ")
        for row in results:
            print(row)
    except Exception as e:
        print("Error:", e)

def view_transaction(cursor):
    try:
        if cursor is None:
            raise Exception("Database connection not established.")
        cursor.execute("SELECT * FROM Transactions")
        results = cursor.fetchall()
        print("Transaction records: ")
        for row in results:
            print(row)
    except Exception as e:
        print("Error:", e)

def view_pl(cursor):
    try:
        if cursor is None:
            raise Exception("Database connection not established.")
        cursor.execute("SELECT * FROM PL")
        results = cursor.fetchall()
        print("P/L records: ")
        for row in results:
            print(row)
    except Exception as e:
        print("Error:", e)
