from src.model import client_model
from src.model import classes
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()

# note: these mostly assume input is already valid


def enter_new_person(person_id, person_name):
    """Function to enter new person into the database"""
    # check to make sure it's not there
    my_cursor.execute("""SELECT COUNT(*) FROM Person WHERE id = %s""",
                      (person_id))

    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 1:
        return "Person already exists"

    my_cursor.execute("""INSERT INTO Person (id, name) VALUES (%s, %s)""", (person_id,person_name))
    mydb.commit()


def enter_new_topic(topic_id, topic_name):
    """Function to enter new topic into the database"""
    # check to make sure it's not there
    my_cursor.execute("""SELECT COUNT(*) FROM Person WHERE id = %s""",
                      (topic_id))

    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 1:
        return "Topic already exists"

    my_cursor.execute("""INSERT INTO Person (id, name) VALUES (%s, %s)""", (topic_id, topic_name))
    mydb.commit()


def enter_new_goal(goal_id, curriculum_name, description):
    """Function to enter new goal into database"""
    # check to make sure curriculum is there
    my_cursor.execute("""SELECT COUNT(*) FROM Curriculum WHERE name = %s""",
                      (curriculum_name))
    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 0:
        return "Curriculum DNE"

    my_cursor.execute("""SELECT COUNT(*) FROM Goal WHERE id = %s AND curriculum_name = %s""",
                      (goal_id, curriculum_name))
    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 1:
        return "Goal DNE"

    my_cursor.execute("""INSERT INTO Person (id, name) VALUES (%s, %s)""", (goal_id, curriculum_name, description))
    mydb.commit()


def enter_new_course(course_name, subject_code, credit_hours, description):
    """Function to enter new course into db"""
    # check to make sure it's not there
    my_cursor.execute("""SELECT COUNT(*) FROM Course WHERE name = %s""",
                      (course_name))
    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 1:
        return "course already exists"

    my_cursor.execute("""INSERT INTO Course (name, subject_code, credit_hours, description) VALUES (%s, %s, %s, %s)""", (course_name, subject_code, credit_hours, description))
    mydb.commit()


def enter_new_section(course_name, semester, unit_id, num_students, comment1, comment2):
    """Function to create new section"""
    # check to make sure it's not there
    my_cursor.execute("""SELECT COUNT(*) FROM Section WHERE course_name = %s AND semester = %s AND unit_id = %s""",
                      (course_name, semester, unit_id))
    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 1:
        return "section already exists"

    my_cursor.execute("""INSERT INTO Section (course_name, semester, unit_id, num_students, comment1, comment2) VALUES (%s, %s, %s, %s, %s, %s)""",
                      (course_name, semester, unit_id, num_students, comment1, comment2))
    mydb.commit()