"""
This file contains classes for our database entities.
Notes: - classes are made based off of actual entities
       - classes are meant to help store class information retrieved from database
"""



"""
The idea behind this class is to store and retrieve information from the curriculum table

In this iteration, I took the liberty of making the class variables lists instead of just single variables.
This is so that when we store/retrieve information from this table in the database, we can store it ia single
object and not have to use multiple
"""
class Curriculum:

    def __init__(self):
        self.name = None
        self.min_credit_hours = None
        self.id_in_charge = None

    def __str__(self):
        """
        Overridden str function
        """
        print(f"name: {self.name}")
        print(f"min_credit_hours: {self.min_credit_hours}")
        print(f"id_in_charge: {self.id_in_charge}")

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
        self.name = None
        self.subject_code = None
        self.credit_hours = None
        self.description = None

    def __str__(self):
        """
        Overridden str function
        """
        print(f"name: {self.name}")
        print(f"min_credit_hours: {self.subject_code}")
        print(f"id_in_charge: {self.credit_hours}")
        print(f"id_in_charge: {self.description}")


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
