import mysql.connector
import logging

from src.model.classes import Curriculum, Course, Topic, Person, CurriculumTopic

import threading
from kivy.clock import Clock

class DBAdapter:

    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def init_connection(self, hostname, username, password):
        # Establish connection with credentials:
        db_connection = None
        db_cursor = None

        try:
            self.db_connection = mysql.connector.connect(
                host=hostname,
                user=username,
                password=password
            )
            self.db_cursor = self.db_connection.cursor(buffered=True)
            return True
        except:
            logging.error("DBAdapter: " + "Cannot connect to host- " + hostname)
            return False

    def try_use_db(self, db_name):
        try:
            self.db_cursor.execute("USE %s" % db_name)
            self.db_connection.commit()
            return True
        except:
            return False

    def execute_source(self, src_path, max_statements= None,value_progress_callback=None):
        logging.info("DBAdapter: " + "Opening source at " + src_path)

        try:
            sql_file = open(src_path, 'rt')
            queries = sql_file.read()

        except:
            logging.error("DBAdapter: " + "Cannot find source file at " + src_path)
            return False

        #try:
        prog = 0
        for statement in queries.split(';'):
            if len(statement.strip()) > 0:
                self.db_cursor.execute(statement.strip() + ';')
                self.db_connection.commit()
                prog += 1
                if max_statements and value_progress_callback != None:
                    value_progress_callback(prog/max_statements)

        logging.info("DBAdapter: " + "Successfully executed source at " + src_path)
        """
        except:
            logging.error("DBAdapter: " + "Failed to execute source at " + src_path)
            return False
        """
        return True

    def get_person(self, id):
        PERSON = """SELECT name FROM Person
                    WHERE id = %s"""

        ret = None
        try:
            self.db_cursor.execute(PERSON, id)
            self.db_connection.commit()
            p_attribs = self.db_cursor.fetchall()
            ret = Person()
            ret.name = p_attribs[0][0]
            ret.id = id

        except:
            logging.warning("DBAdapter: Error- cannot retrieve person: " + str(id))


        return ret

    def get_curricula_names(self):
        CURRICULA_NAMES = """SELECT name FROM Curriculum"""
        return_list = []

        try:
            self.db_cursor.execute(CURRICULA_NAMES)
            self.db_connection.commit()
            tups = self.db_cursor.fetchall()
            for t in tups:
                return_list.append(t[0])
        except:
           logging.warning("DBAdapter: Error- cannot retrieve Curricula names.")

        return return_list

    def get_curriculum(self, name):
        CURRICULUM = """SELECT * FROM Curriculum WHERE name = %s"""
        TOPICS = """SELECT * FROM CurriculumTopics WHERE curriculum_name = %s"""
        COURSES = """SELECT course_name FROM CurriculumListings WHERE curriculum_name = %s"""

        cur = None
        try:
            self.db_cursor.execute(CURRICULUM, name)
            self.db_connection.commit()
            attribs = self.db_cursor.fetchall()
            self.db_cursor.execute(TOPICS, name)
            self.db_connection.commit()
            topics = self.db_cursor.fetchall()
            self.db_cursor.execute(COURSES, name)
            self.db_connection.commit()
            courses = self.db_cursor.fetchall()
        except:
            logging.warning("DBAdapter: Error- cannot retrieve Curriculum " + str(name))
            return None

        cur.name = attribs[0][0]
        cur.min_credit_hours = attribs[0][1]
        cur.id_in_charge = attribs[0][2]

        for t in topics:
            ct = CurriculumTopic()
            ct.curriculum_name = t[0]
            ct.topic_id = t[1]
            ct.level = t[2]
            ct.subject_area = t[3]
            ct.time_unit = t[3]
            cur.course_topics.append(ct)

        for c in courses:
            if (c[2]):  # if required course
                cur.req_course_names.append(c[1])
            else:
                cur.opt_course_names.append(c[2])
        return cur

    def validate_new_curriculum_topics(self, curriculum_topics):
        """Function to determine if list of topics is
        in the general topics table.

        Note: this function assumes the curriculum already exists
        """

        for cur in curriculum_topics:
            # check to make sure its in the general topics table
            self.db_cursor.execute("""SELECT COUNT(*) FROM Topic WHERE name = %s""", (cur,))
            ct = self.db_cursor.fetchone()
            ct = ct[0]
            if ct == 0:
                print("topic does not exist, we must create new one or cancel") # todo

        return True

    def validate_new_curriculum_courses(self, curriculum_courses):
        """Function to determine if the list of courses is
        in the general courses table

        Note: this function assumes the curriculum already exists
        """

        for cur in curriculum_courses:
            # check to make sure its in the general courses table
            self.db_cursor.execute("""SELECT COUNT(*) FROM Course WHERE name = %s""", (cur,))
            ct = self.db_cursor.fetchone()
            ct = ct[0]
            if ct == 0:
                print("course does not exist, we must create new one or cancel")  # todo

        return True

    def validate_new_person(self, person_id):
        """Funtion to determine if a person with the same id as a new person
        already exists in the database"""

        self.db_cursor.execute("""SELECT COUNT(*) FROM Person WHERE id == %s""", (person_id,))
        ct = self.db_cursor.fetchone()
        ct = ct[0]
        if ct == 0:
            return False
        return True

    def validate_new_topic(self, topic_id):
        """Function to determine if a topic with the same id as the new topic
        already exists in the database"""

        self.db_cursor.execute("""SELECT COUNT(*) FROM Topic WHERE id == %s""", (topic_id,))
        ct = self.db_cursor.fetchone()
        ct = ct[0]
        if ct == 0:
            return False
        return True
