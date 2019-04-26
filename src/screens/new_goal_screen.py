import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from src.model import classes
from src.db import adapter


class NewGoalScreen(Screen):

    screen_name = 'new_goal'

    view_kv_filepath = 'screens/new_goal_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(self.view_kv_filepath)
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)


class NewGoalScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.curriculum = classes.Curriculum()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'add_new_screen'

    def submit_callback(self):
        new_goal = classes.Goal()

        # getting input from ui
        new_goal.curriculum_name = None if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        new_goal.id = None if len(self.ids.goal_id.text) == 0 else self.ids.goal_id.text
        new_goal.description =  None if len(self.ids.description.text) == 0 else self.ids.description.text

        if new_goal.curriculum_name is None or new_goal.id is None:
            print("All fields must contain input")
            self.app.screen_manager.transition.direction = 'up'
            self.app.screen_manager.current = 'add_new_screen'

        # todo: validating input (holding off for now because this depends on a curriculum's existence)

        print("submit")