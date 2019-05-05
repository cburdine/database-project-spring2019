from src.db.adapter import DBAdapter
from src.model.classes import Person, CurriculumTopic

"""
The purpose of this class is to serve as a
'Flyweight' model for the database, which
caches all values retrieved from the
database so that they do not need to 
be read from again. Values can then
be updated as often as needed.
"""
class ClientModel:

    def __init__(self, adapter_ref):
        self.adapter = adapter_ref

        # These should not be accessed directly:
        self._curricula_map = {}
        self._person_map = {}
        self._course_map = {}
        self._topic_map = {}
        self._goal_map = {}
        self._section_map = {}
        self._cur_topic_temp = CurriculumTopic()

    def get_person(self, id):

        if id in self._person_map.keys():
            return self._person_map[id]
        else:
            p = self.adapter.get_person(id)
            if p == None:
                return None
            else:
                self._person_map[id] = p
                return p

    def get_curriculum_names(self):

        if len(self._curricula_map.keys()) <= 0:
            self.update_curriculum_names()
        return self._curricula_map.keys()

    def update_curriculum_names(self):
        for name in self.adapter.get_curricula_names():
            self._curricula_map[name] = None

    def get_curriculum(self, name):
        if name in self._curricula_map.keys():
            if self._curricula_map[name] == None:
                self._curricula_map[name] = self.adapter.get_curriculum(name)
            return self._curricula_map[name]
        else:
            return None

    def update_curriculum(self, name):
        if name not in self._curricula_map.keys():
            self.update_curriculum_names()

        if name in self._curricula_map.keys():
            self._curricula_map[name] = self.adapter.get_curriculum(name)

    def get_topic(self, id):
        if id in self._topic_map.keys():
            return self._topic_map[id]
        else:
            t = self.adapter.get_topic(id)
            if t is None:
                return None
            else:
                self._topic_map[id] = t
                return t

    def set_topic(self, new_topic):
        """Function to add new topic to the db"""
        self.adapter.set_topic(new_topic)
        self._topic_map[new_topic.id] = new_topic # updating our topic map

    def set_person(self, new_person):
        """Function to add new person to the db"""
        self.adapter.set_person(new_person)
        self._person_map[new_person.id] = new_person # updating our person map

    def get_course(self, course_name):
        """Function to retrieve a topic from the db"""
        if course_name in self._course_map.keys():
            return self._course_map[course_name]
        else:
            c = self.adapter.get_course(course_name)
            if c != None:
                self._course_map[course_name] = c
                return c

    def set_course(self, new_course):
        """Function to add new course to the database"""
        self.adapter.set_course(new_course)
        self._course_map[new_course.name] = new_course
        # print(self._course_map)

    def get_section(self, new_section):
        if new_section.unit_id in self._section_map.keys():
            return self._section_map[new_section.unit_id]
        else:
            return self.adapter.get_section(new_section)

    def set_section(self, new_section):
        """Function that adds new section to the database"""
        self.adapter.set_section(new_section)
        self._section_map[new_section.unit_id] = new_section

    def set_curriculum(self, new_curriculum):
        """Function to set new curriculum"""
        self.adapter.set_curriculum(new_curriculum)
        self._curricula_map[new_curriculum.name] = new_curriculum
        if new_curriculum.name not in self._curricula_map.values():
            self._curricula_map[new_curriculum.name] = None

    def get_goal(self, new_goal):
        """Function to get a goal from the db"""
        if new_goal.id in self._goal_map.keys():
            return self._goal_map.keys()
        else:
            return self.adapter.get_goal(new_goal)

    def set_goal(self, new_goal):
        """Function to set goal"""
        self.adapter.set_goal(new_goal)
        self._curricula_map[new_goal.id] = new_goal

    def set_course_goal(self, goal_id, course_name):
        """Function to set a course goal in the database"""
        self.adapter.set_course_goal(goal_id, course_name)

    def set_course_topic(self, topic_id, course_name):
        """Function to set course topic"""
        self.adapter.set_course_topic(topic_id,course_name)

    def set_curriculum_course(self, curriculum_name, course_name, required):
        """Function to set curriculum course in the db"""
        self.adapter.set_curriculum_course(curriculum_name, course_name, required)

    def set_curriculum_topic(self, curriculum_topic):
        """Function to set curriculum topic"""
        self.adapter.set_curriculum_topic(curriculum_topic)


