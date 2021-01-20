"""
@author: Jiale Ma
Customer class is defined in this file.
A Customer instance can query the current inventory, rent cars and return cars.
"""
import os
import sys
import copy
import json
import time
import math

class Customer:
    # Define the basic information of the user
    basic_rental_info = {"type": None,
                         "number": None,
                         "days": None,
                         "time": None,
                         "vip": False}

    def __init__(self, data_path = None, rented_cars = None):
        self.data_path = data_path
        if rented_cars == None:
            self.rented_cars = copy.deepcopy(self.basic_rental_info)
        else:
          self.rented_cars = rented_cars

    def run(self, rental_shop):
        """
        rental_shop: the instance of Shop class
        When the user instance executes this function,
        it formally interacts with the car rental system through instruction.
        """
        self.rental_shop = rental_shop
        while (True):
            print("\n[instructions]")
            instruction = input("1: inquire about available stock and prices.\n"
                                "2: rent car(s).\n"
                                "3: return car(s).\n"
                                "q: exit.\n"
                                "please input the number of the instruction you want to operate and press Enter: ")
            if (instruction == '1'):
                self.inquire()
            elif instruction == '2':
                self.rent_car()
            elif instruction == '3':
                self.return_car()
            elif instruction == 'q':
                break
            else:
                print("[Error] invalid input!")
            input("\npress Enter to continue...")

    # def load_data(self):
    #     with open(self.data_path, 'r') as load_f:
    #         self.rented_cars = json.load(load_f)

    def inquire(self):
        """
        Inquiry about inventory
        """
        self.rental_shop.display_inventory_pricing(self.basic_rental_info["vip"])

    def rent_car(self):
        """
        Rent car(s) from shop and save data to local.
        """
        if self.rented_cars["type"]:
            print("\n[Fail] Only if you return the cars you have rented, you can rent new cars!")
            self.print_rental_info()
            return
        rented_cars = self.rental_shop.process_rental_request()
        if rented_cars != {}:
            rental_time = time.strftime("%H:%M:%S %d-%m-%Y", time.localtime()) + '/' + str(time.time())
            rented_cars["time"] = rental_time
            rented_cars["vip"] = self.basic_rental_info["vip"]
            self.rented_cars = rented_cars
            self.save()

    def return_car(self):
        """
        Return car(s) to shop.
        """
        if self.rented_cars["type"] == None:
            print("[Fail] You have not rented any car!")
            return
        self.print_rental_info()

        # while (True):
        #     is_continue_input = input("Would you like to return these car(s)? yes or no \n")
        #     if (is_continue_input == "yes"):
        #         break
        #     elif (is_continue_input == "no"):
        #         return
        #     else:
        #         print("[Error] invalid input!")

        to_return = copy.deepcopy(self.rented_cars)
        while (True):
            number = input("How many cars do you want to return? please input the number: ")
            try:
                number = int(number)
                if (0 < number < self.rented_cars["number"]):
                    self.rented_cars["number"] -= number
                    break
                elif number == self.rented_cars["number"]:
                    self.rented_cars = copy.deepcopy(self.basic_rental_info)
                    break
                else:
                    print("[Error] Please input the correct number that must be between 1 to {} (the total number)".
                          format(self.rented_cars["number"]))
                    continue
            except:
                print("[Error] Invalid input!")

        # self.rental_shop.issue_bill(self.rented_cars)
        to_return["number"] = number
        self.rental_shop.issue_bill(to_return)
        self.save()

    def save(self):
        """
        Save customer data in JSON format
        """
        with open(self.data_path, 'w') as dump_f:
            json.dump(self.rented_cars, dump_f)

    def print_rental_info(self):
        """
        Print the rental information of customer
        """
        print("\n[Your rental information]")
        format_1, format_2 = self.rented_cars["time"].split('/')
        print("Rental time:", format_1)
        print("Type:", self.rented_cars["type"])
        print("Number:", self.rented_cars["number"])
        print("Expected days:", self.rented_cars["days"])
        print("Actual days:", math.ceil((time.time() - float(format_2)) / 86400))