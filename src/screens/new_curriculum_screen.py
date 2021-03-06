import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from src.model import classes
from src.db import adapter
import logging
from src.widgets.dialogues import MessageDialogue
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))


class NewCurriculumScreen(Screen):

    screen_name = 'new_curriculum'

    view_kv_filepath = 'new_curriculum_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(os.path.join(FILE_DIR, self.view_kv_filepath))
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)

    def on_enter(self, *args):
        self.root_widget.populate()


class NewCurriculumScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()
        self.req_courses = set()
        self.opt_courses = set()
        self.cur_topics = {}

    def link_to_app(self, app_ref):
        self.app = app_ref

    def populate(self):
        self.update_live_description_callback()

        self.ids.topics_list.setRows(self.cur_topics)
        self.ids.sv_topics_list.height = self.ids.topics_list.get_height()

        self.ids.req_courses_list.setRows(self.req_courses)
        self.ids.sv_req_courses_list.height = self.ids.req_courses_list.get_height()

        self.ids.opt_courses_list.setRows(self.opt_courses)
        self.ids.sv_opt_courses_list.height = self.ids.opt_courses_list.get_height()

    def back_callback(self):
        self.ids.curriculum_name.text = ''
        self.ids.min_credit_hours.text = ''
        self.ids.id_in_charge.text = ''
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def remove_req_course_callback(self):
        rem_req_course = self.ids.req_courses_list.get_selected_row()
        if rem_req_course is None:
            dialogue = MessageDialogue(title="Row Error",message="No row is selected.")
            dialogue.open()
        else:
            self.req_courses.remove(rem_req_course)
            self.ids.req_courses_list.remove_selected_row()
            self.ids.sv_req_courses_list.height = self.ids.req_courses_list.get_height()

    def remove_opt_course_callback(self):
        rem_opt_course = self.ids.opt_courses_list.get_selected_row()
        if rem_opt_course is None:
            dialogue = MessageDialogue(title="Row Error", message="No row is selected.")
            dialogue.open()
        else:
            self.opt_courses.remove(rem_opt_course)
            self.ids.opt_courses_list.remove_selected_row()
            self.ids.sv_opt_courses_list.height = self.ids.opt_courses_list.get_height()

    def remove_topic_callback(self):
        rem_topic = self.ids.topics_list.get_selected_row()
        if rem_topic is None:
            dialogue = MessageDialogue(title="Row Error", message="No row is selected.")
            dialogue.open()
        else:
            del self.cur_topics[rem_topic]
            self.ids.topics_list.remove_selected_row()
            self.ids.sv_opt_courses_list.height = self.ids.opt_courses_list.get_height(expected_node_height=3.0)

    def add_course_callback(self):
        course_name = self.ids.course_name.text
        course_type = self.ids.course_type.text

        if len(course_name) == 0 or not self.app.client_model.get_course(course_name=course_name):
            logging.info("NewCurriculumScreenRoot: could not find course " + str(course_name))
            dialogue = MessageDialogue(title="Database Error",
                                       message="The Course does not\nexist in the database")
            dialogue.open()
        elif course_name in self.req_courses or course_name in self.opt_courses:
            logging.info("NewCurriculumScreenRoot: course " + str(course_name) + " alread has been added")
            dialogue = MessageDialogue(title="Course Error",
                                       message="The Course with name " + str(course_name) +
                                       "\nhas already been added.")
            dialogue.open()
        elif course_type is 'Required':
            self.req_courses.add(course_name)
            self.ids.req_courses_list.addRow(course_name)
            self.ids.sv_req_courses_list.height = self.ids.req_courses_list.get_height()
            self.ids.course_name.text = ''
            self.ids.course_type.text = 'Required'

        else:
            self.opt_courses.add(course_name)
            self.ids.opt_courses_list.addRow(course_name)
            self.ids.sv_opt_courses_list.height = self.ids.opt_courses_list.get_height(expected_node_height=3.0)
            self.ids.course_name.text = ''
            self.ids.course_type.text = 'Required'

    def add_topic_callback(self):
        topic_id_txt = self.ids.curriculum_topic_id.text
        topic = None
        if len(topic_id_txt) > 0:
            topic = self.app.client_model.get_topic(int(topic_id_txt))

        topic_level = int(self.ids.curriculum_topic_level.text)

        topic_subj_area = None
        topic_subj_area_txt = self.ids.curriculum_topic_subj_area.text
        if len(topic_subj_area_txt) > 0:
            topic_subj_area = topic_subj_area_txt

        curriculum_topic_units = None
        curriculum_topic_units_txt = self.ids.curriculum_topic_units.text
        if len(curriculum_topic_units_txt) > 0:
             curriculum_topic_units = int(float(curriculum_topic_units_txt) * 10.0)
        
        if topic is None or topic_subj_area == None or curriculum_topic_units == None:
            logging.info("NewCurriculumScreenRoot: could not find topic with id " + str(topic_id_txt))
            dialogue = MessageDialogue(title="Database Error",
                                       message="The Topic with id " + str(topic_id_txt) + "\ndoes not exist in the database")
            dialogue.open()

        elif topic.id in self.cur_topics.keys():
            logging.info("NewCurriculumScreenRoot: topic with id " + str(topic.id) + " already added.")
            dialogue = MessageDialogue(title="Topic Error",
                                       message="The Topic with id " + str(topic.id) +
                                               "\nhas already been added.")
            dialogue.open()
        else:
            cTopic = classes.CurriculumTopic()
            cTopic.topic_id = topic.id
            cTopic.level = topic_level
            cTopic.curriculum_name = None
            cTopic.subject_area = topic_subj_area
            cTopic.time_unit = curriculum_topic_units
            cTopic._linked_topic_name = topic.name
            self.cur_topics[topic.id] = cTopic

            self.ids.topics_list.addRow(str(cTopic))
            self.ids.sv_topics_list.height = self.ids.topics_list.get_height()
            self.ids.curriculum_topic_id.text = ''
            self.ids.curriculum_topic_level.text = '1'
            self.ids.curriculum_topic_subj_area.text = ''
            self.ids.curriculum_topic_units.text = ''


    def update_live_description_callback(self):

        name = "<Curriculum Name>" if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text

        min_credit_hours = "<minimum credit hours>" if len(self.ids.min_credit_hours.text) == 0 else int(self.ids.min_credit_hours.text)
        id_in_charge = "<ID>" if len(self.ids.id_in_charge.text) == 0 else self.ids.id_in_charge.text
        cur_topics = "<curriculum topics>" #if len(self.ids.curriculum_topics.text) == 0 \
                                           #else self.ids.curriculum_topics.text.split(',')

        person_name = "<person in charge name>"
        if len(self.ids.id_in_charge.text) != 0:
            p = self.app.client_model.get_person(int(self.ids.id_in_charge.text))
            person_name = "[color=ff0101]????[/color]" if p is None else p.name

        description = []
        IND = "\n           "
        description.append(IND + f"[color=ffffff][size=40]Name: {name}[/size][/color]")
        description.append(IND + f"Minimum Credit Hours: {min_credit_hours}")
        description.append(IND + f"Person in charge: {person_name} (ID:{id_in_charge})")
        topic_names = []

        self.ids.live_description_label.halign = 'left'
        self.ids.live_description_label.valign = 'top'
        self.ids.live_description_label.markup = True
        self.ids.live_description_label.text = ''.join(description)
        self.ids.live_description_label.texture_update()

    def submit_callback(self):

        new_curriculum = classes.Curriculum()

        # getting input from ui
        new_curriculum.name = None if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        new_curriculum.min_credit_hours = None if len(self.ids.min_credit_hours.text) == 0 else self.ids.min_credit_hours.text
        new_curriculum.id_in_charge = None if len(self.ids.id_in_charge.text) == 0 else int(self.ids.id_in_charge.text)

        new_curriculum.req_course_names = self.req_courses
        new_curriculum.opt_course_names = self.opt_courses
        new_curriculum.cur_topics = self.cur_topics.values()

        # to validate input
        #       need to make sure min_credit_hours and id_in_charge are numbers
        #       need to make sure id_in_charge in person table
        #       need to make sure topics are in topics table
        #       need to make sure courses are in courses table
        if self.app.client_model.get_curriculum(new_curriculum.name) is not None:
            logging.info("NewCurriculumScreenRoot: curriculum already exists")
            dialogue = MessageDialogue(title="Curriculum error",
                                       message=f"A Curriculum with name \"{new_curriculum.name}\"\nalready exists.")
            dialogue.open()
            return


        if new_curriculum.name is None or new_curriculum.id_in_charge is None \
                or new_curriculum.min_credit_hours is None or new_curriculum.cur_topics is None\
                or new_curriculum.req_course_names is None:
            logging.info("NewCurriculumScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="A curriculum Name, id in charge,\nand minimum credit hours are required.")
            dialogue.open()
            return

        if new_curriculum.cur_topics is not []:
            for ct in new_curriculum.cur_topics:
                tp = self.app.client_model.get_topic(ct.topic_id)
                if tp is None:
                    logging.info("NewCurriculumScreenRoot: Invalid topic")
                    dialogue = MessageDialogue(title="Database error", message="One of the topics does not exist in the\n database.")
                    dialogue.open()
                    return

        for c in new_curriculum.opt_course_names:
            cs = self.app.client_model.get_course(c)
            if cs.name is None:
                logging.info("NewCurriculumScreenRoot: Invalid course: " + str(c))
                dialogue = MessageDialogue(title="Database error",
                                           message="One of the courses does not exist\nin the database.")
                dialogue.open()
                return
        for c in new_curriculum.req_course_names:
            cs = self.app.client_model.get_course(c)
            if cs.name is None:
                logging.info("NewCurriculumScreenRoot: Invalid course: " + str(c))
                dialogue = MessageDialogue(title="Database error",
                                           message="One of the courses does not exist\nin the database.")
                dialogue.open()
                return

        p = self.app.client_model.get_person(new_curriculum.id_in_charge)

        if not p:
            logging.info("NewCurriculumScreenRoot: Invalid person")
            dialogue = MessageDialogue(title="Database error", message="The person id does not exist in the db")
            dialogue.open()
            return

        for t in new_curriculum.cur_topics:
            t.curriculum_name = new_curriculum.name

        # finally, need to check duplicate submisson...right?
        already_in_db = self.app.client_model.get_curriculum(new_curriculum.name)
        if already_in_db:
            logging.info("NewCurriculumScreenRoot: Duplicate Sumbission")
            dialogue = MessageDialogue(title="Database error", message="A curriculum with this name already exists in the db")
            dialogue.open()
            return

        self.app.client_model.set_curriculum(new_curriculum)
        self.ids.curriculum_name.text = ''
        self.ids.min_credit_hours.text = ''
        self.ids.id_in_charge.text = ''
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'
        dialogue = MessageDialogue(title="success", message="successfully created the curriculum")
        dialogue.open()

        print("submit")
