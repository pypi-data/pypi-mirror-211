# Easy-X-TUI

_Easy, Cross-platform TUI_

This lightweight package provides cross-platform utilities for creating terminal GUIs (TUIs).

[Read the documentation](https://stephenlf.github.io/easy-tui)

For lightweight GUIs, consider [easygui](https://pypi.org/project/easygui/).
For advanced, semantic terminal handling, consider [curses](https://docs.python.org/3/library/curses.html) from the standard library.

## Classes
---
### Window
Inheritable class that permits recording (buffering) a terminal window's worth of strings and printing them to the console all at once.

### Menu
Utility class to use within a custom Window class. Permits the creation of a list of menu options and tracks which option is selected.

### TableMenu
Utility class to use within a custom Window class. Permits the creation of a list of menu options and tracks which option is selected. Can hold multiple selections in a set