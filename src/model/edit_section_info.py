from src.model import client_model
from src.model import classes
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()


def edit_section(course_name, semester, unit_id):
    """Function to edit section"""

    # check to make sure it's there
    my_cursor.execute("""SELECT COUNT(*) FROM Seciton WHERE course_name = %s AND semester = %s AND unit_id = %s""",
                      (course_name, semester, unit_id))

    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 0:
        return "goal does not exist"

    num = input("how many students are in this section?")
    com1 = input("add a comment?")
    com2 = input("how about another?")

    my_cursor.execute("""DELETE FROM Section WHERE course_name = %s AND semester = %s AND unit_id = %s""", (course_name, semester, unit_id))
    mydb.commit()

    my_cursor.execute("""INSERT INTO Section (course_name, semester, unit_id) VALUES (%s, %s, %s)""",
                      (course_name, semester, unit_id))
    mydb.commit()