#!usr/bin/python3

import kivy
kivy.require('1.0.7')
from kivy.lang.builder import Builder
from src.app import CurriculaApp

def main():
    # import/build .kv file:
    Builder.load_file('curricula.kv')
    CurriculaApp().run()


if __name__ == '__main__':
    main()
