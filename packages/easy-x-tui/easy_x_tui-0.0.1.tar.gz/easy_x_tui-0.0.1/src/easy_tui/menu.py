class Menu:
    """
Creates a simple "menu" object which may be used in your Windows.

To create a new menu, call `Menu(options)`, where `options` is a list of strings
that serve as menu items. 

Logging may be enabled on the debug level with `self.do_logging()`

Call `self.select_down()` and `self.select_up()` to change which item is selected.

See examples for implementation.

Attributes
----------
`self.options` - List of options.
`self.selection` - Index of current item.
    """

    logs = False
    def __init__(self, options: list, selection: int = 0):
        """
Initialize new menu. 

`options` - List of strings to serve as menu options.
`selection` - Menu item selected. Defaults to 0.
        """

        if self.logs: logging.debug("::easy_tui::Menu - Initialized")
        self.options = options 
        self.selection = selection
        self.num_options = len(self.options)

    def select_down(self):
        """Increments menu selection index with wrapping."""

        if self.logs: logging.debug("::easy_tui::Menu - select_down() called")
        self.selection = (self.selection + 1) % self.num_options

    def select_up(self):
        """Decrements menu selection index with wrapping."""

        if self.logs: logging.debug("::easy_tui::Menu - select_up() called")
        self.selection = (self.selection + (self.num_options - 1)) % self.num_options

    def do_logging(self):
        """Enable logging on object."""
        self.logs = True

class TableMenu:
    """
Creates a simple "menu" object, as above, which permits multiple selections. 
The index of a menu item may be added or removed 

Attributes
----------
`self.options` - List of options.
`self.selection` - Index of current item.
`self.selections` - Set of indices of all selected items.
    """

    logs = False
    def __init__(self, options: list, selection=0):
        if self.logs: logging.debug("::easy_tui::TableMenu - Initialized")
        self.options = options 
        self.selection: int = selection
        self.selections: set[int] = set()
        self.num_options = len(self.options)

    def select_down(self):
        """Increments menu selection index with wrapping."""

        if self.logs: logging.debug("::easy_tui::TableMenu - select_down() called")
        self.selection = (self.selection + 1) % self.num_options

    def select_up(self):
        """Decrements menu selection index with wrapping."""

        if self.logs: logging.debug("::easy_tui::TableMenu - select_up() called")
        self.selection = (self.selection + (self.num_options - 1)) % self.num_options
    
    def add_selection(self):
        """Adds selected item (index = self.selection) to list of selected items (self.selections)."""

        if self.logs: logging.debug(f"::easy_tui::TableMenu - selection added: {i}")
        self.selections.add(self.selection)
    
    def rm_selection(self):
        """
Removes selected item (index = self.selection) from list of selected items (self.selections).
Can throw KeyError if selected item is not in `self.selections` already.  
        """
        if self.logs: logging.debug(f"::easy_tui::TableMenu - selection removed: {i}")
        self.selections.remove(self.selection)