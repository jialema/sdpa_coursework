"""
@author: Jiale Ma
CustomerVIP class is defined in this file.
"""
import math
import time
from customer import Customer

class CustomerVIP(Customer):
    basic_rental_info = {"type": None,
                         "number": None,
                         "days": None,
                         "time": None,
                         "vip": True}
    # def __init__(self, name = None, data_path = None):
    #     super(CustomerVIP, self).__init__(name, data_path)
    #     self.vip = True

    # def inquire(self):
    #     self.rental_shop.display_inventory_pricing(self.vip)

    # def return_car(self):
    #     print("\n[Your rental information]")
    #     if self.rented_cars == {}:
    #         print("[Fail] You have not rented any car!")
    #         return
    #     for rental_time in self.rented_cars.keys():
    #         format_1, format_2 = rental_time.split('/')
    #         print("rental time:", format_1)
    #         print("type:", list(self.rented_cars[rental_time].items())[0][0])
    #         print("number:", list(self.rented_cars[rental_time].items())[0][1])
    #         print("days:", math.ceil((time.time() - float(format_2)) / 86400))
    #
    #     while (True):
    #         is_continue_input = input("Would you like to return these car(s)? yes or no \n")
    #         if (is_continue_input == "yes"):
    #             break
    #         elif (is_continue_input == "no"):
    #             return
    #         else:
    #             print("[Error] invalid input!")
    #
    #     self.rental_shop.issue_bill(self.rented_cars, self.vip)
    #     self.rented_cars = {}
    #     self.save()



