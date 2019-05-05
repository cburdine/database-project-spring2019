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

    def update_live_description_callback(self):
        curriculum_name = "<Curriculum>" if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        goal_id = "<Goal ID>" if len(self.ids.goal_id.text) == 0 else int(self.ids.goal_id.text)
        goal_description = "<Description>" if len(self.ids.goal_description.text) == 0 else self.ids.goal_description.text

        IND = "\n           "
        description_label = []
        description_label.append(IND + f"[color=ffffff][size=40]Curriculum Name: {curriculum_name}[/size][/color]")
        description_label.append(IND + f"ID Number: {goal_id}")
        description_label.append(IND + IND + f"[color=ffffff][size=24]Goal Description:[/size][/color]")
        description_label.append(IND + str(goal_description))

        self.ids.live_description_label.halign = 'left'
        self.ids.live_description_label.valign = 'top'
        self.ids.live_description_label.markup = True
        self.ids.live_description_label.text = ''.join(description_label)
        self.ids.live_description_label.texture_update()

    def submit_callback(self):
        new_goal = classes.Goal()

        # getting input from ui
        new_goal.curriculum_name = None if len(self.ids.curriculum_name.text) == 0 else self.ids.curriculum_name.text
        new_goal.id = None if len(self.ids.goal_id.text) == 0 else int(self.ids.goal_id.text)
        new_goal.description = None if len(self.ids.goal_description.text) == 0 else self.ids.goal_description.text

        already_in_db = None
        already_in_db = self.app.client_model.get_goal(new_goal)

        curriculum_exists = None
        curriculum_exists = self.app.client_model.get_curriculum(new_goal.curriculum_name)

        if new_goal.curriculum_name is None or new_goal.id is None or new_goal.description is None:
            logging.info("NewGoalScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input.")
            dialogue.open()
        elif already_in_db is not None:
            logging.info("NewGoalScreenRoot: goal with id " +str(new_goal.id) + "already exists")
            dialogue = MessageDialogue(title="Entry error", message="Goal is already defined")
            dialogue.open()
        elif curriculum_exists is None:
            logging.info("NewGoalScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="DB error", message="The curriculum for this goal\ndoes not exist.")
            dialogue.open()
        else:
            # safe to enter into db
            self.app.client_model.set_goal(new_goal)
            self.ids.curriculum_name.text = ''
            self.ids.goal_id.text = ''
            self.ids.goal_description.text = ''
            self.app.screen_manager.transition.direction = 'right'
            self.app.screen_manager.current = 'main'
