from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
import time

class MessageDialogue(Popup):

    def __init__(self, title, message, dismiss_text='dismiss'):
        self.content = StackLayout(orientation='tb-lr')
        self.content.add_widget(Label(text=message, size_hint=(None, None), size=(272, 86), halign='center'))
        dismiss_button = Button(text=dismiss_text, size_hint=(None, None), size=(272, 20))
        self.content.add_widget(dismiss_button)
        Popup.__init__(self,title=title,
                            content=self.content,
                            size_hint=(None, None), size=(300, 170))
        dismiss_button.bind(on_release=self.dismiss)


class ConfirmDialogue(Popup):

    def __init__(self, title, message, true_handler=None, false_handler=None):
        self.outcome = None
        self.content = StackLayout(orientation='lr-tb', spacing=5)
        self.content.add_widget(Label(text=message, size_hint=(None, None), size=(272, 84), halign='center'))
        yes_button = Button(text='yes', size_hint=(None, None), size=(134, 20))
        no_button = Button(text='no', size_hint=(None, None), size=(134, 20))
        self.content.add_widget(yes_button)
        self.content.add_widget(no_button)
        Popup.__init__(self,title=title,
                            content=self.content,
                            size_hint=(None, None), size=(300, 170),
                            auto_dismiss=False)
        self.minimum_width = 272
        self.true_handler_func = true_handler if true_handler != None else self.dismiss_pass
        self.false_handler_func = false_handler if false_handler != None else self.dismiss_pass

        yes_button.bind(on_release=self.dismiss_true)
        no_button.bind(on_release=self.dismiss_false)

    def dismiss_true(self, *args):
        self.outcome = True
        self.dismiss()
        self.true_handler_func()

    def dismiss_false(self, *args):
        self.outcome = False
        self.dismiss()
        self.false_handler_func()

    def dismiss_pass(self):
        pass


class ProgressBarDialogue(Popup):

    def __init__(self, title, message):
        self.content = StackLayout(orientation='lr-tb')
        self.content.add_widget(Label(text=message, size_hint=(None, None), size=(272, 60), halign='center'))
        self.prog_bar = ProgressBar(max=100, size_hint=(None, None), size=(272, 40))
        self.prog_bar.value_normalized = 0.0
        self.content.add_widget(self.prog_bar)
        Popup.__init__(self, title=title,
                            content=self.content,
                            size_hint=(None, None), size=(300, 170),
                            auto_dismiss=False)

    def update_value(self, value):
        self.prog_bar.value_normalized = value



