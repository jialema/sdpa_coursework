"""
@author: Jiale Ma
Shop class is defined in this file.
"""
import os
import json
import copy
import time
import math
from pprint import pprint
from customer import Customer

class Shop:
    inventory = {"hatchback":
                     {"number": 100,
                      "pricing_one": 30,
                      "pricing_two": 25,
                      "pricing_vip": 20},
                 "sedan":
                     {"number": 200,
                      "pricing_one": 50,
                      "pricing_two": 40,
                      "pricing_vip": 35},
                 "SUV":
                     {"number": 300,
                      "pricing_one": 100,
                      "pricing_two": 90,
                      "pricing_vip": 80}}

    def __init__(self, inventory_data_path = None):
        self.inventory_data_path = inventory_data_path
        if os.path.exists(self.inventory_data_path):
            with open(self.inventory_data_path, 'r') as load_f:
                self.inventory = json.load(load_f)
                # pprint(self.inventory)
        else:
            print("Path of", self.inventory_data_path, "not exists!")
            self.inventory = copy.deepcopy(Shop.inventory)
            self.save()

    def display_inventory_pricing(self, is_vip = False):
        """
        Judge whether the customer is VIP or not, and then display the inventory and price information.
        """
        print("\n[{} in shop]".format("available inventory"))
        if is_vip:
            for i, key in enumerate(self.inventory.keys()):
                print("{}.{}".format(i + 1, key))
                print("{} inventory: {}".format(' ' * 2, self.inventory[key]["number"]))
                print("{} pricing for VIP customers: {} pounds per day".format(' ' * 2, self.inventory[key]["pricing_vip"]))
        else:
            for i, key in enumerate(self.inventory.keys()):
                print("{}.{}".format(i + 1, key))
                print("{} inventory: {}".format(' ' * 2, self.inventory[key]["number"]))
                print("{} pricing for less than a week: {} pounds per day".format(' ' * 2, self.inventory[key]["pricing_one"]))
                print("{} pricing for a longer period: {} pounds per day".format(' ' * 2, self.inventory[key]["pricing_two"]))

    def process_rental_request(self):
        """
        To deal with customers' car rental request,
        it mainly realizes the interactive operation of customers' car rental.
        """
        rented_cars = {}
        is_continue = True
        while(True and is_continue):
            car_info = input("\nPlease input the type, number, and days of the car you want to rent, like SUV,3,5: ")
            try:
                car_type, car_number, days = car_info.split(',')
                car_number = int(car_number)
                days = int(days)
                if car_type in self.inventory:
                    if self.inventory[car_type]["number"] >= car_number:

                        if(days > 10000 or days < 1):
                            print("[Error] Please input the correct number of days that must be between 1 to 10,000.")
                            continue

                        if (car_number <= 0):
                            print("[Error] Please input the correct number of cars that must be between "
                                  "1 to {} (the number in stock).".format(self.inventory[car_type]["number"]))
                            continue

                        self.inventory[car_type]["number"] -= car_number

                        # Save car rental information to return these data
                        rented_cars["type"] = car_type
                        rented_cars["number"] = car_number
                        rented_cars["days"] = days

                        print("You have rented {} {}(s) for {} days successfully!".format(car_number, car_type, days))
                        break
                    else:
                        print("There are only", self.inventory[car_type]["number"], car_type, "in stock.")
                        print("[Fail] Car rental failed!")
                else:
                    print("[Error] No such car!")
            except:
                print("[Error] Invalid input!")
            # while(True):
            #     is_continue_input = input("Do you want to continue to rent car(s)? yes or no \n")
            #     if(is_continue_input == "yes"):
            #         pass
            #     elif(is_continue_input == "no"):
            #         is_continue = False
            #     else:
            #         print("[Error] Invalid input!")
            #         continue
            #     break
        self.save()
        return rented_cars

    def issue_bill(self, rented_cars = None):
        """
        Release the bill according to the user's car return information and update the inventory.
        """
        format_1, format_2 = rented_cars["time"].split('/')
        car_type = rented_cars["type"]
        car_number = rented_cars["number"]
        expected_days = rented_cars["days"]
        actual_days = math.ceil((time.time() - float(format_2)) / 86400)
        if expected_days > actual_days:
            days = expected_days
        else:
            days = actual_days
        vip = rented_cars["vip"]
        if vip:
            payment = self.inventory[car_type]["pricing_vip"] * days
            payment *= car_number
        else:
            if days > 7:
                payment = self.inventory[car_type]["pricing_one"] * 7 + \
                          self.inventory[car_type]["pricing_two"] * (days -7)
            else:
                payment = self.inventory[car_type]["pricing_one"] * days
            payment *= car_number
        self.inventory[car_type]["number"] += car_number
        print("\n[You have returned cars successfully! Here is your bill.]")
        print("Return time:", time.strftime("%H:%M:%S %d-%m-%Y", time.localtime()))
        print("Type:", car_type)
        print("Number:", car_number)
        print("Expected days:", expected_days)
        print("Actual days:", actual_days)
        print("Days for check-out:", days)
        print("Payment:", payment, "pound(s)")
        self.save()

    def save(self):
        """
        Save shop data in JSON format
        """
        with open(self.inventory_data_path, 'w') as dump_f:
            json.dump(self.inventory, dump_f)