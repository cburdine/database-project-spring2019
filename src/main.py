#!usr/bin/python3

from src.model.app import CurriculaApp
from src.model.enter_new_curriculum import enter_new_curriculum

def main():
    # import/build .kv file:
    CurriculaApp().run()

if __name__ == '__main__':
    main()
