import kivy
from src.screens.main_screen import MainScreen
from src.screens.login_screen import LoginScreen
from src.screens.curriculum_dashboard_screen import CurriculumDashboardScreen
from src.screens.add_new_screen import AddNewScreen
from src.screens.curriculum_dashboard_screen import CurriculumDashboardScreen
from src.screens.new_curriculum_screen import NewCurriculumScreen
from src.screens.new_goal_screen import NewGoalScreen
from src.screens.new_topic_screen import NewTopicScreen
from src.screens.topic_already_exists_screen import TopicAlreadyExistsScreen
from src.screens.all_fields_must_contain_input_screen import AllFieldsMustContainInputScreen
from src.screens.topic_id_must_be_numeric_screen import TopicIdMustBeNumericScreen
from src.screens.new_person_screen import NewPersonScreen
from src.screens.success_screen import SuccessScreen
from src.screens.new_course_screen import NewCourseScreen
from src.screens.subject_code_must_be_numeric_screen import SubjectCodeMustBeNumericScreen
from src.screens.credit_hours_must_be_numeric_screen import CreditHoursMustBeNumericScreen
from src.screens.course_already_exists_screen import CourseAlreadyExistsScreen
from src.screens.new_section_screen import NewSectionScreen
from src.screens.unit_id_must_be_numeric_screen import UnitIdMustBeNumericScreen
from src.screens.num_students_must_be_numeric_screen import NumStudentsMustBeNumericScreen
from src.screens.course_does_not_exist_in_database_screen import CourseDoesNotExistScreen
from src.screens.section_already_exists_screen import SectionAlreadyExistsScreen
from src.db.adapter import DBAdapter
from src.model.client_model import ClientModel
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.app import App
kivy.require('1.10.1')

class CurriculaApp(App):

    def __init__(self):
        App.__init__(self)
        self.db_adapter = DBAdapter()
        self.screen_manager = ScreenManager()
        self.client_model = ClientModel(self.db_adapter)


    def build(self):
        self.screen_manager.clear_widgets()
        screen_list = []
        screen_list.append(LoginScreen(root_app=self))
        screen_list.append(MainScreen(root_app=self))
        screen_list.append(CurriculumDashboardScreen(root_app=self))
        screen_list.append(AddNewScreen(root_app=self))
        screen_list.append(NewCurriculumScreen(root_app=self))
        screen_list.append(NewPersonScreen(root_app=self))
        screen_list.append(NewGoalScreen(root_app=self))
        screen_list.append(NewTopicScreen(root_app=self))
        screen_list.append(TopicAlreadyExistsScreen(root_app=self))
        screen_list.append(AllFieldsMustContainInputScreen(root_app=self))
        screen_list.append(TopicIdMustBeNumericScreen(root_app=self))
        screen_list.append(SuccessScreen(root_app=self))
        screen_list.append(NewCourseScreen(root_app=self))
        screen_list.append(SubjectCodeMustBeNumericScreen(root_app=self))
        screen_list.append(CreditHoursMustBeNumericScreen(root_app=self))
        screen_list.append(CourseAlreadyExistsScreen(root_app=self))
        screen_list.append(NewSectionScreen(root_app=self))
        screen_list.append(UnitIdMustBeNumericScreen(root_app=self))
        screen_list.append(NumStudentsMustBeNumericScreen(root_app=self))
        screen_list.append(CourseDoesNotExistScreen(root_app=self))
        screen_list.append(SectionAlreadyExistsScreen(root_app=self))

        for screen in screen_list:
            self.screen_manager.add_widget(screen)

        return self.screen_manager

    def changeScreen(self, screen):
        print(screen)

