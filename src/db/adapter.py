import mysql.connector
import logging

from src.model.classes import Curriculum, Course, Topic, Person, CurriculumTopic, Section, Goal, SectionGrades, SectionGoalGrades

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
            return None

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

    def get_course_names(self):
        COURSE_NAMES = """SELECT name FROM Course"""
        return_list = []

        try:
            self.db_cursor.execute(COURSE_NAMES)
            self.db_connection.commit()
            tups = self.db_cursor.fetchall()
            for t in tups:
                return_list.append(t[0])
        except:
           logging.warning("DBAdapter: Error- cannot retrieve Course names.")

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
        if attribs:
            cur.name = attribs[0][0]
            cur.min_credit_hours = attribs[0][1]
            cur.id_in_charge = attribs[0][2]
        else:
            return None

        for t in topics:
            ct = CurriculumTopic()
            ct.curriculum_name = t[0]
            ct.topic_id = t[1]
            ct.level = t[2]
            ct.subject_area = t[3]
            ct.time_unit = t[4]
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
            logging.warning("DBAdapter: Error- cannot retrieve topic with id " + str(id))
            return None

        return ret

    def set_topic(self, new_topic, updating=False):
        """Function to add a new topic to the database"""

        TOPIC_QUERY = """UPDATE Topic SET name = %s WHERE id = %s""" if updating \
            else """INSERT INTO Topic (name, id) VALUES (%s, %s)"""



        self.db_cursor.execute(TOPIC_QUERY, (new_topic.name, new_topic.id))
        self.db_connection.commit()

    def set_person(self, new_person, updating=False):
        """Function to add a new person to the database"""
        PERSON_QUERY = """UPDATE Person SET name = %s WHERE id = %s""" if updating \
            else """INSERT INTO Person (name, id) VALUES (%s, %s)"""

        self.db_cursor.execute(PERSON_QUERY, (new_person.name, new_person.id))
        self.db_connection.commit()

    def get_course(self, name):
        """Function to retrieve course from the database"""
        GET_TOPIC_IDS = """SELECT topic_id FROM CourseTopics WHERE course_name = %s"""
        GET_GOAL_IDS = """SELECT goal_id FROM CourseGoals WHERE course_name = %s"""

        ret = None

        try:
            self.db_cursor.execute("""SELECT subject_code, credit_hours, description FROM Course WHERE name = %s""", (name,))
            c = self.db_cursor.fetchall()
            ret = Course()
            ret.subject_code = c[0][0]
            ret.credit_hours = c[0][1]
            ret.description = c[0][2]
            ret.name = name
            ret.goals = []
            ret.topics = []


            self.db_cursor.execute(GET_TOPIC_IDS, (name,))
            t_ids = self.db_cursor.fetchall()
            for id in t_ids:
                ret.topics.append(id[0])

            self.db_cursor.execute(GET_GOAL_IDS, (name,))
            g_ids = self.db_cursor.fetchall()
            for id in g_ids:
                ret.goals.append(id[0])

        except:
            logging.warning("DBAdapter: Error- cannot retrieve course: " + str(name))
            return None

        return ret

    def set_course(self, new_course, updating=False):
        """Fucntion to set the course in the db"""
        COURSE_QUERY = """UPDATE Course SET subject_code = %s, credit_hours = %s, description = %s WHERE name = %s""" if updating \
            else """INSERT INTO Course (subject_code, credit_hours, description, name) VALUES (%s, %s, %s, %s)"""

        self.db_cursor.execute(COURSE_QUERY, (new_course.subject_code, new_course.credit_hours, new_course.description, new_course.name))
        self.db_connection.commit()

        # Add course topics and course goals:
        for ct_id in new_course.topics:
            self.set_course_topic(ct_id, new_course.name)
        for cg_id in new_course.goals:
            self.set_course_goal(cg_id, new_course.name)

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
                ret = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve section: " + str(id))

        return ret

    def set_section(self, new_section, updating=False):
        """Function for adding a section to the db"""
        SECTION_QUERY = """UPDATE Section SET num_students = %s, comment1 = %s, comment2 = %s WHERE course_name = %s, semester = %s, section_id = %s, year = %s""" if updating \
            else """INSERT INTO Section (course_name, semester, section_id, num_students, comment1, comment2, year) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        if updating:
            self.db_cursor.execute(SECTION_QUERY,
                (new_section.num_students, new_section.comment1, new_section.comment2, new_section.course_name, new_section.semester, new_section.section_id, new_section.year))
        else:
            self.db_cursor.execute(SECTION_QUERY,
                                   (new_section.course_name, new_section.semester, new_section.section_id,
                                    new_section.num_students, new_section.comment1, new_section.comment2, new_section.year))
        self.db_connection.commit()

    def set_curriculum(self, new_curriculum, updating=False):
        """Function for adding curriculum to the db"""
        if not updating:
            #Add Curriculum to database:
            self.db_cursor.execute("""INSERT INTO Curriculum (name, min_credit_hours, id_in_charge) VALUES (%s, %s, %s)""",
                                   (new_curriculum.name, new_curriculum.min_credit_hours, new_curriculum.id_in_charge))
            self.db_connection.commit()

            #Add required courses:
            arg_list = list(map(lambda r: (new_curriculum.name, r, True), new_curriculum.req_course_names))
            self.db_cursor.executemany(
                """INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",arg_list)
            self.db_connection.commit()

            #Add optional courses:
            arg_list = list(map(lambda r: (new_curriculum.name, r, False), new_curriculum.opt_course_names))
            self.db_cursor.executemany(
                """INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)""",arg_list)
            self.db_connection.commit()

            #Add curriculum topics:
            arg_list = list(map(lambda ct: (new_curriculum.name, ct.topic_id, ct.level, ct.subject_area, ct.time_unit), new_curriculum.cur_topics))
            self.db_cursor.executemany(
                """INSERT INTO CurriculumTopics (curriculum_name, topic_id, level, subject_area, time_unit) VALUES (%s, %s, %s, %s, %s)""",arg_list)
            self.db_connection.commit()
        else:
            # Update Curriculum to database:
            self.db_cursor.execute(
                """UPDATE Curriculum SET min_credit_hours = %s, id_in_charge = %s WHERE name = %s""",
                (new_curriculum.min_credit_hours, new_curriculum.id_in_charge, new_curriculum.name))
            self.db_connection.commit()

            # update optional courses:
            arg_list = list(map(lambda r: (False, new_curriculum.name, r), new_curriculum.opt_course_names))
            self.db_cursor.executemany(
                """UPDATE CurriculumListings SET required = %s WHERE curriculum_name = %s AND course_name = %s""",
                arg_list)
            self.db_connection.commit()

            # update required courses:
            arg_list = list(map(lambda r: (True, new_curriculum.name, r), new_curriculum.req_course_names))
            self.db_cursor.executemany(
                """UPDATE CurriculumListings SET required = %s WHERE curriculum_name = %s AND course_name = %s""",
                arg_list)
            self.db_connection.commit()

            # update curriculum topics:
            arg_list = list(map(lambda ct: (ct.level, ct.subject_area, ct.time_unit, new_curriculum.name, ct.topic_id),
                                new_curriculum.cur_topics))
            self.db_cursor.executemany(
                """UPDATE CurriculumTopics SET level = %s, subject_area = %s, time_unit = %s WHERE curriculum_name = %s AND topic_id = %s""",
                arg_list)
            self.db_connection.commit()

    def fetch_goal_context_description(self, goalId):
        """Retrieves all descriptions of a Goal, potentially across
           the context of multiple curricula and returns a description"""
        GET_ALL_CONTEXTS = """SELECT curriculum_name, description FROM Goal WHERE id = %s """

        try:
            self.db_cursor.execute(GET_ALL_CONTEXTS,(goalId,))
            descriptions = self.db_cursor.fetchall()
            if len(descriptions) <= 0:
                return None

            ret_str = []
            ret_str.append(f"Goal #{goalId}\n")
            ret_str.append(f"From {descriptions[0][0]}: {descriptions[0][1]}")
            if len(descriptions) > 1:
                ret_str.append(" (and more)")
            return ''.join(ret_str)

        except:
            logging.warning("DBAdapter: Error- cannot retrieve goal contexts from id: " + str(goalId))
            return None

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
                ret = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve goal: " + str(new_goal.id))

        return ret


    def set_goal(self, new_goal, updating=False):
        """Function to write goal to the db"""
        GOAL_QUERY = """UPDATE Goal SET description = %s WHERE id = %s AND curriculum_name = %s""" if updating \
            else """INSERT INTO Goal (id, curriculum_name, description) VALUES (%s, %s, %s)"""

        if not updating:
            self.db_cursor.execute(
                GOAL_QUERY,
                (new_goal.id, new_goal.curriculum_name, new_goal.description))
        else:
            self.db_cursor.execute(
                GOAL_QUERY,
                (new_goal.description, new_goal.id, new_goal.curriculum_name))
        self.db_connection.commit()

    def set_course_goal(self, goal_id, course_name, updating=False):
        """Function to write course goal to the db"""
        self.db_cursor.execute(
            """INSERT INTO CourseGoals (course_name, goal_id) VALUES (%s, %s)""",
            (course_name, goal_id))
        self.db_connection.commit()

    def set_course_topic(self, topic_id,course_name):
        """Function to write course topic to the db"""
        self.db_cursor.execute(
            """INSERT INTO CourseTopics (course_name, topic_id) VALUES (%s, %s)""",
            (course_name, topic_id))
        self.db_connection.commit()

    def get_course_topic(self, topic_id, course_name):
        """Function to get a course topic from the db"""
        ret = None
        try:
            self.db_cursor.execute(
                """SELECT course_name, topic_id FROM CourseTopics WHERE course_name = %s AND topic_id = %s""",
                (course_name, topic_id))
            ct = self.db_cursor.fetchall()
            ret = Course()
            if ct:
                cname = ct[0][0]
                ctopic = ct[0][1]
                ret = [cname, ctopic]
            else:
                ret = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve course topic: " + str(id))

        return ret

    def set_curriculum_course(self, curriculum_name, course_name, required, updating=True):
        """Function to write curriculum course to the db"""
        CURRICULUM_COURSE_QUERY = """UPDATE CurriculumListings SET required = %s WHERE curriculum_name = %s AND course_name = %s""" if updating \
            else """INSERT INTO CurriculumListings (curriculum_name, course_name, required) VALUES (%s, %s, %s)"""

        if not updating:
            self.db_cursor.execute(
                CURRICULUM_COURSE_QUERY,
                (curriculum_name, course_name, required))
        else:
            self.db_cursor.execute(
                CURRICULUM_COURSE_QUERY,
                (required, curriculum_name, course_name))
        self.db_connection.commit()

    def set_curriculum_topic(self, curriculum_topic, updating=False):
        """Function to write curriculum topic to the db"""
        CURRICULUM_TOPIC_QUERY = """UPDATE CurriculumListings SET level = %s, subject_area = %s, time_unit = %s WHERE curriculum_name = %s AND topic_id = %s""" if updating \
            else """INSERT INTO CurriculumTopics (curriculum_name, topic_id, level, subject_area, time_unit) VALUES (%s, %s, %s, %s, %s)"""

        if not updating:
            self.db_cursor.execute(
                CURRICULUM_TOPIC_QUERY,
                (curriculum_topic.curriculum_name, curriculum_topic.topic_id, curriculum_topic.level, curriculum_topic.subject_area, curriculum_topic.time_unit))
        else:
            self.db_cursor.execute(
                CURRICULUM_TOPIC_QUERY,
                (curriculum_topic.level, curriculum_topic.subject_area, curriculum_topic.time_unit, curriculum_topic.curriculum_name, curriculum_topic.topic_id))
        self.db_connection.commit()

    def get_curriculum_topic(self, curriculum_name, curriculum_topic):
        """Function to retrieve curriculum topic from the db"""
        ret = None
        try:
            self.db_cursor.execute(
                """SELECT course_name, topic_id, level, subject_area, time_unit FROM CurriculumTopics WHERE curriculum_name = %s AND topic_id = %s""",
                (curriculum_name, curriculum_topic))
            ct = self.db_cursor.fetchall()
            if ct:
                cname = ct[0][0]
                ctopic = ct[0][1]
                level = ct[0][2]
                subject_area = ct[0][3]
                time_unit = ct[0][4]
                ret = [cname, ctopic, level, subject_area, time_unit]
            else:
                ret = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve curriculum topic: " + str(id))

        return ret

    def curriculum_goal_list(self, curriculum_name):
        """Function to retrieve a list of curriculum goals from the db"""
        ret = None
        try:
            self.db_cursor.execute(
                """SELECT id, description FROM Goal WHERE curriculum_name = %s""",
                (curriculum_name))
            goals = self.db_cursor.fetchall()

            if goals:
                ret = []
                go = Goal()
                go.curriculum_name = curriculum_name
                for g in goals:
                    go.description = g[1]
                    go.id = g[0]
                    ret.append(g)
            else:
                ret = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve curriculum goal list: " + str(id))

        return ret

    def get_section_grades(self, section, section_goal=False):
        """Function to retrieve the section grades from the db and return them as a list
        (this works for SectionGrades table and SectionGoalGrades table)"""
        if not section_goal:
            SECTION_GRADES = """SELECT count_ap, count_a count_am, count_bp, count_b count_bm, count_cp, count_c count_cm, count_dp, count_d, count_dm, count_f,count_i, count_w FROM SectionGrades WHERE course = %s AND semester = %s AND year = % AND section_id = %s"""
        else:
            SECTION_GRADES = """SELECT count_ap, count_a count_am, count_bp, count_b count_bm, count_cp, count_c count_cm, count_dp, count_d, count_dm, count_f FROM SectionGoalGrades WHERE course = %s AND semester = %s AND year = % AND section_id = %s AND goal_id = %s"""

        ret = None
        try:
            if not section_goal:
                self.db_cursor.execute(
                    SECTION_GRADES,
                    (section.course_name, section.semester, section.year, section.section_id))
            else:
                self.db_cursor.execute(
                    SECTION_GRADES,
                    (section.course_name, section.semester, section.year, section.section_id, section.goal_id))
            section_grades = self.db_cursor.fetchall()
            if not section_goal:
                ret = SectionGrades
            else:
                ret = SectionGoalGrades
            if section_grades and not section_goal:
                ret.count_ap= section_grades[0][0]
                ret.count_a = section_grades[0][1]
                ret.count_am = section_grades[0][2]
                ret.count_bp = section_grades[0][3]
                ret.count_b = section_grades[0][4]
                ret.count_bm = section_grades[0][5]
                ret.count_cp = section_grades[0][6]
                ret.count_c = section_grades[0][7]
                ret.count_cm = section_grades[0][8]
                ret.count_dp = section_grades[0][9]
                ret.count_d = section_grades[0][10]
                ret.count_dm = section_grades[0][11]
                ret.count_f = section_grades[0][12]
                ret.count_i = section_grades[0][13]
                ret.count_w = section_grades[0][14]
                ret.course = section.course_name
                ret.semester = section.semester
                ret.year = section.year
                ret.section_id = section.section_id
            elif section_grades and section_goal:
                ret.count_ap = section_grades[0][0]
                ret.count_a = section_grades[0][1]
                ret.count_am = section_grades[0][2]
                ret.count_bp = section_grades[0][3]
                ret.count_b = section_grades[0][4]
                ret.count_bm = section_grades[0][5]
                ret.count_cp = section_grades[0][6]
                ret.count_c = section_grades[0][7]
                ret.count_cm = section_grades[0][8]
                ret.count_dp = section_grades[0][9]
                ret.count_d = section_grades[0][10]
                ret.count_dm = section_grades[0][11]
                ret.count_f = section_grades[0][12]
                ret.course = section.course_name
                ret.semester = section.semester
                ret.year = section.year
                ret.section_id = section.section_id
                ret.goal_id = section.goal_id
            else:
                ret = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve section grades: " + str(id))

        return ret

    def get_sections(self, start_year, start_semester, end_year, end_semester, section_goal=False):
        """Function to retrieve a list of sections based on the given criteria"""
        SECTION_GRADES = """SELECT course_name, section_id, num_students, comment1, comment2 FROM Section WHERE semester = %s AND year = %s"""

        spring = 'R'
        fall = 'F'
        summer = 'S'
        winter = 'W'

        sem1 = {1 : 'F', 2 : 'W', 3 : 'R', 4 : 'S'}
        sem2 = {'F' : 1, 'W' : 2, 'R' : 3,'S' : 4}
        start = sem2[start_semester]
        end = sem2[end_semester]

        semester_list = []
        year_list = []
        if start_year != end_year:
            num_years = end_year-start_year
            for i in range(0, num_years+1):
                year_list.append(start_year+i)
                ctr = start

                # todo: very jank way of doing this but idk what else to do rn
                # basically, for each year, we put on 4 semesters in order of when the start semester occurs
                # we should be putting on one of each
                for i in range(1,5):
                    semester_list.append(sem1[ctr%5])
                    ctr+=1
                    if ctr%5 == 0:
                        ctr+=1
            # when we're done with each year, we pop off the end of semester_list until we have the right end semester
            while semester_list[len(semester_list)-1] != sem1[end]:
                semester_list.pop(len(semester_list)-1)

        else:
            year_list.append(start_year)
            for i in range(start, end+1):
                year_list.append(i)



        ret = None
        section_list1 = []
        section_list2 = []
        current_section = Section()
        try:
            for i in year_list:
                for j in semester_list:
                    self.db_cursor.execute(SECTION_GRADES, (j, i))
                    section_list1 = self.db_cursor.fetchall()
                    for k in section_list1:
                        current_section.course_name = k[0]
                        current_section.section_id = k[1]
                        current_section.num_students = k[2]
                        current_section.comment1 = k[3]
                        current_section.comment2 = k[4]
                        current_section.year = i
                        current_section.semester = j
                        section_list2.append(current_section)
            if section_list2:
                ret = section_list2
            else:
                ret = None

        except:
            logging.warning("DBAdapter: Error- cannot retrieve sections: " + str(id))

        return ret

    def get_sections_of_a_course(self, course):
        """Function to retrieve a list of sections based off of a course"""
        # TODO
        pass