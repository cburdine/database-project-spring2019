import kivy
from src.view.main_screen import MainScreen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
kivy.require('1.10.1')

class CurriculaApp(App):

    def __init__(self):
        App.__init__(self)
        self.db_adapter = None
        self.screen_manager = ScreenManager()
        self.screen = MainScreen()


    def build(self):
        self.screen_manager.clear_widgets()
        self.screen_manager.add_widget(self.screen)

        return self.screen_manager

    def changeScreen(self, screen):
        print(screen)
