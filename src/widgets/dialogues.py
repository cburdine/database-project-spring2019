
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MessageDialogue(Popup):

    def __init__(self, title, message, dismiss_text='dismiss'):
        self.content = StackLayout(orientation='tb-lr')
        self.content.add_widget(Label(text=message, size_hint=(None, None), size=(272, 86), halign='center'))
        dismiss_button = Button(text=dismiss_text, size_hint=(None, None), size=(272, 20))
        self.content.add_widget(dismiss_button)
        Popup.__init__(self,title=title,
                            content=self.content,
                            size_hint=(None, None), size=(300, 170))
        dismiss_button.bind(on_press=self.dismiss)
