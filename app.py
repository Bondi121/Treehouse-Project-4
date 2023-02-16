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
            \rPlease chose one of the above options. Click "Enter" to see the menu again.
            ''')
        
        

def analyzing_database():
    items = session.query(Product).order_by(Product.product_price).all()
    lowest_product_price = items[0]
    highest_product_price = items[-1]
    brands = session.query(Brands).all()
    brand_products = []

    for brand in brands:
        brand_products.append((len(brand.products), brand.brand_name))
        
    brand_with_highest_product = max(brand_products)
    
    print(f"{lowest_product_price.product_name} has the lowest price of {lowest_product_price.product_price}.")
    print(f"{highest_product_price.product_name} has the highest price of {highest_product_price.product_price}.")
    print(f"{brand_with_highest_product[1]} has the most product of {brand_with_highest_product[0]} products.")


def adding_product():
    product = input("Please enter the new product name: ").strip()
    brand_name = input("Please enter the brand name: ").strip()
    
    check_brand = session.query(Brands).filter(Brands.brand_name==brand_name).first()
    if check_brand == None:
        print("Brand doesn't exist")
        return None

    while True:
        quantity = input("Please enter the quantity: ")
        try:
            quantity = int(quantity)
            break
        except:
            print("Please insert a proper value(example: 5)")

    
    while True:
        price = input("Please enter the price (example: $5.99): ")
        while price[0] != "$":
            price = input("Your answer needs to start with a $, Please enter the price (example: $5.99): ")

        try:
            price = price[1:]
            new_price = clean_price(price)
            print(new_price)
            break
        except:
            print("Please insert a proper value(example: 5)")
    
    product_date = datetime.now()
    product_date = product_date.date()

    new_product = Product(product_name=product, brand_id=check_brand.brand_id, product_quantity=quantity, product_price=new_price, date_updated=product_date)
    session.add(new_product)
    session.commit()
    print(f'Product created {new_product.product_name}')
    return new_product


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
            check_product_in_db = session.query(Product).filter(Product.product_name==product[0].strip()).first()
            if check_product_in_db is None:
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
            check_brand_in_db = session.query(Brands).filter(Brands.brand_name==brand.strip()).first()
            if check_brand_in_db is None:
                store_brand = Brands(brand_name=brand.strip())
                session.add(store_brand)
        session.commit()


def display_product_by_id():
    while True:
        product_id = input("Input the Product ID you would like to fetch: ")
        product = session.query(Product).filter(Product.product_id==product_id).first()
        if product:
            print(f'Your selected product is: Product name: {product.product_name} - Brand name: {product.brand.brand_name} - Quantity: {product.product_quantity} - Price: {product.product_price} - Date updated: {product.date_updated}')
            return product
        else:
            print("Product doesn't exist, please enter a proper product id")



def export_data():
    export_brands()
    export_inventory()


def export_brands():
    outfile = open('brands_backup.csv', 'w')
    outcsv = csv.writer(outfile)
    records = session.query(Brands).all()
    header = (Brands.__table__.columns.keys())

    outcsv.writerow(header)
    data = []
    for brand in records:
        data.append((brand.brand_id, brand.brand_name))
    outcsv.writerows(data)
    outfile.close()



def export_inventory():
    outfile = open('inventory_backup.csv', 'w')
    outcsv = csv.writer(outfile)
    records = session.query(Product).all()
    header = (Product.__table__.columns.keys())

    outcsv.writerow(header)
    data = []
    for product in records:
        data.append((product.product_id, product.brand_id, product.product_name, product.product_quantity, product.product_price, product.date_updated))
    outcsv.writerows(data)
    outfile.close()


def app():
    decision = menu().upper()
    print(decision)
    if decision == "V":
        display_product_by_id()
    elif decision == "N":
        adding_product()
    elif decision == "A":
        analyzing_database()
    elif decision == "B":
        export_data()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    brands_add_csv()
    inventory_add_csv()
    app()