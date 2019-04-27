from src.model import client_model
from src.model import classes
import mysql.connector


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()


def edit_course(course_name):
    """Function to edit course information"""

    # check to see if course exists
    my_cursor.execute("""SELECT COUNT(*) FROM Course WHERE name = %s""", (course_name,))
    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 0:
        return """This course does not exist."""

    # does user want to delete or modify this course entry
    delete_or_edit = 'ojqwd'
    while delete_or_edit != 'd' and delete_or_edit != 'e':
        delete_or_edit = input("""To delete this course, press 'd'. To edit, press 'e'. """)

    if delete_or_edit == 'e':
        sc = input("""what is the new subject code?""")
        ch = input("""what are the new credit hours?""")
        desc = input("""what is the new description?""")

        my_cursor.execute("""DELETE FROM Course WHERE name = %s""", (course_name,))
        mydb.commit()
        my_cursor.execute(
            """INSERT INTO Course (name, subject_code, credit_hours, description) VALUES (%s, %s, %s, %s)""",
            (course_name, sc, ch, desc))
        mydb.commit()
    else:
        my_cursor.execute("""DELETE FROM Course WHERE name = %s""", (course_name,))
        mydb.commit()
