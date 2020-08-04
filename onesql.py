import sqlite3
import time
import datetime
#from sql import Database
import uuid

conn = sqlite3.connect('properties.db', check_same_thread=False)
c = conn.cursor()


# c.execute(finduser,(ID.get(),))

class Database():

    @staticmethod
    def create_table_user():
        c.execute("""CREATE TABLE IF NOT EXISTS user (
                user_id VARCHAR PRIMARY KEY,
                user_name VARCHAR NOT NULL UNIQUE,
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
        with conn:
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
    def select_food(slfood):
        with conn:
            c.execute(
                "SELECT * FROM food  WHERE  food_name=?", (slfood,))
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

# Database.get_user_by_user_name('zaman')

#print(Database.join_table())
# Database.get_user_by_user_name('yasa')
# Database.update_user_password('yasa', 44555666)
# Database.remove_user("777777")
# Database.join_table()
#print(Database.select_food('armut'))


db = Database()

class User:
    def __init__(self, user_name, user_password, name, surname, user_id=None, created_day=None):
        self.user_id = uuid.uuid4().hex if user_id is None else user_id
        self.user_name = user_name
        self.user_password = user_password
        self.name = name
        self.surname = surname
        self.created_day = created_day
        db.insert_user(self)

    def remove_user(self):
        db.remove_user(self)

    def get_user(self):
        return db.get_user_by_user_name(self)

    def update_user(self, username):
        return db.update_user_password(self, username)


class Address(User):
    def __init__(self, address_type, street_name, street_number, flat_no, address_id=None):
        self.address_id = uuid.uuid4().hex if address_id is None else address_id
        self.address_type = address_type
        self.street_name = street_name
        self.street_number = street_number
        self.flat_no = flat_no
        db.insert_address(self)


class Seller(User):
    def __init__(self, User, Address, seller_id=None):  # ilgilen
        self.seller_id = seller_id
        self.address_id = Address.address_id
        self.user_id = User.user_id
        self.user_name = User.user_name
        db.insert_seller(self)


class Buyer(User):
    def __init__(self, Order, User, Address, buyer_id=None):
        self.buyer_id = buyer_id
        self.order_id = Order.order_id
        self.address_id = Address.address_id
        self.user_name = User.user_name
        self.user_id = User.user_id
        db.insert_buyer(self)



class Food:
    def __init__(self, food_name, food_id=None):
        self.food_id = uuid.uuid4().hex if food_id is None else food_id
        self.food_name = food_name
        db.insert_food(self)

    def get_food(self):
        return db.select_food(self)


class Order(Food):
    def __init__(self, Food, order_id=None, order_date=None):
        self.order_id = uuid.uuid4().hex if order_id is None else order_id
        self.order_date = order_date
        self.food_id = Food.food_id
        self.food_name = Food.food_name
        db.insert_order(self)


User(user_name="sami", user_password="987978", name="qwe", surname="rwe") # okay
# User.remove_user('sami') # okay
# User.get_user("Yakup01")
# User.update_user('zalim',9636969) # okay
# Food('iskender') # okay
# Address(address_type='company', street_name='hosdere', street_number='02', flat_no='05', city_name='Akara', zip_code='135654')
# Order(Food.food_id)
# print(A.name)
# Food('lahmacun')
# Order('lahmacun')
# Seller()
# Address(address_type='company', street_name='hosdere', street_number='2', flat_no='3', zip_code='12312', city_name='Ankara')

#Order(Food('cacık'))
# User(user_name="mahmut", name="mert", surname="rwe", user_password='789654')
#Seller(User(user_name="sami", user_password="987978", name="qwe", surname="rwe"),Address(address_type='company',
# street_name='hosdere', street_number='2', flat_no='3', zip_code='12312', city_name='Ankara'))
#A =User(user_name="sami", user_password="987978", name="qwe", surname="rwe")
#B = Address(address_type='company', street_name='hosdere', street_number='2', flat_no='3', zip_code='12312', city_name='Ankara')
#C = Seller(A,B)

#food1 =Food('döner')
#food1 = Food('cacık')
#order1 = Order(Food('çekirdek')),
#a = Food('yasak ceviz')
#order = Order(a)
#address4 =Address(street_name='dfgg', street_number='14', flat_no='17')
#user5 = User(user_name="güresci", user_password="1115562992", name="mero", surname="qewgh")
#seller =Seller(User=user5, Address=address4)
#buyer1 = Buyer(Order=order, User=user5, Address=address4)
#Address(street_name='werrrt', address_type='company', street_number='33', flat_no='56')


#User(user_name="atesli", user_password="89751", name="ibrahim", surname="tatlıses")
#data= User.get_user('atesli')
#print(data)
#User.get_user('atesli')
#User.update_user('musaa','888888')
#User.remove_user('musaa')


#User.update_user('atesli', '123321123')
#a = Food.get_food('elma')
#print(a)
#Order(a)
