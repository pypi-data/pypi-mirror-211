def window_example():
    """Example of the Window class"""

    from window import Window
    from os import system

    WINDOW_HEIGHT = 27
    WINDOW_WIDTH = 140 

    class Example(Window):
        def __init__(self):
            self.window_height = WINDOW_HEIGHT
            self.new_buffer()   # Creates a new datamember: self.buffer.

            self.buffer[0] = "This is the first line"
            self.buffer[1] = "This is the second line"
            self.buffer[2] = "================================="
            self.buffer[3] = "..."
            self.buffer[-1] = "This is the last line. Press [ENTER] to continue"
    
        def update_buffer_once(self):
            self.buffer[7] = "This is an updated line"
            self.buffer[8] = "Notice that we only have to mess with the lines that are changing"

        def update_buffer_twice(self):
            self.wipe()
            self.buffer[8] = "Everything was wiped!!!"
    
    system(f"mode {WINDOW_WIDTH}, {WINDOW_HEIGHT+1}")   # Sets the terminal window size.
                                                        # Works better in a self-contained terminal window (not code editor)
    w = Example()

    print(w)
    input()

    w.update_buffer_once()
    print(w)
    input()
    
    w.update_buffer_twice()
    print(w)
    input()

def window_with_menu_example():
    """Example of the Menu class implemented on a custom Window instance"""

    from window import Window
    from menu import Menu
    from os import system

    WINDOW_HEIGHT = 27
    WINDOW_WIDTH = 140 

    class Example(Window):
        def __init__(self):
            self.window_height = WINDOW_HEIGHT
            self.new_buffer()   # Creates a new datamember: self.buffer.

            self.menu = self.init_menu()

            self.buffer[0] = "Example Window. See options below."
            self.buffer[1] = "=================================="
            self.buffer[2] = ""

            self.buffer_menu()

            self.buffer[-2] = 'Enter selection. Type "up", "down", or "exit"'
    
        def init_menu(self):
            menu_options = [
                "This is option idx = 0",
                "This is option idx = 1",
                "This is option idx = 2"
            ]
            return Menu(menu_options)
        
        def buffer_menu(self):
            for i in range(len(self.menu.options)):
                if self.menu.selection == i:
                    self.buffer[i+3] = f"[X] {self.menu.options[i]}"
                else:
                    self.buffer[i+3] = f"[ ] {self.menu.options[i]}"
        
        def select_up(self):
            self.menu.select_up()
            self.buffer_menu()
        
        def select_down(self):
            self.menu.select_down()
            self.buffer_menu()

    w = Example()
    print(w)

    while(True):
        i = input()
        if i.lower() == "exit":
            break
        elif i.lower() == "up":
            w.select_up()
            print(w)
            continue
        elif i.lower() == "down":
            w.select_down()
            print(w)
            continue
        print(w)

def window_with_table_menu_example():
    """Example of the TableMenu class implemented on a custom Window instance"""

    from window import Window
    from menu import TableMenu
    from os import system

    WINDOW_HEIGHT = 27
    WINDOW_WIDTH = 140 

    class Example(Window):
        def __init__(self):
            self.window_height = WINDOW_HEIGHT
            self.new_buffer()   # Creates a new datamember: self.buffer.

            self.menu = self.init_menu()

            self.buffer[0] = "Example Window. See options below."
            self.buffer[1] = "=================================="
            self.buffer[2] = ""

            self.buffer_menu()

            self.buffer[-2] = 'Enter selection. Type "up", "down", "add", "remove", or "exit"'
    
        def init_menu(self):
            menu_options = [
                "This is option idx = 0",
                "This is option idx = 1",
                "This is option idx = 2"
            ]
            return TableMenu(menu_options)
        
        def buffer_menu(self):
            for i in range(len(self.menu.options)):
                if i == self.menu.selection: 
                    self.buffer[i+3] = 'X '
                else:
                    self.buffer[i+3] = '  '

                if i in self.menu.selections:
                    self.buffer[i+3] += f"[*] {self.menu.options[i]}"
                else:
                    self.buffer[i+3] += f"[ ] {self.menu.options[i]}"
        
        def select_up(self):
            self.menu.select_up()
            self.buffer_menu()
        
        def select_down(self):
            self.menu.select_down()
            self.buffer_menu()
        
        def add_selection(self):
            self.menu.add_selection()
            self.buffer_menu()
        
        def remove_selection(self):
            self.menu.rm_selection()
            self.buffer_menu()

    w = Example()
    print(w)

    while(True):
        i = input()
        if i.lower() == "exit":
            break
        elif i.lower() == "up":
            w.select_up()
            print(w)
            continue
        elif i.lower() == "down":
            w.select_down()
            print(w)
            continue
        elif i.lower() == "add":
            w.add_selection()
            print(w)
            continue
        elif i.lower() == "remove":
            w.remove_selection()
            print(w)
            continue
        print(w)