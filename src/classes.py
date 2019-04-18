"""
This file contains classes for our database entities.
Notes: - classes are made based off of actual entities
       - classes are meant to help store class information retrieved from database
"""

import mysql.connector

mydb = mysql.connector.connect


"""
The idea behind this class is to store and retrieve information from the curriculum table

In this iteration, I took the liberty of making the class variables lists instead of just single variables.
This is so that when we store/retrieve information from this table in the database, we can store it ia single
object and not have to use multiple
"""
class Curriculum:

    def __init__(self):
        self.name = []
        self.min_credit_hours = []
        self.id_in_charge = []

    def debug_print(self):
        """
        Function used for debugging to see what this object
        contains
        """
        print(f"name: {self.name}")
        print(f"min_credit_hours: {self.min_credit_hours}")
        print(f"id_in_charge: {self.id_in_charge}")

    def set_name(self, n):
        self.name.append(n)

    def set_min_credit_hours(self, mch):
        self.min_credit_hours.append(mch)

    def set_id_in_charge(self, idc):
        self.id_in_charge.append(idc)

    def send_to_db(self):
        """
        Function to send current info stored in object to the database
        Should be useful for query where we need to write curriculum information to the db
        """

    def retrieve_from_db(self):
        """
        function to retrieve information from the db and return it to a list
        :returns: list
        """

"""
Class to store and retrieve information from the course table
"""
class Course:
    def __init__(self):
        self.name = []
        self.subject_code = []
        self.credit_hours = []
        self.description = []

    def debug_print(self):
        """
        Function used for debugging to see what this object
        contains
        """
        print(f"name: {self.name}")
        print(f"min_credit_hours: {self.subject_code}")
        print(f"id_in_charge: {self.credit_hours}")
        print(f"id_in_charge: {self.description}")

    def set_name(self, n):
        self.nam.append(n)

    def set_min_credit_hours(self, mch):
        self.subject_code = mch

    def set_id_in_charge(self, idc):
        self.credit_hours = idc

    def set_id_in_charge(self, idc):
        self.description = idc

    def send_to_db(self):
        """
        Function to send current info stored in object to the database
        Should be useful for query where we need to write curriculum information to the db
        """

    def retrieve_from_db(self):
        """
        function to retrieve information from the db and return it to a list
        :returns: list
        """
