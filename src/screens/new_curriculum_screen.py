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

class NewCurriculumScreen(Screen):

    screen_name = 'new_curriculum'

    view_kv_filepath = 'screens/new_curriculum_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewCurriculumScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def submit_callback(self):

        new_curriculum = classes.Curriculum()

        # getting input from ui
        new_curriculum.name = None if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        new_curriculum.min_credit_hours = None if len(self.ids.min_credit_hours.text) == 0 else self.ids.min_credit_hours.text
        new_curriculum.id_in_charge = None if len(self.ids.id_in_charge.text) == 0 else self.ids.id_in_charge.text
        new_curriculum.cur_topics = None if len(self.ids.curriculum_topics.text) == 0 else self.ids.curriculum_topics.text
        if new_curriculum.cur_topics is not None:
            new_curriculum.cur_topics = new_curriculum.cur_topics.split(', ')
        new_curriculum.req_course_names = None if len(self.ids.required_courses.text) == 0 else self.ids.required_courses.text
        if new_curriculum.req_course_names is not None:
            new_curriculum.req_course_names = new_curriculum.req_course_names.split(', ')
        new_curriculum.opt_course_names = None if len(self.ids.optional_courses.text) == 0 else self.ids.optional_courses.text
        if new_curriculum.opt_course_names is not None:
            new_curriculum.opt_course_names = new_curriculum.opt_course_names.split(', ')

        # to validate input
        #       need to make sure min_credit_hours and id_in_charge are numbers
        #       need to make sure id_in_charge in person table
        #       need to make sure topics are in topics table todo: needs to work for multiple topics
        #       need to make sure courses are in courses table

        can_submit = True

        if new_curriculum.min_credit_hours is not None:
            min_credit_hours_is_numeric = False
            if str.isdigit(new_curriculum.min_credit_hours):
                min_credit_hours_is_numeric = True

        if new_curriculum.id_in_charge is not None:
            id_in_charge_is_numeric = False
            if str.isdigit(new_curriculum.id_in_charge):
                id_in_charge_is_numeric = True

        topic_exists = False
        tp = None
        for ct in new_curriculum.cur_topics:
            if str.isdigit(ct):
                tp = self.app.client_model.get_topic(ct)
                if tp.name is not None:
                    topic_exists = True
                    tp = None
            if not topic_exists:
                logging.info("NewCurriculumScreenRoot: Invalid topic")
                dialogue = MessageDialogue(title="Database error", message="One of the topics does not exist in the db")
                dialogue.open()
                can_submit = False
            topic_exists = False

        courses_exist = False
        cs = None
        if new_curriculum.req_course_names is not None and new_curriculum.opt_course_names is not None:
            courses =  new_curriculum.req_course_names + new_curriculum.opt_course_names
        elif new_curriculum.req_course_names is not None:
            courses = new_curriculum.req_course_names
        elif new_curriculum.opt_course_names is not None:
            courses = new_curriculum.opt_course_names
        for c in courses:
            cs = self.app.client_model.get_course(c)
            if cs.name is not None:
                courses_exist = True
                cs = None
            if not courses_exist:
                logging.info("NewCurriculumScreenRoot: Invalid course")
                dialogue = MessageDialogue(title="Database error", message="One of the courses does not exist in the db")
                dialogue.open()
                can_submit = False
            courses_exists = False

        person_id_exists = False
        p = None
        p = self.app.client_model.get_person(new_curriculum.id_in_charge)
        if p.id is not None:
            person_id_exists = True
        if not person_id_exists:
            logging.info("NewCurriculumScreenRoot: Invalid person")
            dialogue = MessageDialogue(title="Database error", message="The person id does not exist in the db")
            dialogue.open()
            can_submit = False

        if new_curriculum.name is None or new_curriculum.id_in_charge is None \
                or new_curriculum.min_credit_hours is None or new_curriculum.cur_topics is None\
                or new_curriculum.req_course_names is None:
            logging.info("NewCurriculumScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
            can_submit = False
        elif not min_credit_hours_is_numeric:
            logging.info("NewCurriculumScreenRoot: minimum credit hours must be numeric")
            dialogue = MessageDialogue(title="Format error", message="minimum credit hours must be numeric")
            dialogue.open()
            can_submit = False
        elif not id_in_charge_is_numeric:
            logging.info("NewCurriculumScreenRoot: id in charge must be numeric")
            dialogue = MessageDialogue(title="Format error", message="id of person in charge must be numeric")
            dialogue.open()
            can_submit = False
        elif can_submit:
            # describe the topic further

            self.app.client_model.set_curriculum(new_curriculum)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'main' # todo, need to further describe
                                                      # curriculum topic before we can finish

        print("submit")
