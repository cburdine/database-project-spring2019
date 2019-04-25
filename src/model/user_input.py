from src.model import client_model
from src.model import classes
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()

"""
The purpose of this file is to give a general idea of what the UI should be like when entering information.
Users will have a choice of...
    1. entering new information
    2. editing existing information
...In this file, we will validate and test user input before sending it to our functions"""

# todo: write this file
