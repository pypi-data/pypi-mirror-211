class Window:
    """
Provides utilities for storing and printing one terminal-screen's worth of text. 
Intended to be an inherited class. 

When inheriting from `Window`, you may overload the `__init__` class. If you do,
be sure to include the line `self.new_buffer()` at the end of the
`__init__()` definition. You must also define self.window_height.

Methods in this module also implement logging from the `logging` library. To enable
logging, include the logging module in your project and run `self.do_logging()` in 
your __init__() definition. This module logs method calls and  prints them at the 
debug level.
    """

    window_height = 27
    """Defines the height of the window. May be overridden."""

    logs = False
    """Set to True (by calling self.do_logging()) to enable logging."""

    def __init__(self, window_height: int = 27):
        """
Initializes a new Window. If deriving from this class, define `self.window_height`
datamember and include the lines `self.new_buffer()` and (optionally) `self.do_logging()`
in your __init__() function.
        """
        
        self.window_height = window_height
        self.new_buffer()
        if self.logs: logging.debug(f"::easy_tui::Window - Initializing {self.__name__}")

    def do_logging(self):
        """Call to enable logging at the debug level."""
        self.logs = True

    def __repr__(self):
        """Prints the stored buffer to the console. Call after updating buffer."""
        return '\n'.join(self.buffer)

    def new_buffer(self):
        """
Creates a new buffer (`self.buffer`) with number of lines = `self.window_height`. 
Modify lines individually by accessing their index. 

e.g. 
```
>>> self.buffer[2] = "This is the third line in the screen"
>>> self.print()
·
This is the third line in the screen
·
·...(23 lines)
```

... Outputs a terminal screen's worth of lines. The third line contains the included
text.
        """
        if self.logs: logging.debug(f"::easy_tui::Window - Creating buffer of height {self.window_height} on {self.__name__}")
        self.buffer = ["" for _ in range(self.window_height)]

    def print(self):
        """Alternative to printing the Window with print(...)"""
        if self.logs: logging.debug(f"::easy_tui::Window - print() called on {self.__name__}")
        for line in self.buffer:
            print(line)

    def wipe(self):
        """Wipes each line of the buffer"""
        if self.logs: logging.debug(f"::easy_tui::Window - wipe() called on {self.__name__}")
        for i in range(self.window_height):
            self.buffer[i] = ""
        self.print()