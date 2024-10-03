import mysql.connector as mysql
from connection import connect, con, cursor
def create_tables(cursor,con):
    try:
        if con is None or cursor is None:
            connect()
        cursor.execute('''
        create table if not exists user_login(user_id varchar(100),
        password varchar(50)
        );
        ''')
        # Create the Product Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                product_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255),
                quantity_available INT,
                supplierID INT
            );
        ''')

        # Create the Supplier Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Supplier (
                supplierID INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255),
                product_id INT,
                product_name VARCHAR(200),
                cost DECIMAL(10, 2),
                FOREIGN KEY (product_id) REFERENCES Product(product_id)
            );
        ''')

        # Create the Staff History Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS StaffHistory (
                staff_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255),
                designation VARCHAR(100),
                contact VARCHAR(15),
                email VARCHAR(100),
                address TEXT,
                dob DATE,
                hire_date DATE,
                salary DECIMAL(10, 2)
            );
        ''')

        # Create the Staff Attendance Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS StaffAttendance (
                attendance_id INT PRIMARY KEY AUTO_INCREMENT,
                date DATE,
                staff_id INT,
                clockIN TIME,
                clockOUT TIME,
                salary int,
                FOREIGN KEY (staff_id) REFERENCES StaffHistory(staff_id)
            );
        ''')

        # Create the Transactions Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transactions (
                transaction_id INT PRIMARY KEY AUTO_INCREMENT,
                date DATE, user_id varchar(200),
                product_id INT,
                quantity INT,
                amount DECIMAL(10, 2),
                FOREIGN KEY (product_id) REFERENCES Product(product_id)
            );
        ''')

        # Create the Profit and Loss (P/L) Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS PL (
                pl_id INT PRIMARY KEY AUTO_INCREMENT,
                date DATE,
                income DECIMAL(10, 2),
                expenditure DECIMAL(10, 2),
                profit_loss DECIMAL(10, 2)
            );
        ''')

        # Create Customer Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Customer (
               CustomerID INT PRIMARY KEY AUTO_INCREMENT,
               name varchar(50),
               user_id varchar(50),
               password varchar(50),
               contact INT,
               Total_Amount INT,
               total_visits INT
            );
        ''')

        print("All tables created successfully.")
        con.commit()

    except mysql.Error as e:
        print(f"Error creating tables: {e}")
