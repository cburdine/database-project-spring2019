
from kivy.uix.textinput import TextInput
import re

class IntTextInput(TextInput):

    def __init__(self,**kwargs):
        super(IntTextInput, self).__init__(**kwargs)
        self.pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        s = re.sub(self.pat, '', substring)

        return super(IntTextInput, self).insert_text(s, from_undo=from_undo)

class IntListTextInput(IntTextInput):

    def __init__(self, **kwargs):
        super(IntListTextInput, self).__init__(**kwargs)
        self.pat = re.compile('[^0-9, ]')


