"""
@author: Jiale Ma
This is a unit test script to test the code of Car Rental System program.
Input python test carRental_test.py in the terminal to start the test.
"""

import os
import json
import unittest
from customer import Customer
from shop import Shop

CUSTOMERS_DIRECTORY = "test_data/customers"  # the path of storing data about car rental information
INVENTORY_DATA_PATH = "test_data/inventory.json"

class Test(unittest.TestCase):

    def setUp(self) -> None:
        """
        Before testing the method of the class, create the instance of the class.
        """
        if not os.path.exists(CUSTOMERS_DIRECTORY):
            os.makedirs(CUSTOMERS_DIRECTORY)

        self.data_path = CUSTOMERS_DIRECTORY + "/test.json"
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as load_f:
                rented_cars = json.load(load_f)
            self.user = Customer(self.data_path, rented_cars)
        else:
            self.user = Customer(self.data_path)

        rental_shop = Shop(INVENTORY_DATA_PATH)
        self.user.rental_shop = rental_shop

    def tearDown(self) -> None:
        pass

    def test_rent_car(self):
        """
        Test the Customer.rent_car(). Make sure the code can handle possible input errors, like null values,
        negative values, non-integer inputs, or other invalid values.
        """
        self.assertEqual(self.user.rent_car(), None, "The test of the function of rent_car fail!")

    def test_return_car(self):
        """
        Test the Customer.return_car(). Make sure the code can handle possible input errors, like null values,
        negative values, non-integer inputs, or other invalid values.
        """

        self.assertEqual(self.user.return_car(), None, "The test of the function of return_car fail!")

        # After test, remove all related files or directories.
        os.remove(CUSTOMERS_DIRECTORY + "/test.json")
        os.remove(INVENTORY_DATA_PATH)
        os.removedirs(CUSTOMERS_DIRECTORY)

if __name__ == '__main__':
    unittest.main()



