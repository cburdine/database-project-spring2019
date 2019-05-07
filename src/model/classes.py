"""
This file contains classes for our database entities.
Notes: - classes are made based off of actual entities
       - classes are meant to help store class information retrieved from database
"""

"""
The idea behind this class is to store and retrieve information from the curriculum table

In this iteration, I took the liberty of making the class variables lists instead of just single variables.
This is so that when we store/retrieve information from this table in the database, we can store it ia single
object and not have to use multiple
"""
class Curriculum:
    def __init__(self):
        self.name = None
        self.min_credit_hours = None
        self.id_in_charge = None
        self.cur_topics = []
        self.opt_course_names = []
        self.req_course_names = []

    def __str__(self):
        """
        Overridden str function
        """
        str = f"name: {self.name}" + \
              f"\nmin_credit_hours: {self.min_credit_hours}" + \
              f"\nid_in_charge: {self.id_in_charge}"
        return str

"""
Class to store and retrieve information from the course table
"""
class Course:
    def __init__(self):
        self.name = None
        self.subject_code = None
        self.credit_hours = None
        self.description = None
        self.topics = []
        self.goals = []

    def __str__(self):
        """
        Overridden str function
        """
        str = f"name: {self.name}" + \
              f"\nmin_credit_hours: {self.subject_code}" + \
              f"\nid_in_charge: {self.credit_hours}" + \
              f"\nid_in_charge: {self.description}"
        return str

"""Person class"""

class Person:
    def __init__(self):
        self.name = None
        self.id = None

    def __str__(self):
        """
        Overridden str function
        """
        str = f"name: {self.name}" + \
              f"\nid: {self.id}"
        return str

    def set_name(self, n):
        self.name = n

    def set_id(self, mch):
        self.id = mch

class Topic:
    def __init__(self):
        self.id = None
        self.name = None

    def __str__(self):
        """
        Overridden str function
        """
        str = f"{self.name} (ID: {self.id})"

        return str


class CurriculumTopic:
    def __init__(self):
        self.curriculum_name = None
        self.topic_id = None
        self.level = None
        self.subject_area = None
        self.time_unit = None
        self._linked_topic_name = None

    def __str__(self):
        """
        Overridden str function
        """
        ret = []
        if self._linked_topic_name != None:
            ret.append(str(self._linked_topic_name) +
                       " (ID: " + str(self.topic_id) + ") ")
        else:
            ret.append(f"Topic #{str(self.topic_id)}")
        ret.append(f"\nSubject: {self.subject_area} (Level {self.level})")
        ret.append(f"\nTime Units: {self.time_unit/10.0}")
        return ''.join(ret)

    def link_topic_name(self, topic_name):
        self._topic_linked_name = topic_name

class Section:
    def __init__(self):
        self.course_name = None
        self.semester = None
        self.year = None
        self.section_id = None
        self.num_students = None
        self.comment1 = None
        self.comment2 = None

    def __str__(self):
        """
        Overridden str function
        """
        str = []
        str.append(f"course_name: {self.course_name}\n")
        str.append(f"semester: {self.semester}\n")
        str.append(f"year: {self.year}\n")
        str.append(f"section_id: {self.section_id}\n")
        str.append(f"num_students: {self.num_students}\n")
        str.append(f"comment1: {self.comment1}\n")
        str.append(f"comment2: {self.comment2}\n")
        return ''.join(str)


class SectionGrades:

    #Maybe use an array here?
    def __init__(self):
        self.course = None
        self.semester = None
        self.year = None
        self.section_id = None
        self.count_ap = 0
        self.count_a = 0
        self.count_am = 0
        self.count_bp = 0
        self.count_b = 0
        self.count_bm = 0
        self.count_cp = 0
        self.count_c = 0
        self.count_cm = 0
        self.count_dp = 0
        self.count_d = 0
        self.count_dm = 0
        self.count_f = 0
        self.count_i = 0
        self.count_w = 0

    def __str__(self):
        """
        Overridden str function
        """
        ret = []
        ret.append(f"course: {self.course}\n")
        ret.append(f"semester: {self.semester}\n")
        ret.append(f"unit_id: {self.section_id}\n")
        ret.append(f"count_ap: {self.count_ap}\n")
        ret.append(f"count_a: {self.count_a}\n")
        ret.append(f"count_am,: {self.count_am}\n")
        ret.append(f"count_bp: {self.count_bp}\n")
        ret.append(f"count_b: {self.count_b}\n")
        ret.append(f"count_bm,: {self.count_bm}\n")
        ret.append(f"count_cp: {self.count_cp}\n")
        ret.append(f"count_c: {self.count_c}\n")
        ret.append(f"count_cm,: {self.count_cm}\n")
        ret.append(f"count_dp: {self.count_dp}\n")
        ret.append(f"count_d: {self.count_d}\n")
        ret.append(f"count_dm,: {self.count_dm}\n")
        ret.append(f"count_i: {self.count_i}\n")
        ret.append(f"count_w: {self.count_w}\n")
        return ''.join(ret)

class SectionGoalGrades:
    def __init__(self):
        self.course = None
        self.semester = None
        self.year = None
        self.section_id = None
        self.goal_id = None
        self.count_ap = 0
        self.count_a = 0
        self.count_am = 0
        self.count_bp = 0
        self.count_b = 0
        self.count_bm = 0
        self.count_cp = 0
        self.count_c = 0
        self.count_cm = 0
        self.count_dp = 0
        self.count_d = 0
        self.count_dm = 0
        self.count_f = 0

    def __str__(self):
        """
        Overridden str function
        """
        ret = []
        ret.append(f"course: {self.course}\n")
        ret.append(f"semester: {self.semester}\n")
        ret.append(f"unit_id: {self.section_id}\n")
        ret.append(f"goal_id: {self.goal_id}\n")
        ret.append(f"count_ap: {self.count_ap}\n")
        ret.append(f"count_a: {self.count_a}\n")
        ret.append(f"count_am,: {self.count_am}\n")
        ret.append(f"count_bp: {self.count_bp}\n")
        ret.append(f"count_b: {self.count_b}\n")
        ret.append(f"count_bm,: {self.count_bm}\n")
        ret.append(f"count_cp: {self.count_cp}\n")
        ret.append(f"count_c: {self.count_c}\n")
        ret.append(f"count_cm,: {self.count_cm}\n")
        ret.append(f"count_dp: {self.count_dp}\n")
        ret.append(f"count_d: {self.count_d}\n")
        ret.append(f"count_dm,: {self.count_dm}\n")
        return ''.join(ret)

class Goal:
    def __init__(self):
        self.id = None
        self.curriculum_name = None
        self.description = None

    def __str__(self):
        """
        Overridden str function
        """
        ret = []
        ret.append(f"Goal #{self.id}\n")
        ret.append(f"Curriculum: {self.curriculum_name}\n")
        ret.append(f"{self.description}")
        return ''.join(ret)

    def __hash__(self):
        return hash(self.id, self.curriculum_name)

class ContextFreeGoal:

    def __init__(self):
        self.id = None
        self.description = None

    def __str__(self):
        return self.description


