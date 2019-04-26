from src.db.adapter import DBAdapter

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

        if id not in self._person_map.keys():
            self._person_map[id] = self.adapter.get_person(id)
        return self._person_map[id]

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
            print(self._topic_map[id])
            return self._topic_map[id]
        else:
            return self.adapter.get_topic(id)

    def set_topic(self, new_topic):
        """Function to add new topic to the db"""
        self.adapter.set_topic(new_topic)
        self._topic_map[new_topic.id] = new_topic.name # updating our topic map

    #def update


