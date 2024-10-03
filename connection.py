import mysql.connector as mysql

con = None
cursor = None

def connect():
    global con, cursor
    try:
        con = mysql.connect(
            host="localhost",
            user="root",
            password="12345678",
            database="supermarket",
            port=3306,
            auth_plugin='mysql_native_password'
        )
        cursor = con.cursor()
        print("Connection successful.")
        return con, cursor
    except mysql.Error as e:
        print(f"Error: {e}")
        con = None
        cursor = None
        return None, None



# if __name__ == "__main__":
# connect()
