import mysql.connector
import logging

from src.model.classes import Curriculum, Course, Topic, Person, CurriculumTopic, Section, Goal

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
        """Function to retrieve a person from the database to store in client model"""
        PERSON = """SELECT name FROM Person
                    WHERE id = %s"""

        ret = None
        try:
            self.db_cursor.execute("""SELECT name, id FROM Person WHERE id = %s""", (id,))
            self.db_cursor.execute(PERSON, (id,))
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
        COURSES = """SELECT * FROM CurriculumListings WHERE curriculum_name = %s"""

        #try:
        self.db_cursor.execute(CURRICULUM, (name,))
        self.db_connection.commit()
        attribs = self.db_cursor.fetchall()
        self.db_cursor.execute(TOPICS, (name,))
        self.db_connection.commit()
        topics = self.db_cursor.fetchall()
        self.db_cursor.execute(COURSES, (name,))
        self.db_connection.commit()
        courses = self.db_cursor.fetchall()
        #except:
        #    logging.warning("DBAdapter: Error- cannot retrieve Curriculum " + str(name))
        #    return None
        cur = Curriculum()
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
            cur.cur_topics.append(ct)

        for c in courses:
            if (c[2]):  # if required course
                cur.req_course_names.append(c[1])
            else:
                cur.opt_course_names.append(c[1])
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

    def add_new_topic_to_db(self, topic_obj):
        """Function to add a brand new topic to the database"""
        # todo: don't need this anymore
        self.db_cursor.execute("""INSERT INTO Topic (id, name) VALUES (%s, %s)""", (topic_obj.id, topic_obj.name))
        self.db_connection.commit()

    def get_topic(self, id):
        """Function to retrieve a topic from the database to store in client model"""
        TOPIC = """SELECT COUNT(*) FROM Topic WHERE id = %s"""

        ret = None
        try:
            self.db_cursor.execute("""SELECT name, id FROM Topic WHERE id = %s""", (id,))
            t = self.db_cursor.fetchall()
            ret = Topic()
            ret.name = t[0][0]
            ret.id = id

        except:
            logging.warning("DBAdapter: Error- cannot retrieve person: " + str(id))

        return ret

    def set_topic(self, new_topic):
        """Function to add a new topic to the database"""
        self.db_cursor.execute("""INSERT INTO Topic (id, name) VALUES (%s, %s)""", (new_topic.id, new_topic.name))
        self.db_connection.commit()

    def set_person(self, new_person):
        """Function to add a new person to the database"""
        self.db_cursor.execute("""INSERT INTO Person (id, name) VALUES (%s, %s)""", (new_person.id, new_person.name))
        self.db_connection.commit()

    def get_course(self, name):
        """Function to retrieve course from the database"""
        COURSE = """SELECT COUNT(*) FROM Topic WHERE id = %s"""

        ret = None
        try:
            self.db_cursor.execute("""SELECT subject_code, credit_hours, description FROM Course WHERE name = %s""", (name,))
            c = self.db_cursor.fetchall()
            ret = Course()
            ret.subject_code = c[0][0]
            ret.credit_hours = c[0][1]
            ret.description = c[0][2]
            ret.name = name

        except:
            logging.warning("DBAdapter: Error- cannot retrieve person: " + str(id))

        return ret

    def set_course(self, new_course):
        """Fucntion to set the course in the db"""
        self.db_cursor.execute("""INSERT INTO Course (name, subject_code, credit_hours, description) VALUES (%s, %s, %s, %s)""", (new_course.name, new_course.subject_code, new_course.credit_hours, new_course.description))
        self.db_connection.commit()

    def get_section(self, new_section):
        """Function to retrieve section from the db"""

        SECTION = """SELECT COUNT(*) FROM Section WHERE id = %s"""

        ret = None
        try:
            self.db_cursor.execute("""SELECT num_students, comment1, comment2 FROM Section WHERE course_name = %s AND semester = %s AND unit_id  = %s""",
                                   (new_section.course_name, new_section.semester, new_section.unit_id))
            c = self.db_cursor.fetchall()
            ret = Section()
            if c:
                ret.num_students = c[0][0]
                ret.comment1 = c[0][1]
                ret.comment2 = c[0][2]
                ret.course_name = new_section.course_name
                ret.semester = new_section.semester
                ret.unit_id = new_section.unit_id
            else:
                ret.num_students = None
                ret.comment1 = None
                ret.comment2 = None
                ret.course_name = None
                ret.semester = None
                ret.unit_id = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve person: " + str(id))

        return ret

    def set_section(self, new_section):
        """Function for adding a section to the db"""
        self.db_cursor.execute(
            """INSERT INTO Section (course_name, semester, unit_id, num_students, comment1, comment2) VALUES (%s, %s, %s, %s, %s, %s)""",
            (new_section.course_name, new_section.semester, new_section.unit_id, new_section.num_students, new_section.comment1, new_section.comment2))
        self.db_connection.commit()

    def set_curriculum(self, new_curriculum):
        """Function for adding curriculum to the db"""
        # addnig into curriculum table
        self.db_cursor.execute("""INSERT INTO Curriculum (name, min_credit_hours, id_in_charge) VALUES (%s, %s, %s)""",
                               (new_curriculum.name, new_curriculum.min_credit_hours, new_curriculum.id_in_charge))
        self.db_connection.commit()
        # adding into curriculum listings table
        # todo make sure these two have no errors
        self.db_cursor.execute("""INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",
                               (new_curriculum.name, new_curriculum.req_course_names, 1))
        self.db_connection.commit()
        self.db_cursor.execute(
            """INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",
            (new_curriculum.name, new_curriculum.opt_course_names, 0))
        self.db_connection.commit()
        # adding into curriculum topics table
        self.db_cursor.execute(
            """INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",
            (new_curriculum.name, new_curriculum.opt_course_names, 0))
        self.db_connection.commit()


    def get_goal(self, new_goal):
        """Function to retrieve goal from the db"""

        GOAL = """SELECT COUNT(*) FROM Section WHERE id = %s"""

        ret = None
        try:
            self.db_cursor.execute(
                """SELECT description FROM Goal WHERE id = %s AND curriculum_name = %s""",
                (new_goal.id, new_goal.curriculum_name,))
            c = self.db_cursor.fetchall()
            ret = Goal()
            if c:
                ret.description = c[0][0]
                ret.id = new_goal.id
                ret.curriculum_name = new_goal.curriculum_name
            else:
                ret.description = None
                ret.id = None
                ret.curriculum_name = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve goal: " + str(id))

        return ret


    def set_goal(self, new_goal):
        """Function to write goal to the db"""
        self.db_cursor.execute(
            """INSERT INTO Goal (id, curriculum_name, description) VALUES (%s, %s, %s)""",
            (new_goal.id, new_goal.curriculum_name, new_goal.description))
        self.db_connection.commit()

    def set_course_goal(self, goal_id, course_name):
        """Function to write course goal to the db"""
        self.db_cursor.execute(
            """INSERT INTO CourseGoals (course_name, goal_id) VALUES (%s, %s)""",
            (course_name, goal_id))
        self.db_connection.commit()

    def set_course_topic(self, topic_id,course_name):
        """Function to write course topic to the db"""
        self.db_cursor.execute(
            """INSERT INTO CourseTopics (course_name, goal_id) VALUES (%s, %s)""",
            (course_name, topic_id))
        self.db_connection.commit()

    def set_curriculum_course(self, curriculum_name, course_name, required):
        """Function to write curriculum course to the db"""
        self.db_cursor.execute(
            """INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",
            (curriculum_name,course_name, required))
        self.db_connection.commit()

    def set_curriculum_topic(self, curriculum_name, topic_id, level, subject_area, time_unit):
        """Function to write curriculum topic to the db"""
        self.db_cursor.execute(
            """INSERT INTO CurriculumTopics (curriculum_name, topic_id, level, subject_area, time_unit) VALUES (%s, %s, %s, %s, %s)""",
            (curriculum_name, topic_id, level, subject_area, time_unit))
        self.db_connection.commit()