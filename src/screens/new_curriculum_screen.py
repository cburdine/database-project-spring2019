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

    def on_enter(self, *args):
        self.root_widget.populate()


class NewCurriculumScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()
        self.req_courses

    def link_to_app(self, app_ref):
        self.app = app_ref

    def populate(self):
        self.update_live_description_callback()

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'



    def update_live_description_callback(self):

        name = "<Curriculum Name>" if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        min_credit_hours = "<minimum credit hours>" if len(self.ids.min_credit_hours.text) == 0 else int(self.ids.min_credit_hours.text)
        id_in_charge = "<person in charge>" if len(self.ids.id_in_charge.text) == 0 else self.ids.id_in_charge.text
        cur_topics = "<curriculum topics>" #if len(self.ids.curriculum_topics.text) == 0 \
                                           #else self.ids.curriculum_topics.text.split(',')
        person_name = "<person in charge name>"

        description = []
        IND = "\n           "
        description.append(IND + f"[color=ffffff][size=40]Name: {name}[/size][/color]")
        description.append(IND + f"Minimum Credit Hours: {min_credit_hours}")
        description.append(IND + f"Person in charge: {person_name} (id:{id})")
        topic_names = []

        many = False
        for t in topic_names:
            if len(t) > 0:
                if many:
                    description.append(', ')
                else:
                    many = True
                description.append(t.strip())

        description.append(IND + IND + f"[color=ffffff][size=20]Required Courses:[/size][/color]" + IND)
        req_course_names = []
        many = False
        for t in req_course_names:
            if len(t) > 0:
                if many:
                    description.append(', ')
                else:
                    many = True
                description.append(t.strip())

        description.append(IND + IND + f"[color=ffffff][size=20]Elective Courses:[/size][/color]" + IND)
        opt_course_names = []
        many = False
        for t in opt_course_names:
            if len(t) > 0:
                if many:
                    description.append(', ')
                else:
                    many = True
                description.append(t.strip())

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

        new_curriculum.cur_topics = [] if len(self.ids.curriculum_topics.text) == 0 else self.ids.curriculum_topics.text
        if new_curriculum.cur_topics and new_curriculum.cur_topics is not []:
            new_curriculum.cur_topics = [s.strip() for s in new_curriculum.cur_topics.split(',')]

        new_curriculum.req_course_names = [] if len(self.ids.required_courses.text) == 0 else self.ids.required_courses.text
        if new_curriculum.req_course_names and new_curriculum.req_course_names is not []:
            new_curriculum.req_course_names = [s.strip() for s in new_curriculum.req_course_names.split(',')]

        new_curriculum.opt_course_names = [] if len(self.ids.optional_courses.text) == 0 else self.ids.optional_courses.text
        if new_curriculum.opt_course_names and new_curriculum.opt_course_names is not []:
            new_curriculum.opt_course_names = [s.strip() for s in new_curriculum.opt_course_names.split(',')]

        # to validate input
        #       need to make sure min_credit_hours and id_in_charge are numbers
        #       need to make sure id_in_charge in person table
        #       need to make sure topics are in topics table
        #       need to make sure courses are in courses table

        if new_curriculum.name is None or new_curriculum.id_in_charge is None \
                or new_curriculum.min_credit_hours is None or new_curriculum.cur_topics is None\
                or new_curriculum.req_course_names is None:
            logging.info("NewCurriculumScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="A curriculum Name, id in charge,\nand minimum credit hours are required.")
            dialogue.open()
            return

        if new_curriculum.cur_topics is not []:
            for ct in new_curriculum.cur_topics:
                tp = self.app.client_model.get_topic(ct)
                if tp.name is None:
                    logging.info("NewCurriculumScreenRoot: Invalid topic")
                    dialogue = MessageDialogue(title="Database error", message="One of the topics does not exist in the\n database.")
                    dialogue.open()
                    return

        courses = new_curriculum.req_course_names + new_curriculum.opt_course_names
        for c in courses:
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

        # todo: new plan --> make new entry screen for each table (Curriculum Topics,
        #  Curriculum, Curriculum Listings, etc.)
        for i in new_curriculum.cur_topics:
            tmp = classes.CurriculumTopic()
            tmp.topic_id = i
            tmp.curriculum_name = new_curriculum.name
            #self.app.client_model.se

        self.app.client_model.set_temp_cur_topic(tmp)
        self.app.screen_manager.transition.direction = 'up'
        self.app.screen_manager.current = 'new_curriculum_topic'

        print("submit")
