import sqlite3
import time
import datetime

conn = sqlite3.connect('properties.db', check_same_thread=False)
c = conn.cursor()


# c.execute(finduser,(ID.get(),))

class Database():

    @staticmethod
    def create_table_user():
        c.execute("""CREATE TABLE IF NOT EXISTS user (
                user_id VARCHAR PRIMARY KEY,
                user_name VARCHAR NOT NULL,
                user_password VARCHAR NOT NULL,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                created_date DATE NOT NULL
                )""")
        conn.commit()

        print('Create table user finished successfully.')

    @staticmethod
    def create_table_address():
        c.execute("""CREATE TABLE IF NOT EXISTS address (
                address_id VARCHAR PRIMARY KEY,
                address_type TEXT NOT NULL,
                street_name VARCHAR NOT NULL,
                street_number NUMERIC NOT NULL,
                flat_no NUMERIC NOT NULL
                )""")
        conn.commit()

        print('Create table address finished successfully.')

    @staticmethod
    def create_table_seller():
        c.execute("""CREATE TABLE IF NOT EXISTS seller (
                        seller_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name VARCHAR NOT NULL,
                        user_id VARCHAR NOT NULL,
                        address_id NUMERIC NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES user(user_id), 
                        FOREIGN KEY(address_id) REFERENCES address(address_id) 
                        )""")
        conn.commit()

        print('Create table seller finished successfully.')

    @staticmethod
    def create_table_buyer():
        c.execute("""CREATE TABLE IF NOT EXISTS buyer (
                        buyer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name VARCHAR NOT NULL,
                        user_id VARCHAR NOT NULL,
                        address_id NUMERIC NOT NULL,
                        order_id NUMERIC NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES user(user_id), 
                        FOREIGN KEY(address_id) REFERENCES address(address_id), 
                        FOREIGN KEY(order_id) REFERENCES orders(order_id)  
                        )""")
        conn.commit()

        print('Create table buyer finished successfully.')

    @staticmethod
    def create_table_food():
        c.execute("""CREATE TABLE IF NOT EXISTS food ( 
                food_id VARCHAR PRIMARY KEY,
                food_name TEXT NOT NULL,
                UNIQUE(food_name)
                )""")
        conn.commit()

        print('Create table food finished successfully.')

    @staticmethod
    def create_table_order():
        c.execute("""CREATE TABLE IF NOT EXISTS orders (
                order_id VARCHAR PRIMARY KEY,
                food_id VARCHAR NOT NULL,
                food_name TEXT NOT NULL,
                order_date DATE NOT NULL
                )""")
        conn.commit()

        print('Create table order finished successfully.')

    @staticmethod
    def insert_user(inuser):
        unix = int(time.time())
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
        with conn:  # connection
            c.execute(
                "INSERT INTO user VALUES (?, ?, ?, ?, ?, ?)",
                (inuser.user_id, inuser.user_name,
                 inuser.user_password,
                 inuser.name, inuser.surname, date))

    @staticmethod
    def get_user_by_user_name(username):
    #with conn:
        c.execute("SELECT * FROM user WHERE user_name=?", (username,))
        data = c.fetchone()
        return data

    @staticmethod
    def update_user_password(username, user_password):
        with conn:
            c.execute("""UPDATE user SET user_password =?
                        WHERE user_name =?""",
                      (user_password, username))

    @staticmethod
    def remove_user(username):
        with conn:
            c.execute("DELETE from user WHERE user_name =?", (username,))
            return c.fetchall()

    @staticmethod
    def insert_address(inaddress):
        with conn:
            c.execute(
                "INSERT INTO address VALUES (?, ?, ?, ?, ?)",
                (inaddress.address_id, inaddress.address_type, inaddress.street_name, inaddress.street_number, inaddress.flat_no))

    @staticmethod
    def insert_food(infood):
        with conn:
            c.execute(
                "INSERT INTO food VALUES (?, ?)", (infood.food_id, infood.food_name))
    @staticmethod
    def select_food():
        with conn:
            c.execute(
                "SELECT * FROM food")
            fd = c.fetchone()
            return fd

    @staticmethod
    def insert_order(inorder):
        unix = int(time.time())
        date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))
        with conn:  # connection
            c.execute(
                "INSERT INTO orders VALUES (?, ?, ?, ?)",
                (inorder.order_id, inorder.food_id, inorder.food_name, date))

    @staticmethod
    def join_table():
        with conn:
            c.execute("""SELECT food.food_name AS food_name, address.address_type AS address_type,
            orders.order_date AS order_date
            FROM
            food
            LEFT JOIN address ON address.address_type = address_type LEFT JOIN orders 
            ON orders.order_date = order_date""")
        rows = c.fetchall()  # get the remaining rows as a list
        for row in rows:
            return row


    @staticmethod
    def insert_seller(inseller):
        with conn:
            c.execute(
                "INSERT INTO seller VALUES (?, ?, ?, ?)",
                (inseller.seller_id, inseller.user_name, inseller.user_id, inseller.address_id))

    @staticmethod
    def insert_buyer(inbuyer):
        with conn:
            c.execute(
                "INSERT INTO buyer VALUES (?, ?, ?, ?, ?)",
                (inbuyer.buyer_id, inbuyer.user_name, inbuyer.user_id, inbuyer.address_id, inbuyer.order_id))


Database.create_table_user()
Database.create_table_address()
Database.create_table_food()
Database.create_table_order()
Database.create_table_seller()
Database.create_table_buyer()

# print(Database.join_table())



# Database.get_user_by_user_name('zaman')

# print(Database.join_table())
# Database.get_user_by_user_name('yasa')
# Database.update_user_password('yasa', 44555666)
# Database.remove_user("777777")
# Database.join_table()
# print(Database.select_food('armut'))
