from src.db.adapter import DBAdapter
from src.model.classes import Person, CurriculumTopic, Curriculum
import logging
from src.widgets.dialogues import MessageDialogue

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

    def get_course_topic(self, topic_id, course_name):
        """Function to get the course topic"""
        return self.adapter.get_course_topic(topic_id, course_name)

    def set_curriculum_course(self, curriculum_name, course_name, required):
        """Function to set curriculum course in the db"""
        self.adapter.set_curriculum_course(curriculum_name, course_name, required)

    def set_curriculum_topic(self, curriculum_topic):
        """Function to set curriculum topic"""
        self.adapter.set_curriculum_topic(curriculum_topic)

    def get_curriculum_topic(self, curriculum_name, curriculum_topic_id):
        """Function to retrieve curriculum topic from the db"""
        return self.adapter.get_curriculum_topic(curriculum_name, curriculum_topic_id)

    def evaluate_curriculum(self, curriculum_name, required_percentage = .5):
        """Function to evaluate the curriculum in terms of coverage by topics and returning a string
        defining the topic coverage of the curriculum"""

        # making sure the curriculum exists
        curriculum_obj = Curriculum()
        curriculum_obj = self.get_curriculum(curriculum_name)
        if curriculum_obj.name is None:
            logging.info("ClentModel: Invalid Curriculum")
            dialogue = MessageDialogue(title="Database error",
                                       message="The Curriculum does not exist in the db.")
            dialogue.open()
        else:

            level_1_topics_covered_by_required_courses = []
            level_2_topics_covered_by_required_courses = []
            level_3_topics_covered_by_required_courses = []

            level_1_topics_covered_period = []
            level_2_topics_covered_period = []
            level_3_topics_covered_period = []

            level_1_topics = []
            level_2_topics = []
            level_3_topics = []

            for i in curriculum_obj.cur_topics:
                q = self.get_curriculum_topic(curriculum_obj.name, i)
                c_name = i[0]
                curriculum_topic = i[1]
                level = i[2]
                subject_area = i[3]
                time_unit = i[4]

                if level == 1:
                    level_1_topics.append(q)
                elif level == 2:
                    level_2_topics.append(q)
                elif level == 3:
                    level_3_topics.append(q)

                hours_to_cover = time_unit

                for j in curriculum_obj.req_course_names:
                    k = self.get_course_topic(i, j)
                    course_topic = k[1]

                    if curriculum_topic == course_topic:
                        d = self.get_course(j)
                        cred_hours = d.credit_hours
                        hours_to_cover -= cred_hours

                if hours_to_cover <= 0:
                    if level == 1:
                        level_1_topics_covered_by_required_courses.append(q)
                    elif level == 2:
                        level_2_topics_covered_by_required_courses.append(q)
                    elif level == 3:
                        level_3_topics_covered_by_required_courses.append(q)
                else:

                    for j in curriculum_obj.opt_course_names:
                        k = self.get_course_topic(i, j)
                        course_topic = k[1]
                        if curriculum_topic == course_topic:
                            d = self.get_course(j)
                            cred_hours = d.credit_hours
                            hours_to_cover -= cred_hours


                    if hours_to_cover <= 0:
                        if level == 1:
                            level_1_topics_covered_period.append(q)
                        elif level == 2:
                            level_2_topics_covered_period.append(q)
                        elif level == 3:
                            level_3_topics_covered_period.append(q)





            if len(level_1_topics_covered_by_required_courses) == len(level_1_topics):
                all_1_covered_by_required = True
            else:
                all_1_covered_by_required = False

            if len(level_2_topics_covered_by_required_courses) == len(level_2_topics):
                all_2_covered_by_required = True
            else:
                all_2_covered_by_required = False

            if level_3_topics_covered_by_required_courses:
                level_3_covered_by_required = True
            else:
                level_3_covered_by_required = False


            if len(level_1_topics_covered_period) == len(level_1_topics):
                all_1_covered = True
            else:
                all_1_covered = False

            if len(level_2_topics_covered_period) == len(level_2_topics):
                all_2_covered = True
            else:
                all_2_covered = False



            if all_1_covered_by_required and all_2_covered_by_required and len(level_3_topics_covered_by_required_courses)/len(level_3_topics) >= required_percentage:
                return 'Extensive'
            elif all_1_covered_by_required and all_2_covered_by_required and len(level_3_topics_covered_by_required_courses)/len(level_3_topics) < required_percentage:
                return 'Inclusive'
            elif all_1_covered_by_required and len(level_2_topics_covered_by_required_courses)/len(level_2_topics) >= required_percentage and all_1_covered and all_2_covered:
                return 'Basic-plus'
            elif all_1_covered_by_required and len(level_2_topics_covered_by_required_courses)/len(level_2_topics) >= required_percentage:
                return 'Basic'
            elif all_1_covered_by_required and len(level_2_topics_covered_by_required_courses)/len(level_2_topics) < required_percentage:
                return 'Unsatisfactory'
            elif not all_1_covered_by_required:
                return 'Substandard'