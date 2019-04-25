from src.model import client_model
from src.model import classes
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="jabtexas23",
    database="Curricula")

my_cursor = mydb.cursor()


def edit_curriculum(curriculum_name):
    """Function to edit an existing curriculum"""

    # check to make sure it's there
    my_cursor.execute("""SELECT COUNT(*) FROM Curriculum WHERE name = %s""", (curriculum_name,))

    ct = my_cursor.fetchone()
    ct = ct[0]
    if ct == 0:
        return "curriculum does not exist"

    # ask what portion of the curriculum they would like to edit
    edit = input("""What part of the curriculum would you like to edit. Options include...
                    1. name of curriculum
                    2. number of minimum credit hours
                    3. person in charge of curriculum
                    4. topics included in the curriculum
                    5. courses associated with the curriculum""")
    while edit not in [1,2,3,4,5]:
        edit = input("""Please enter your answer as 1,2,3,4, or 5""")

    if edit == 1:
        new_name = input("""What would you like the new name to be?""")
        my_cursor.execute("""INSERT INTO Curriculum (name) VALUES (%s)""", (new_name,))
        mydb.commit()
    elif edit == 2:
        new_hours = 0
        while new_hours <= 0:
            new_hours = input("""What would you like the new hours to be?""")
        my_cursor.execute("""INSERT INTO Curriculum (min_credit_hours) VALUES (%s)""", (new_hours,))
        mydb.commit()
    elif edit == 3:
        new_id = input("""What would you like the new person in charge to be?""")
        my_cursor.execute("""SELECT COUNT(*) FROM PERSON WHERE id = %s""", (new_id))
        ct = my_cursor.fetchone()
        ct = ct[0]
        if ct == 0:
            return "This person is not in the database"
        my_cursor.execute("""INSERT INTO Curriculum (id_in_charge) VALUES (%s)""", (new_id,))
        mydb.commit()
    elif edit == 4:
        # do they want to add or remove or edit a curriculum topic?
        add_or_remove_or_edit = "nei"
        while add_or_remove_or_edit not in ['add', 'remove', 'edit']:
            add_or_remove_or_edit = input("""To add a curriculum topic, type 'add'. To remove a curriculum topic, write 'remove'. 
            To edit a curriculum topic, type 'edit'.""")

        if add_or_remove_or_edit == 'add':
            print('nyc')

            # make sure topic does not already exist in db
            topic_id = input("""What is the new topic id you would like to add to the curriculum""")
            my_cursor.execute("""SELECT COUNT(*) FROM CurriculumTopics WHERE curriculum_name = %s AND topic_id = %s""", (curriculum_name, topic_id))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 1:
                return "curriculum topic already exists"

            # get information to create the curriculum topic
            level = -1
            while level not in [1, 2, 3]:
                level = input("""Please enter the topic level (1,2, or 3""")
            subject_area = input("""Please write about the subject area""")
            time_unit = -1
            while time_unit < 0:
                time_unit = input("""Please enter the number of units this topic should cover""")

            # insert the curriculum topic into the db
            my_cursor.execute(
                """INSERT INTO CurriculumTopics (curriculum_name, topic_id, level, subject_area, time_unit) VALUES (%s, %s, %s, %s, %s)""",
                (curriculum_name, topic_id, level, subject_area, time_unit))
            mydb.commit()
        elif add_or_remove_or_edit == 'remove':

            # make sure it's in db
            topic_id = input("""What is the new topic id you would like to delete to the curriculum""")
            my_cursor.execute("""SELECT COUNT(*) FROM CurriculumTopics WHERE curriculum_name = %s AND topic_id = %s""",
                              (curriculum_name, topic_id))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 0:
                return "curriculum topic does not exist in db"

            # delete it from db
            my_cursor.execute("""DELETE FROM CurriculumTopics WHERE curriculum_name = %s AND topic_id = %s""",
                              (curriculum_name, topic_id))
            mydb.commit()
        else:
            # make sure topic does not already exist in db
            topic_id = input("""What is the new topic id you would like to add to the curriculum""")
            my_cursor.execute("""SELECT COUNT(*) FROM CurriculumTopics WHERE curriculum_name = %s AND topic_id = %s""",
                              (curriculum_name, topic_id))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 0:
                return "curriculum topic does not exist"

            # get information to create the curriculum topic
            level = -1
            while level not in [1, 2, 3]:
                level = input("""Please enter the topic level (1,2, or 3""")
            subject_area = input("""Please write about the subject area""")
            time_unit = -1
            while time_unit < 0:
                time_unit = input("""Please enter the number of units this topic should cover""")

            # delete it from db
            my_cursor.execute("""DELETE FROM CurriculumTopics WHERE curriculum_name = %s AND topic_id = %s""",
                              (curriculum_name, topic_id))
            mydb.commit()

            # insert the curriculum topic into the db
            my_cursor.execute(
                """INSERT INTO CurriculumTopics (curriculum_name, topic_id, level, subject_area, time_unit) VALUES (%s, %s, %s, %s, %s)""",
                (curriculum_name, topic_id, level, subject_area, time_unit))
            mydb.commit()
    elif edit == 5:
        # do they want to add or remove or edit a curriculum listing?
        add_or_remove_or_edit = "nei"
        while add_or_remove_or_edit not in ['add', 'remove', 'edit']:
            add_or_remove_or_edit = input("""To add a curriculum listing, type 'add'. To remove a curriculum topic, write 'remove'. 
                    To edit a curriculum topic, type 'edit'.""")

        if add_or_remove_or_edit == 'add':
            # check to see if it is in the Course table
            c = input("please enter the new course name associated with this curriculum")
            my_cursor.execute("""SELECT COUNT(*) FROM Course WHERE name = %s""", (c,))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 0:
                return """This course does not exist."""

            # check to see if it is already in curriculum listings
            my_cursor.execute(
                """SELECT COUNT(*) FROM CurriculumListings WHERE course_name = %s AND curriculum_name = %s""",
                (c, curriculum_name))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 1:
                return """This is already in curriculum listings."""

            req = 'j'
            while req != 'y' and req != 'n':
                req = input("""If this course is required, type 'r' """)

            if req == 'y':
                req = True
            else:
                req = False

            my_cursor.execute(
                """INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",
                (curriculum_name, c, req))
            mydb.commit()
        elif add_or_remove_or_edit == 'remove':
            c = input("please enter the new course name associated with this curriculum")
            my_cursor.execute("""SELECT COUNT(*) FROM Course WHERE name = %s""", (c,))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 0:
                return """This course does not exist."""

            # check to see if it is in curriculum listings
            my_cursor.execute(
                """SELECT COUNT(*) FROM CurriculumListings WHERE course_name = %s AND curriculum_name = %s""",
                (c, curriculum_name))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 1:
                # delete it from db
                my_cursor.execute("""DELETE FROM CurriculumListings WHERE curriculum_name = %s AND course_name = %s""",
                                  (curriculum_name, c))
                mydb.commit()
            else:
                return "already not in database"
        elif add_or_remove_or_edit == 'edit':
            # check to see if it is in the Course table
            c = input("please enter the new course name associated with this curriculum")
            my_cursor.execute("""SELECT COUNT(*) FROM Course WHERE name = %s""", (c,))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 0:
                return """This course does not exist."""

            # check to see if it is already in curriculum listings
            my_cursor.execute(
                """SELECT COUNT(*) FROM CurriculumListings WHERE course_name = %s AND curriculum_name = %s""",
                (c, curriculum_name))
            ct = my_cursor.fetchone()
            ct = ct[0]
            if ct == 1:
                req = 'j'
                while req != 'y' and req != 'n':
                    req = input("""If this course is required, type 'r' """)

                if req == 'y':
                    req = True
                else:
                    req = False

                my_cursor.execute("""DELETE FROM CurriculumListings WHERE curriculum_name = %s AND course_name = %s""",
                                  (curriculum_name, c))
                mydb.commit()

                my_cursor.execute(
                    """INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",
                    (curriculum_name, c, req))
                mydb.commit()
            else:
                return "this is not in the curriculum listings"

