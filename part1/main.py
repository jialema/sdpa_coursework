#-*-coding:utf-8-*-

"""
@author: Jiale Ma
This is the main.py of the car rental system program.
Run this file to start the program.
"""

import os
import json
from customer import Customer
from shop import Shop
from customer_vip import CustomerVIP

CUSTOMERS_DIRECTORY = "data/customers"  # the path of storing data about car rental information
INVENTORY_DATA_PATH = "data/inventory.json"

def log_in():
    """Return the instance of Customer or CustoerVIP
    First, load the user data file to show which users are in the current database.
    Then, enter the user name. If the user already exists, the data will be loaded.
    If the user does not exist, the user will be created, and ask if they want to be a VIP.
    """

    # If the data folder does not exist, create it.
    if not os.path.exists(CUSTOMERS_DIRECTORY):
        os.makedirs(CUSTOMERS_DIRECTORY)

    # Load user data
    customers_data = os.listdir(CUSTOMERS_DIRECTORY)
    customers_names = [ele[:-5] for ele in customers_data]
    if customers_names != []:
        print("Users in current database:")
        print(customers_names)

    username = input("Please input your username: ")
    data_path = os.path.join(CUSTOMERS_DIRECTORY, username + ".json")

    # Judge whether user exists and create user
    if username in customers_names:
        with open(data_path, 'r') as load_f:
            rented_cars = json.load(load_f)
        if rented_cars["vip"]:
            user = CustomerVIP(data_path, rented_cars)
        else:
            user = Customer(data_path, rented_cars)
    else:
        user = None
        while (True):
            be_vip = input("Do you want to be a VIP member? yes or no \n")
            if (be_vip == "yes"):
                user = CustomerVIP(data_path)
            elif (be_vip == "no"):
                user = Customer(data_path)
            else:
                print("[Error] invalid input!")
                continue
            break

    return user

def initialization():
    """initialization()
    Startup interface display of Car Rental System
    """
    try:
        width_terminal = os.get_terminal_size().columns
    except:
        width_terminal = 100
    title = "Car Rental System"
    length_title = len(title)
    length_underline = (width_terminal - length_title) // 2
    print("{}{}{}".format("-" * length_underline, title , "-" * length_underline))

def main():
    # clear terminal or console
    # os.system('cls')

    # User login
    user = log_in()

    # Interface initialization
    initialization()

    # Initialize shop
    rental_shop = Shop(INVENTORY_DATA_PATH)

    # Start to operate related instructions
    user.run(rental_shop)

if __name__ == '__main__':
    main()