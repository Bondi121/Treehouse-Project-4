from models import Base, session, Brands, Product, engine
from datetime import datetime
import csv
import time

def menu():
    while True:
        print('''Please select the operation you would like to perform:
        \rV) View Product
        \rN) Add a new Product
        \rA) View an analysis
        \rB) Back up of the database
        '''
        )
        user_input = input("Select any of the above options")
        if user_input.upper() in ["V", "N", "A", "B"]:
            return user_input
        else:
            input('''
            \rPlease chose one of the above options.
            ''')

def display_product_by_id(id):
    product = session.query(Product).filter(Product.product_id==id).first()


def clean_price(price):
    converted_price = None
    try:
        converted_price = float(price)
    except:
        print("Price not valid.")
        return None
    return int(converted_price * 100)


def clean_date(date):
    split_date = date.split("/")
    day = int(split_date[1])
    month = int(split_date[0])
    year = int(split_date[2])
    new_date = datetime(year, month, day)
    return new_date.date()


def inventory_add_csv():
    with open('inventory.csv') as csv_file:
        tracker = 0
        data = csv.reader(csv_file, delimiter=',')
        for product in data:
            if tracker == 0:
                tracker += 1
                continue
            brand = product[4].strip()
            check_brand = session.query(Brands).filter(Brands.brand_name==brand).first()
            dollar_price = product[1][1:]
            new_price = clean_price(dollar_price)
            new_date = clean_date(product[3])

            product = Product(brand_id=check_brand.brand_id, product_name=product[0], product_quantity=product[2], product_price=new_price, date_updated=new_date)
            session.add(product)
        session.commit()


def brands_add_csv():
    with open ('brands.csv') as f:
        initial = 0
        for brand in f:
            if initial == 0:
                initial += 1
                continue
            check_brand_in_db = session.query(Brands).filter(Brands.brand_name==brand).first()
            if check_brand_in_db == None:
                store_brand = Brands(brand_name=brand.strip())
                session.add(store_brand)
            else:
                print("Brand is already stored in Database")
        session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    #brands_add_csv()
    #inventory_add_csv()
    #app()
    menu()