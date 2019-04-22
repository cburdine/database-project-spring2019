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
        self.topic_ids = []
        self.opt_course_names = []
        self.required_course_names = []

    def __str__(self):
        """
        Overridden str function
        """
        print(f"name: {self.name}")
        print(f"min_credit_hours: {self.min_credit_hours}")
        print(f"id_in_charge: {self.id_in_charge}")

"""
Class to store and retrieve information from the course table
"""
class Course:
    def __init__(self):
        self.name = None
        self.subject_code = None
        self.credit_hours = None
        self.description = None

    def __str__(self):
        """
        Overridden str function
        """
        print(f"name: {self.name}")
        print(f"min_credit_hours: {self.subject_code}")
        print(f"id_in_charge: {self.credit_hours}")
        print(f"id_in_charge: {self.description}")


"""Person class"""

class Person:
    def __init__(self):
        self.name = None
        self.id = None

    def __str__(self):
        """
        Overridden str function
        """
        print(f"name: {self.name}")
        print(f"id: {self.id}")

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
        print(f"name: {self.name}")
        print(f"id: {self.id}")

    def set_name(self, n):
        self.name = n

    def set_id(self, mch):
        self.id = mch

class CurriculumTopics:
    def __init__(self):
        self.curriculum_name = None
        self.topic_id = None
        self.level = None
        self.subject_area = None
        self.time_unit = None

    def __str__(self):
        """
        Overridden str function
        """
        print(f"curriculum_name: {self.curriculum_name}")
        print(f"topic_id: {self.topic_id}")
        print(f"level: {self.level}")
        print(f"subject_area: {self.subject_area}")
        print(f"time_unit: {self.time_unit}")

    def set_curriculum_name(self, n):
        self.curriculum_name = n

    def set_topic_id(self, n):
        self.topic_id = n

    def set_level(self, n):
        self.level = n

    def set_subject_area(self, n):
        self.subject_area = n

    def set_time_unit(self, n):
        self.time_unit = n

class Section:
    def __init__(self):
        self.course_name = None
        self.semester = None
        self.unit_id = None
        self.num_students = None
        self.comment1 = None
        self.comment2 = None

    def __str__(self):
        """
        Overridden str function
        """
        print(f"course_name: {self.course_name}")
        print(f"semester: {self.semester}")
        print(f"unit_id: {self.unit_id}")
        print(f"num_students: {self.num_students}")
        print(f"comment1: {self.comment1}")
        print(f"comment2: {self.comment2}")

    def set_course_name(self, n):
        self.course_name = n

    def set_semester(self, n):
        self.semester = n

    def set_unit_id(self, n):
        self.unit_id = n

    def set_num_students(self, n):
        self.num_students = n

    def set_comment1(self, n):
        self.comment1 = n

    def set_comment2(self, n):
        self.comment2 = n

class SectionGrades:

    #Maybe use an array here?
    def __init__(self):
        self.course = None
        self.semester = None
        self.unit_id = None
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
        self.count_i = 0
        self.count_w = 0

    def __str__(self):
        """
        Overridden str function
        """
        print(f"course: {self.course}")
        print(f"semester: {self.semester}")
        print(f"unit_id: {self.unit_id}")
        print(f"count_ap: {self.count_ap}")
        print(f"count_a: {self.count_a}")
        print(f"count_am,: {self.count_am}")
        print(f"count_bp: {self.count_bp}")
        print(f"count_b: {self.count_b}")
        print(f"count_bm,: {self.count_bm}")
        print(f"count_cp: {self.count_cp}")
        print(f"count_c: {self.count_c}")
        print(f"count_cm,: {self.count_cm}")
        print(f"count_dp: {self.count_dp}")
        print(f"count_d: {self.count_d}")
        print(f"count_dm,: {self.count_dm}")
        print(f"count_i: {self.count_i}")
        print(f"count_w: {self.count_w}")

    def set_course(self, n):
        self.course = n

    def set_semester(self, n):
        self.semester = n

    def set_unit_id(self, n):
        self.unit_id = n

    def set_count_ap(self, n):
        self.count_ap = n

    def set_count_a(self, n):
        self.count_a = n

    def set_count_am(self, n):
        self.count_am = n

    def set_count_bp(self, n):
        self.count_bp = n

    def set_count_b(self, n):
        self.count_b = n

    def set_count_bm(self, n):
        self.count_bm = n

    def set_count_cp(self, n):
        self.count_cp = n

    def set_count_c(self, n):
        self.count_c = n

    def set_count_cm(self, n):
        self.count_cm = n

    def set_count_dp(self, n):
        self.count_dp = n

    def set_count_d(self, n):
        self.count_d = n

    def set_count_dm(self, n):
        self.count_dm = n

    def set_count_i(self, n):
        self.count_i = n

    def set_count_w(self, n):
        self.count_w = n


class SectionGoalGrades:
    def __init__(self):
        self.course = None
        self.semester = None
        self.unit_id = None
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

    def __str__(self):
        """
        Overridden str function
        """
        print(f"course: {self.course}")
        print(f"semester: {self.semester}")
        print(f"unit_id: {self.unit_id}")
        print(f"goal_id: {self.goal_id}")
        print(f"count_ap: {self.count_ap}")
        print(f"count_a: {self.count_a}")
        print(f"count_am,: {self.count_am}")
        print(f"count_bp: {self.count_bp}")
        print(f"count_b: {self.count_b}")
        print(f"count_bm,: {self.count_bm}")
        print(f"count_cp: {self.count_cp}")
        print(f"count_c: {self.count_c}")
        print(f"count_cm,: {self.count_cm}")
        print(f"count_dp: {self.count_dp}")
        print(f"count_d: {self.count_d}")
        print(f"count_dm,: {self.count_dm}")

    def set_course(self, n):
        self.course = n

    def set_semester(self, n):
        self.semester = n

    def set_unit_id(self, n):
        self.unit_id = n

    def set_goal_id(self, n):
        self.goal_id = n

    def set_count_ap(self, n):
        self.count_ap = n

    def set_count_a(self, n):
        self.count_a = n

    def set_count_am(self, n):
        self.count_am = n

    def set_count_bp(self, n):
        self.count_bp = n

    def set_count_b(self, n):
        self.count_b = n

    def set_count_bm(self, n):
        self.count_bm = n

    def set_count_cp(self, n):
        self.count_cp = n

    def set_count_c(self, n):
        self.count_c = n

    def set_count_cm(self, n):
        self.count_cm = n

    def set_count_dp(self, n):
        self.count_dp = n

    def set_count_d(self, n):
        self.count_d = n

    def set_count_dm(self, n):
        self.count_dm = n

class Goal:
    def __init__(self):
        self.id = None
        self.curriculum_name = None
        self.description = None

    def __str__(self):
        """
        Overridden str function
        """
        print(f"id: {self.id}")
        print(f"curriculum_name: {self.curriculum_name}")
        print(f"description: {self.description}")

    def set_id(self, n):
        self.id = n

    def set_curriculum_name(self, n):
        self.curriculum_name = n

    def set_description(self, n):
        self.description = n
