import click
import yaml
from app import create_engine
from sqlalchemy.orm import sessionmaker
from user_view import tabular_format_details


# Select option
@click.command()
@click.option("--option", prompt="Enter your choice ")
def select_option(option):
    func = func_list['%s' % option]
    return func()


# Show dialog
def show_dialog():
    # Read yaml file and show admin details to perform operation
    with open('data_files/admin_details.yaml') as file:
        dialog = yaml.safe_load(file)
        print(dialog['admin_dialog']["title"])
        for option in dialog['admin_dialog']["options"]:
            print(option, end="")
    return select_option()

# To add category, accept the choice using option
@click.command()
@click.option("--category_name", prompt="Enter category name ")
@click.option("--category_level", prompt="Enter category level ")
@click.option("--base_category", prompt="Enter base category ")
def add_categories(base_category, category_name, category_level):
    from data_models import Categories
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    # Fetch category list
    category_list = [k.to_dict() for k in session.query(Categories).filter_by(category_name=category_name).all()]
    if len(category_list) > 0:
        # If details exist alreday
        print("Category details already present")
    else:
        # If details not exist then add
        category = Categories()
        category.base_category = base_category
        category.category_name = category_name
        category.category_level = category_level
        session.add(category)
        session.commit()
    session.close()
    return show_categories()


@click.command()
@click.option("--category_id", prompt="Enter category id ")
@click.option("--category_name", prompt="Enter category name ")
@click.option("--product_name", prompt="Enter product name ")
@click.option("--product_details", prompt="Enter product details ")
@click.option("--product_price", prompt="Enter product price")
def add_products(category_id, product_name, product_details, product_price, category_name):
    from data_models import Products
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    product_list = [k.to_dict() for k in session.query(Products).filter_by(product_name=product_name).all()]
    if len(product_list) > 0:
        print("Product details already present")
    else:
        products = Products()
        products.category_id = category_id
        products.category_name = category_name
        products.product_name = product_name
        products.product_details = product_details
        products.product_price = product_price
        session.add(products)
        session.commit()
    session.close()
    return show_products()


def show_categories():
    from data_models import Categories
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    category_list = [k.to_dict() for k in session.query(Categories).all()]
    header = list(category_list[0].keys())
    table = tabular_format_details(category_list, header)
    print(table)
    return show_dialog()


def show_products():
    from data_models import Products
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    product_list = [k.to_dict() for k in session.query(Products).all()]
    header = list(product_list[0].keys())
    table = tabular_format_details(product_list, header)
    print(table)
    session.close()
    return show_dialog()


def user_details_to_show_cart():
    from data_models import User
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    user_list = [k.to_dict() for k in session.query(User).all()]
    print("Choose user to see cart details :")
    header = list(user_list[0].keys())
    table = tabular_format_details(user_list, header)
    print(table)
    session.close()
    return show_cart_details()


@click.command()
@click.option("--user_name", prompt="Enter desire username to see cart details ")
def show_cart_details(user_name):
    from data_models import Cart
    engine = create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    cart_list = [k.to_dict() for k in session.query(Cart).filter_by(client_username=user_name).all()]
    header = list(cart_list[0].keys())
    table = tabular_format_details(cart_list, header)
    print(table)
    session.close()
    return show_dialog()


def to_exit():
    return "You exit dashboard successfully"


if __name__ == '__main__':
    func_list = {
        '1': add_categories,
        '2': add_products,
        '3': show_categories,
        '4': show_products,
        '5': user_details_to_show_cart,
        '6': to_exit
    }
    show_dialog()