#!usr/bin/python3

from src.model.app import CurriculaApp
from src.model import edit_course_info

def main():
    # import/build .kv file:
    CurriculaApp().run()

if __name__ == '__main__':
    main()
