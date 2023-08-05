"""
This package provides utilities for creating terminal GUIs (TUIs).

Classes
----------------
Window
    Inheritable class that permits recording (buffering) a terminal window's worth
    of strings and printing them to the console all at once.

Menu
    Utility class to use within a custom Window class. Permits the creation of a 
    list of menu options and tracks which option is selected.

TableMenu
    Utility class to use within a custom Window class. Permits the creation of a 
    list of menu options and tracks which option is selected. Can hold multiple
    selections in a set
"""