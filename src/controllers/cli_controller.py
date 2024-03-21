from flask import Blueprint
from src import db, bcrypt
from datetime import date
from src.models.user import User
from src.models.product import Product
from src.models.promotion import Promotion
from src.models.purchase import Purchase
from src.models.store import Store
from src.models.alert import Alert

# Create blueprint for CLI Controller
db_commands = Blueprint('db', __name__)

# Initilaise database
@db_commands.cli.command('init')
def initialise_database():
    db.drop_all()
    db.create_all()
    print("Flask application has been initialised")


# Create tables in database 
@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print("Tables created succesfully")

# Drop tables from database
@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print("Tables dropped successfully")

# Seed tables into database
@db_commands.cli.command('seed')
def seed_tables():

    # Seed data for users
    users = [
        User(
            username ="User 1",
            email="User1@email.com",
            password=bcrypt.generate_password_hash('abcd1234').decode('utf-8')
        ),
        User( 
            username ="User 2",
            email="User2@email.com",
            password=bcrypt.generate_password_hash('abcd1234').decode('utf-8')
        )
    ]
    
    db.session.add_all(users)

    # Seed data for products
    products = [
        Product(
            product_name="Wholemeal Bread",
            product_brand="Wonder White",
            product_category="Baked Goods"
        ),
        Product( 
            product_name="Denim Jeans",
            product_brand="G-Star RAW",
            product_category="Clothing"
        )
    ]

    db.session.add_all(products)

    # Seed data for promotions
    promotions = [
        Promotion(
            promotion_type="Percentage discount",
            promotion_discount="0.4" # Utilising decimal value over percentge to allow for easier data manipulation
        ),
        Promotion(
            promotion_type="Buy 1 get 1 free",
            promotion_discount=None
        )
    ]

    db.session.add_all(promotions)

    # Seed data for stores     
    stores = [
        Store(
            store_name="Woolworths",
            store_type="Grocery",
            location="123 Example Street, Sydney, NSW, 2000"
        ),
        Store(
            store_name="Cotton On",
            store_type="Clothing",
            location="Example Mall, 123 Test Street, Sydney, NSW, 2000"
        )
    ]

    db.session.add_all(stores)

    # Seed data for purchases
    purchases = [
        Purchase(
            product_id=[0],
            store_id=[0],
            promotion_id=[0],
            user=users[1],
            price= 5.00,
            purchase_date= date.today()
        ),
        Purchase(
            product_id=[1],
            store_id=[1],
            promotion_id=[1],
            user=users[0],
            price=60.00,
            purchase_date= date.today()
        )
    ]

    db.session.add_all(purchases)

    # Seed data for alerts
    alerts = [
        Alert(
            user=users[0],
            product=products[1],
            day_of_week='Tuesday'
        ),
        Alert(
            user=users[0],
            product=products[1],
            day_of_week='Friday'
        )
    ]

    db.session.add_all(alerts)

    # Commit tables into database
    db.session.commit()

    print("Tables seeded successfully")