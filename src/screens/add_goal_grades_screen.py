import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import Widget
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

"""
This class represents the Enter Grades screen (This is an instance of a
kivy Screen object, which is managed by a ScreenManager in the app.py App class.
"""
class AddGoalGradesScreen(Screen):

    screen_name = 'add_goal_grades'

    view_kv_filepath = 'add_goal_grades_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(os.path.join(FILE_DIR + self.view_kv_filepath))
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)

    def on_enter(self, *args):
        self.root_widget.populate()

class AddGoalGradesScreenRoot(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.app = None
        self.course_selector = None

    # Ensure widgets are instantiated before calling this:
    def populate(self):
        rows = self.app.client_model.adapter.get_course_names()
        #topics = self.app.client_model.adapter.get_topics()

        # sort rows here...

        self.course_selector = self.ids.course_selector
        self.course_selector.setRows(rows)
        self.course_selector.set_callback(self.set_course_text_description)
        self.ids.sv_left.scroll_type = ['content', 'bars']
        self.ids.sv_left.bar_margin = dp(2)
        self.ids.sv_left.bar_width = dp(10)

        self.ids.sv_page.scroll_type = ['content', 'bars']
        self.ids.sv_page.bar_margin = dp(2)
        self.ids.sv_page.bar_width = dp(10)

        self.populated_sv = False

        # manually adjust height of selector box to fit unwrapped text:
        self.ids.sv_container.height = self.course_selector.get_height()

    def link_to_app(self, app_ref):
        self.app = app_ref

    def back_callback(self):
        self.app.screen_manager.transition.direction = 'right'
        self.app.screen_manager.current = 'main'

    def resize_callback(self, *args):
        if self.course_selector and self.course_selector.get_selected_row():
            Clock.schedule_once(self.set_course_text_description, 0.0)

    def set_topics_tree(self, course):
        self.ids.topics_tree.setRows(course.topics)
        self.ids.sv_topics.height = self.ids.topics_tree.get_height()

    def set_goals_tree(self, course):
        self.ids.goals_tree.setRows(course.goals)
        self.ids.sv_goals.height = self.ids.goals_tree.get_height()

    def set_course_text_description(self, *args):

        cur_name = self.course_selector.get_selected_row()
        if cur_name != None:
            # A str Builder object might be better to use later on:
            IND = "\n     "
            ENDL = "\n"
            """
            cur = self.app.client_model.get_curriculum(cur_name)
            for c in cur.cur_topics:
                c_topic = self.app.client_model.get_topic(c.topic_id)
                if c_topic is not None:
                    c._linked_topic_name = c_topic.name

            self.set_courses_trees(cur)
            self.set_topics_tree(cur)

            pane_size = dp(1100)
            self.ids.sv_description_container.height = pane_size

            description = []
            person = self.app.client_model.get_person(cur.id_in_charge)
            description.append(IND + f"[color=ffffff][size=40]{cur.name}[/size][/color]")
            description.append(IND + f"Minimum Credit Hours: {cur.min_credit_hours}")
            description.append(IND + f"Person in charge: {person.name} (id:{person.id})")
            """
            self.ids.description_field.halign = 'left'
            self.ids.description_field.valign = 'top'
            self.ids.description_field.markup = True
            self.ids.description_field.text = "DESCRIPTION"
            self.ids.description_field.texture_update()

            topic_tree_label_text = IND + "[size=28]Course Topics[/size]"
            self.ids.topic_tree_label.markup = True
            self.ids.topic_tree_label.text = topic_tree_label_text
            self.ids.topic_tree_label.texture_update()

            goal_tree_label_text = IND + "[size=28]Course Goals[/size]"
            self.ids.goal_tree_label.markup = True
            self.ids.goal_tree_label.text = goal_tree_label_text
            self.ids.goal_tree_label.texture_update()

