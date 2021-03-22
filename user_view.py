import sys
from app import create_engine
from sqlalchemy.orm import sessionmaker
import click
from sqlalchemy import func
from tabulate import tabulate
import yaml
import json


# Show details in tabular format
def tabular_format_details(details, header):
    # Remove unwanted keys
    header.remove('registry')
    header.remove('to_dict')
    final_list = {}
    # Generate data array and pass to tabulate object
    for data in header:
        row_val = list(map(lambda x: x[data], details))
        final_list[data] = row_val
    return tabulate(final_list, headers='keys', tablefmt='pretty')


# To show dialog
def show_dialog():
    with open('data_files/admin_details.yaml') as file:
        dialog = yaml.safe_load(file)
        print(dialog['user_dialog']["title"])
        for option in dialog['user_dialog']["options"]:
            print(option, end="")
        option = input("Enter your choice : ")
    return select_option(option)


# Take choice and perform corresponding operation
def select_option(option):
    if option == '1':
        return sub_category(category_name)
    elif option == '2':
        return show_cart_details(session_data['username'])
    elif option == '3':
        return buy_products(session_data['username'])
    else:
        return "Please select correct option"


# To show category and subcategory
def sub_category(category_name):
    from data_models import Categories
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    sub_category_list = [k.to_dict() for k in session.query(Categories).filter(func.lower(Categories.base_category) == category_name.lower()).all()]
    session.close()

    if len(sub_category_list) > 0:
        # if category list exist then go to another subcategory
        for cat in sub_category_list:
            print(" - ", cat['category_name'])
        cat_name = input("Enter your choice : ")
        return sub_category(cat_name)
    else:
        # if category list does'nt exist then go to product list
        return show_product_section(category_name)


# To show product section
def show_product_section(category_name):
    from data_models import Products, Categories
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    product_list = [k.to_dict() for k in session.query(Products).filter(Products.category_id == Categories.id, func.lower(Categories.category_name) == category_name.lower()).all()]
    session.close()
    if len(product_list):
        header = list(product_list[0].keys())
        table = tabular_format_details(product_list, header)
        print(table)
    return add_to_cart()

# To add product in cart
@click.command()
@click.option("--product_id", prompt="Enter choice to add product to cart or 0 to exit ")
def add_to_cart(product_id):
    from data_models import Products, Cart
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    if product_id == '0':
        return show_dialog()
    else:
        cart = Cart()
        cart.client_id = session_data['user_id']
        cart.product_id = product_id
        cart.status = "In-progress"
        cart.client_username = session_data['username']
        session.add(cart)
        session.commit()
    session.close()
    return show_cart_details(session_data['username'])


# To show cart details
def show_cart_details(user_name):
    from data_models import Cart, Products
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    cart_list = [k.to_dict() for k in session.query(Products).filter(Products.id == Cart.product_id, Cart.client_username == user_name).all()]
    header = list(cart_list[0].keys())
    table = tabular_format_details(cart_list, header)
    print(table)
    session.close()
    # Show dialog to buy product and to remove product from cart
    with open('data_files/admin_details.yaml') as file:
        dialog = yaml.safe_load(file)
        print(dialog['cart_details']["title"])
        for option in dialog['cart_details']["options"]:
            print(option, end="")
        choice = input("Enter your choice : ")
    if choice.lower() == '1':
        # To buy product
        return buy_products(user_name)
    elif choice.lower() == '2':
        # To remove product
        return remove_item_from_cart(user_name)
    else:
        return show_dialog()


# To buy products
def buy_products(user_name):
    from data_models import Cart, Products
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    cart_list = [k.to_dict() for k in session.query(Products).filter(Products.id == Cart.product_id, Cart.client_username == user_name).all()]
    session.close()
    header = list(cart_list[0].keys())
    table = tabular_format_details(cart_list, header)
    # print(table)
    sum_list = list(map(lambda x: x['product_price'], cart_list))
    print("Actual Price : ", sum(sum_list))
    if sum(sum_list) >= 10000:
        print("Discounted Price : 500", )
        print("Net Price : ", (sum(sum_list) - 500))
    else:
        print("Net Price : ", sum(sum_list))


# Remove item from cart
def remove_item_from_cart(user_name):
    from data_models import Cart, Products
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    cart_list = [k.to_dict() for k in session.query(Products).filter(Products.id == Cart.product_id,Cart.client_username == user_name).all()]
    header = list(cart_list[0].keys())
    table = tabular_format_details(cart_list, header)
    print(table)
    choice = input("Enter product id to remove product from cart : ")
    # Fetch cart details on selected product id
    cart_details = session.query(Cart).filter_by(product_id=choice).first()
    session.delete(cart_details)
    session.commit()
    session.close()
    return show_cart_details(user_name)


if __name__ == '__main__':
    category_name = 'NA'
    session_data = json.loads(sys.argv[1])
    # session_data = {"username": "mkadam", "user_id": 1}
    print("---------- welcome to shopping bucket ------------")
    show_dialog()