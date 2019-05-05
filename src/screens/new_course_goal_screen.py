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


class NewCourseGoalScreen(Screen):

    screen_name = 'new_course_goal'

    view_kv_filepath = 'screens/new_course_goal_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewCourseGoalScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'

    def submit_callback(self):
        # getting input from ui
        goal_id =  None if len(self.ids.goal_id.text) == 0 else self.ids.goal_id.text
        course_name = None if len(self.ids.course_name.text) == 0 else self.ids.course_name.text

        # checking db
        goal_in_db = None
        g = None
        if goal_id is not None:
            g = self.app.client_model.get_goal(goal_id)
            if g.id is None:
                goal_in_db = False
            else:
                goal_in_db = True

        course_in_db = False
        c = None
        if course_name is not None:
            c = self.app.client_model.get_course(course_name)
            if c.name is None:
                course_in_db = False
            else:
                course_in_db = True


        # validating input
        if goal_id is None or course_name is None:
            logging.info("NewCourseGoalScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
        elif goal_in_db is False:
            logging.info("NewCourseGoalScreenRoot: Goal not in db")
            dialogue = MessageDialogue(title="db error", message="Goal with this id is not in database")
            dialogue.open()
        elif course_in_db is False:
            logging.info("NewCourseGoalScreenRoot: Course not in db")
            dialogue = MessageDialogue(title="db error", message="Course with this name is not in database")
            dialogue.open()
        else:
            # safe to enter into database
            self.app.client_model.set_course_goal(goal_id, course_name)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.ids.goal_id.text = ''
            self.ids.course_name.text = ''
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'main'


