import kivy
kivy.require('1.10.1')
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.app import Widget
from src.model import classes
from kivy.metrics import dp
import logging
from src.widgets.dialogues import MessageDialogue
import os

FILE_DIR = os.path.dirname(os.path.realpath(__file__))


class EditCourseScreen(Screen):

    screen_name = 'edit_course'

    view_kv_filepath = 'edit_course_screen.kv'

    def __init__(self, root_app=None):
        Screen.__init__(self, name=self.screen_name)
        self.root_widget = Builder.load_file(os.path.join(FILE_DIR, self.view_kv_filepath))
        self.root_widget.link_to_app(root_app)
        self.add_widget(self.root_widget)

    def on_enter(self, *args):
        self.root_widget.populate()

class EditCourseScreenRoot(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.course = classes.Course()
        self.course_topics = {}  # indexed by topic id
        self.course_goals = {}  # indexed by goal id

    def link_to_app(self, app_ref):
        self.app = app_ref

    def populate(self):
        self.course = self.app.client_model._course_to_edit
        for ct in self.course.topics:
            ctopic = self.app.client_model.get_course_topic(ct, self.course.name)
            if ctopic:
                self.course_topics[ct] = self.app.client_model.get_topic(ctopic[1])
        for cg in self.course.goals:
            self.course_goals[cg] = self.app.client_model.get_context_free_goal(cg) # putting in context free goal here
        self.update_live_description_callback()

        self.ids.topics_list.setRows(self.course_topics.values())
        self.ids.sv_topics_list.height = self.ids.topics_list.get_height()

        self.ids.goals_list.setRows(self.course_goals.values())
        self.ids.sv_goals_list.height = self.ids.goals_list.get_height()

        self.ids.course_name.text = self.course.name

    def back_callback(self):
        self.ids.course_name.text = ''
        self.ids.subject_code.text = ''
        self.ids.credit_hours.text = ''
        self.ids.comment_1.text = ''
        self.app.screen_manager.transition.direction = 'down'
        self.app.screen_manager.current = 'course_dashboard'

    def remove_goal_callback(self):
        rem_goal = self.ids.goals_list.get_selected_row()
        if rem_goal is None:
            dialogue = MessageDialogue(title="Row Error",message="No row is selected.")
            dialogue.open()
        else:
            del self.course_goals[rem_goal.id]
            self.ids.goals_list.remove_selected_row()
            self.ids.sv_goals_list.height = max(dp(200), self.ids.goals_list.get_height(expected_node_height=2.0))

    def remove_topic_callback(self):
        rem_topic = self.ids.topics_list.get_selected_row()
        if rem_topic is None:
            dialogue = MessageDialogue(title="Row Error",message="No row is selected.")
            dialogue.open()
        else:
            del self.course_topics[rem_topic.id]
            self.ids.topics_list.remove_selected_row()
            self.ids.sv_topics_list.height = max(dp(200), self.ids.topics_list.get_height())
            self.populate()

    def add_topic_callback(self):
        topic_id_txt = self.ids.course_topic_id.text
        topic = None
        if len(topic_id_txt) > 0:
            topic = self.app.client_model.get_topic(int(topic_id_txt))
        else:
            topic_id_txt = None

        if topic is None:
            logging.info("NewCourseScreenRoot: could not find topic with id " + str(topic_id_txt))
            dialogue = MessageDialogue(title="Database Error",
                                       message="The Topic with id " + str(
                                           topic_id_txt) + "\ndoes not exist in the database.")
            dialogue.open()

        elif topic.id in self.course_topics.keys():
            logging.info("NewCourseScreenRoot: topic with id " + str(topic.id) + " already added.")
            dialogue = MessageDialogue(title="Topic Error",
                                       message="The Topic with id " + str(topic.id) +
                                               "\nhas already been added.")
            dialogue.open()
        else:
            self.course_topics[topic.id] = topic
            self.ids.topics_list.addRow(topic)
            self.ids.sv_topics_list.height = self.ids.topics_list.get_height()
            self.ids.course_topic_id.text = ''
            self.populate()

    def add_goal_callback(self):
        goal_id_txt = self.ids.course_goal_id.text
        if len(goal_id_txt) > 0:
            goal = self.app.client_model.get_context_free_goal(int(goal_id_txt))
        else:
            goal = None

        if goal is None:
            logging.info("NewCourseScreenRoot: Could not find goal with id " + str(goal_id_txt))
            dialogue = MessageDialogue(title="Database Error",
                                       message="The Goal with id " + str(goal_id_txt) +
                                               "\ndoes not exist in the database.")
            dialogue.open()
        elif int(goal_id_txt) in self.course_goals.keys():
            logging.info("NewCourseScreenRoot: goal with id " + str(goal_id_txt) + " already added.")
            dialogue = MessageDialogue(title="Goal Error",
                                       message="The Goal with id " + str(goal_id_txt) +
                                               "\nhas already been added.")
            dialogue.open()
        else:
            self.course_goals[int(goal_id_txt)] = goal
            self.ids.goals_list.addRow(goal)
            self.ids.sv_goals_list.height = self.ids.goals_list.get_height(expected_node_height=2.0)
            self.ids.course_goal_id.text = ''


    def update_live_description_callback(self):

        IND = "\n           "
        course_name = self.course.name if len(self.ids.course_name.text) == 0 else self.ids.course_name.text
        subj_code = self.course.subject_code if len(self.ids.subject_code.text) == 0 else self.ids.subject_code.text
        credit_hours = self.course.credit_hours if len(self.ids.credit_hours.text) == 0 else int(self.ids.credit_hours.text)
        comment_1 = self.course.description if len(self.ids.comment_1.text) == 0 else self.ids.comment_1.text.replace('\n', IND)
        course_topic_id = self.course_topics if len(self.ids.course_topic_id.text) == 0 else self.ids.course_topic_id.text
        course_goal_id = self.course_goals if len(self.ids.course_goal_id.text) == 0 else self.ids.course_goal_id.text

        description_label = []
        description_label.append(IND + f"[color=ffffff][size=40]Course: {course_name} [/size][/color]")
        description_label.append(IND + f"Subject Code: {subj_code}")
        description_label.append(IND + f"Credit Hours: {credit_hours}\n")
        description_label.append(IND + f"[color=ffffff][size=20]Description:[/size][/color]")
        if comment_1:
            description_label.append(IND + comment_1)

        self.ids.live_description_label.halign = 'left'
        self.ids.live_description_label.valign = 'top'
        self.ids.live_description_label.markup = True
        self.ids.live_description_label.text = ''.join(description_label)
        self.ids.live_description_label.texture_update()

    def submit_callback(self):
        new_course = classes.Course()

        # getting input from ui
        new_course.name = self.course.name if len(self.ids.course_name.text) == 0 else self.ids.course_name.text
        new_course.subject_code = self.course.subject_code if len(self.ids.subject_code.text) == 0 else self.ids.subject_code.text
        new_course.credit_hours = self.course.credit_hours if len(self.ids.credit_hours.text) == 0 else int(self.ids.credit_hours.text)
        new_course.description = self.course.description if len(self.ids.comment_1.text) == 0 else self.ids.comment_1.text
        new_course.topics = self.course_topics.keys()
        new_course.goals = self.course_goals.keys()

        # to validate
        #       name must not already be in db
        #       subject code and credit hours must be number


        db_course = self.app.client_model.get_course(new_course.name)

        if new_course.name is None:
            logging.info("NewCourseScreenRoot: some text fields lack input")
            dialogue = MessageDialogue(title="Format error", message="All fields must contain input")
            dialogue.open()
        elif db_course is None:
            logging.info("NewCourseScreenRoot: trying to edit something that's not there")
            dialogue = MessageDialogue(title="Database Error", message="Course is not already in the database.")
            dialogue.open()
        else:
            # can safely enter course into the db
            self.app.client_model.edit_course(new_course)
            dialogue = MessageDialogue(title="success", message="successfully stored tuple in the db")
            dialogue.open()
            self.ids.course_name.text = ''
            self.ids.subject_code.text = ''
            self.ids.credit_hours.text = ''
            self.ids.comment_1.text = ''
            self.app.screen_manager.transition.direction = 'down'
            self.app.screen_manager.current = 'course_dashboard'

    def remove_course_callback(self):

        self.app.client_model.remove_course_goals(self.course)
        self.app.client_model.remove_course_topics(self.course)
        self.app.client_model.remove_course_in_curriculum_listings(self.course)
        self.app.client_model.remove_course_in_section(self.course)
        self.app.client_model.remove_course_in_section_grades(self.course)
        self.app.client_model.remove_course_in_section_goal_grades(self.course)
        self.app.client_model.remove_course(self.course)
        self.app.client_model._course_to_edit = classes.Course()
        self.ids.course_name.text = ''
        self.ids.subject_code.text = ''
        self.ids.credit_hours.text = ''
        self.ids.comment_1.text = ''
        self.app.screen_manager.transition.direction = 'down'
        self.app.screen_manager.current = 'course_dashboard'
        dialogue = MessageDialogue(title="success", message="We removed the course from the db")
        dialogue.open()



