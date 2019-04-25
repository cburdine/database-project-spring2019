from src.model import client_model
from src.model import classes
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()


def edit_person(person_id):
    """Function to edit person"""

    # check to make sure it's there
    my_cursor.execute("""SELECT COUNT(*) FROM Person WHERE id = %s""",
                      (person_id))

    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 0:
        return "person does not exist"

    n = input("""Please enter the person's new name""")

    my_cursor.execute("""DELETE FROM Person WHERE id = %s AND curriculum_name = %s""", (person_id))
    mydb.commit()

    my_cursor.execute("""INSERT INTO Person (id, name) VALUES (%s, %s)""",
                      (person_id, n))
    mydb.commit()