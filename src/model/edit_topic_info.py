from src.model import client_model
from src.model import classes
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()


def edit_topic(topic_id):
    """Function to edit topic"""

    # check to make sure it's there
    my_cursor.execute("""SELECT COUNT(*) FROM Topic WHERE id = %s""",
                      (topic_id))

    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 0:
        return "goal does not exist"

    des = input("""What would you like the new topic name to be?""")

    my_cursor.execute("""DELETE FROM Topic WHERE id = %s""", (topic_id))
    mydb.commit()

    my_cursor.execute("""INSERT INTO Topic (id, name) VALUES (%s, %s)""",
                      (topic_id, des))
    mydb.commit()