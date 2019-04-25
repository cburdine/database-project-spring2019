from src.model import client_model
from src.model import classes
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()

# this variable should contain all the current curriculum names in the database
#       - its first used in the function that adds new curriculums (make sure it doesn't already exist)
all_curriculums = client_model.ClientModel
# all_curriculums.get_curriculum_names() todo: don't know how this works


def enter_new_curriculum(curriculum_name, min_credit_hours, id_person_in_charge):
    """
    Function to do the first query in our project requisites.
    The idea behind this is to have the user enter these basic things in main and then ask the user for more information
    as we go on through the function.
    """
    # todo: would it make more sense to have min_credit_hours be calculated after we enter in all the necessary courses?
    # part 1: validate input for creating the new curriculum

    # first, use our client_model to check and see if we already have the curriculum the person wants to enter
    if curriculum_name in all_curriculums:
        return "curriculum with this name is already in the database"

    # make sure the perosn in charge of the curriculum exists
    if not client_model.ClientModel.get_person(id_person_in_charge):
        return "this person is not in the database"

    # if we pass part 1: then we can safely create the new curriculum for the db
    my_cursor.execute("""INSERT INTO Curriculum (name, min_credit_hours, id_in_charge) VALUES (%s, %s, %s)""",
                        (curriculum_name, min_credit_hours, id_person_in_charge))
    mydb.commit()

    # part 2: ask about curriculum topics

    # get topics from user
    ip = input("""Please enter a list of topic id's that this curriculum should cover""")
    ip = ip.split(', ')

    # verify that topics are contained within our database
    #   if they're not present, we have the user define what the topic is

    my_cursor.execute("""SELECT id FROM Topic""") # todo: doesn't seem natural to ask the user
                                                  #  for a topic id
    basic_topics = my_cursor.fetchall()

    for i in ip:
        # check to see that it is in our Topic table
        if i not in basic_topics:
            print(f"We do not have the {i} topic in our database. Please create it now")
            create_topic(i)

        # get information to create the curriculum topic
        level = -1
        while level not in [1,2,3]:
            level = input("""Please enter the topic level (1,2, or 3""")
        subject_area = input("""Please write about the subject area""")
        time_unit = -1
        while time_unit < 0:
            time_unit = input("""Please enter the number of units this topic should cover""")

        # insert the curriculum topic into the db
        my_cursor.execute("""INSERT INTO CurriculumTopics (curriculum_name, topic_id, level, subject_area, time_unit) VALUES (%s, %s, %s, %s, %s)""",
                          (curriculum_name, i, level, subject_area, time_unit))
        mydb.commit()

    # part 3: get courses associated with this curriculum
    courses = input("""What are the names of the courses associated with this curriculum?""")
    courses = courses.split(', ')

    for i in courses:
        # make sure course exists in db
        my_cursor.execute("""SELECT COUNT(*) FROM Course WHERE name = %s""", (i,))
        ct = my_cursor.fetchone()
        ct = ct[0]
        if ct == 0:
            print("""This course does not exist. Please create it now""")
            create_course(i)

        # check to see if course is required
        req = 'j'
        while req != 'y' and req != 'n':
            req = input("""If this course is required, type 'r' """)

        if req == 'y':
            req = True
        else:
            req = False

        # add information to CurriculumListings
        my_cursor.execute("""INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",
                          (curriculum_name, i, req))
        mydb.commit()

    # part 4: ??

    return "not done yet"


def create_topic(topic_id):
    """
    Function to create a topic for the Topic table if it does not already exist
    """

    ip = input("""Please enter a name for this topic""")

    my_cursor.execute("""INSERT INTO Topic (id, name) VALUES (%s, %s)""",
                      (topic_id, ip))
    mydb.commit()

    return "nyc"


def create_course(course_name):
    """Function to create course"""

    subject_code = input("""What is the subject code for this course?""")
    credit_hours = 0
    while credit_hours <= 0:
        credit_hours = input("""Please enter the number of credit hours for this course""")
    des = input("""Please write a description for the course""")

    my_cursor.execute("""INSERT INTO Course (name, subject_code, credit_hours, description) VALUES (%s, %s, %s, %s)""",
                      (course_name, subject_code, credit_hours, des))
    mydb.commit()

    return "nyc"