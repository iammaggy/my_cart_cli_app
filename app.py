import subprocess
from sqlalchemy.orm import sessionmaker
import json
import config
import tabulate
import requests
import getpass
from sqlalchemy import func


session_details = requests.Session()


# Login session
def login_session(username, password):
    from data_models import User
    # Create engine
    engine = create_engine()
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    # Fetch user details using username and password
    user_list = session.query(User).filter(func.lower(User.username) == username.lower(), func.lower(User.password) == password.lower()).first()
    session.close()
    if user_list:
        # if user exist
        # store details is session
        session_details.user_id = user_list.id
        session_details.username = user_list.username
        session_details.user_role = user_list.user_role
        session_dict = {'username': user_list.username, 'user_id': user_list.id}
        if session_details.user_role == 'user':
            # if user role is user then redirect user tab
            subprocess.call("python user_view.py '%s'" % json.dumps(session_dict), shell=True)
        else:
            # if user role is admin then redirect admin tab
            subprocess.call("python admin_view.py", shell=True)
    else:
        # if user not exist
        print("Please enter correct username and password")
    return True


# To create engine
def create_engine():
    import sqlalchemy
    return sqlalchemy.create_engine(config.DATABASE_URL)


if __name__ == "__main__":

    print("------------ Welcome to MyCart ---------------")
    print("- Please log-in")
    # Take a username
    user_name = input("Enter username : ")
    # Take a password
    password = getpass.getpass("Enter password : ")
    login_session(user_name, password)