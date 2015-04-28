#############################################################################################
#           File: menu_tree.py                                                              #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 8/3/15                                                             #
#############################################################################################


import math
from . import screen as scrn # to avoid problems with same name for 2 vars

# found this way to get the class of None and functions
# i use this for isinstance checks
NoneType = type(None)
function = type(lambda x: x)
builtin = type(len)

class Menu_Tree():

    """a simple tree data structure"""

    __root = None
    __screen = None

    def __init__(self, tree_tup, screen):

        """initialize the tree object"""

        if not isinstance(tree_tup, tuple): raise TypeError("tree_tup must be a tuple representing the tree, for more info use help(Menu_Tree.parse)")
        if not isinstance(screen, scrn.Screen): raise TypeError("screen must be a Screen object")

        self.__root = self.parse(tree_tup)
        self.__screen = screen


    def parse(self, tree_tup):

        """parse a tree tuple to node objects. return the root node.

        tree_tup format(root node format):
        (<text(str)>, <call(function)>, [<child nodes(in same format)>])

        use help(Menu_Node) for node's operation and usage of these parameters
        """

        def internal(tree_tup, parent):

            if not isinstance(tree_tup, tuple): raise TypeError("tree_tup must be a tuple representing the tree, for more info and format use help(Menu_Tree.parse)")
            if not len(tree_tup) == 3: raise ValueError("tree_tup is not in correct format, use help(Menu_Tree.parse) for more info and correct format")
            if not isinstance(tree_tup[0], str): raise TypeError("tree_tup is not in correct format, use help(Menu_Tree.parse) for more info and correct format")
            if not isinstance(tree_tup[1], (function, builtin)): raise TypeError("tree_tup is not in correct format, use help(Menu_Tree.parse) for more info and correct format")
            if not isinstance(tree_tup[2], list): raise TypeError("tree_tup is not in correct format, use help(Menu_Tree.parse) for more info and correct format")

            new = Menu_Node(tree_tup[0], tree_tup[1], parent, self)

            for child in tree_tup[2]:
                internal(child, new)

            return new

        return internal(tree_tup, None)

    def main_loop(self):

        """start the menu system

        the main loop will operate until the user choose 'Quit Program' in the main menu.
        each menu will do its operation 'call method' and then prints the menu itself - leading to another menus
        """

        while self.__root():
            continue

    @property
    def _Menu_Node__screen(self): # so node objects can access __screen. for some reason python's private vars work like this
        return self.__screen
        


class Menu_Node():

    """a tree node used for the Tree class

    when called, executes an operation (call method) with self as parameter
    and then prints a menu (each child node is an option)
    the text attribute is what the parent menu will print in this menu's option
    tree is the Menu_Tree object leading tto the node
    if None is given - use parent's tree
    """

    __children = []
    __parent = None
    __text = ""
    
    def __init__(self, text, call, parent, tree=None):

        """initialize the Node object"""

        if not isinstance(parent, (Menu_Node, NoneType)): raise TypeError("Parent Node must be of type Menu_Node or None (for root node)")
        if not isinstance(text, str): raise TypeError("menu text must be string")
        if not isinstance(call, (function, builtin)): raise TypeError("call must be a function")
        if not isinstance(tree, (Menu_Tree, NoneType)): raise TypeError("node's tree must be a tree or None (to use parent's tree)")
        if parent is None and tree is None: raise ValueError("you cannot use parent's tree for root node")
        if parent is not None and tree is not None and tree is not parent.__tree: raise ValueError("node's tree must be parent's tree")

        self.__text = text
        self.__parent = parent
        self.__children = []
        self.call = call
        self.__tree = tree if tree is not None else parent.__tree

        if not self.__parent == None: self.__parent.add_child(self)


    def add_child(self, child):

        """add a child Node to this Node"""

        if not isinstance(child, Menu_Node): raise TypeError("child node must be of type Menu_Node")

        if not child in self.__children: self.__children.append(child)


##    def child(self, index):
##
##        """get child Node by index"""
##
##        if not isinstance(index, int): raise TypeError("index must be int")
##
##        try:
##            return self.__children[index]
##        except IndexError:
##            raise IndexError("child index out of range")

        
    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        if not isinstance(value, str): raise TypeError("menu text nust be string")
        self.__text = value







    def __call__(self, return_option=True):

        """run the menu

        operate the self.call function, then print the menu using self.print_menu(), and finally handle input
        any invaild input is ignored
        if return_option is False, no 'go back'/'quit program' option will be in the menu
        """

        # reset is done here and not inside print_menu so call can keep it's output when the menu get printed
        self.__tree.__screen.reset()
        # you set the 'call' in the init so you can't access the self argument
        # because of that, the call func get 2 self arguments, and uses the 2nd
        self.call(self)

        # menu stuff
        if len(self.__children) == 0: return True   # continue the while loop in the menu tree, to keep the program running
        self.print_menu()
        while True:
            self.__tree.__screen.update()
            ans = self.__tree.__screen.input()
            # handle input
            if not ans.isdecimal(): continue # invaild
            if int(ans) > len(self.__children): continue # invaild
            if int(ans) == 0 and self.__parent is None: return False # Quit Program chosen - False stops the while loop in the menu tree
            if int(ans) == 0: return self.__parent()
            return self.__children[int(ans)-1]()
            
        


    def print_menu(self, return_option):

        """print a text-based menu on the output screen.

        menu consists of multiple rows in the following format:

        <index(aligned to right, width determined by the max index)> - <text>'

        non-main menu starts with option '0 - Go Back' followed by a blank line

        screen used is menu tree's Screen object

        does not handle with input and choosing options, this function only prints to the screen the menu/
	"""

        def option_format(index, text, max_len):

            """return a menu option representation string in the following format:\n\n'<index(max_len chars width)> - <text>'"""

            # a way i found to set the length of a varible
            # basically you start with a format string that sets the length
            # and after format you get another format string, with a place holder
            # for the actual varible
            # i couldn't figure up a better way to get the length as a varible
            return "{{0:{0}}} - {1!s}".format(max_len, text).format(index)

        
        # calculate the number of digits in the max id. this is used to line all the id's to the right on the end of the longest id
        digits = lambda x: math.floor(math.log10(x)) + 1 if x != 0 else 1
        max_id_len = digits(len(self.__children)) if return_option else digits(len(self.__children)-1)
	
        # add a 'go back' option on the top if the menu is not a main menu, and a 'quit program' if it is
        if return_option:
            if self.__parent is not None:
            self.__tree.__screen.output(option_format(0, "Go Back", max_id_len))
            self.__tree.__screen.output() # blank line
        else:
            self.__tree.__screen.output(option_format(0, "Quit Program", max_id_len))
            self.__tree.__screen.output() # blank line
		
        # print all the options of the menu (child nodes)
        if return_option:
            for child in range(len(self.__children)):
                self.__tree.__screen.output(option_format(child+1, self.__children[child].text, max_id_len))
        else:
            for child in range(len(self.__children)):
                self.__tree.__screen.output(option_format(child, self.__children[child].text, max_id_len))
            






        
        




        

        
    
