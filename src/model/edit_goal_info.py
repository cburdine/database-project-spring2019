from src.model import client_model
from src.model import classes
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()


def edit_goal(goal_id):
    """Function to edit Goal"""

    curriculum_name = input("""To what curriculum does this goal belong to?""")

    # check to make sure it's there
    my_cursor.execute("""SELECT COUNT(*) FROM Goal WHERE id = %s AND curriculum_name = %s""", (goal_id, curriculum_name))

    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 0:
        return "goal does not exist"

    des = input("""What would you like the new description to be?""")

    my_cursor.execute("""DELETE FROM Goal WHERE id = %s AND curriculum_name = %s""", (goal_id,curriculum_name))
    mydb.commit()

    my_cursor.execute("""INSERT INTO Goal (id, curriculum_name, description) VALUES (%s, %s, %s)""",
                      (goal_id, curriculum_name, des))
    mydb.commit()