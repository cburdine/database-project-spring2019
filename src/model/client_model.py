from src.db.adapter import DBAdapter
from src.model.classes import Person

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

    def get_person(self, id):

        #if id not in self._person_map.keys():
            #self._person_map[id] = self.adapter.get_person(id)
        #return self._person_map[id]

        if id in self._person_map.keys():
            return self._person_map[id]
        else:
            return self.adapter.get_person(id)

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
            return self.adapter.get_topic(id)

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
            return self.adapter.get_course(course_name)

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

