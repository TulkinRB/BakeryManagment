#############################################################################################
#           File: top_bar.py                                                                #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 2/3/15                                                             #
#############################################################################################

class Top_Bar():

    """The top-bar shown in Menu_Tree menu system

    The Menu_Tree initializer creates itself a top-bar object

    initializer format:
    left / middle/ right:

    a function with no arguments that returns a string
    called each screen update and the result is printed to it's position in the top-bar
    """

    def __init__(self, left, middle, right):

        if not isinstance(left, (function, builtin)): raise TypeError("left must be a function. for details use help(Top_Bar)")
        try:
            if not isinstance(left(), str): raise TypeError()
        except TypeError: # will get here if left gets arguments or is not callable too
            raise TypeError("left in invaild format. for details use help(Top_Bar)")
        if not isinstance(middle, (function, builtin)): raise TypeError("middle must be a function. for details use help(Top_Bar)")
        try:
            if not isinstance(middle(), str): raise TypeError()
        except TypeError: # will get here if middle gets arguments or is not callable too
            raise TypeError("middle in invaild format. for details use help(Top_Bar)")
        if not isinstance(right, (function, builtin)): raise TypeError("right must be a function. for details use help(Top_Bar)")
        try:
            if not isinstance(right(), str): raise TypeError()
        except TypeError: # will get here if right gets arguments or is not callable too
            raise TypeError("right in invaild format. for details use help(Top_Bar)")


        self.__left = left
        self.__middle = middle
        self.__right = right

    def __call__(self):

        def mid_line():

            left =  "{0}{1}{2}{1}".format("|  {0:<35s}", " "*10, "{1:<35s}")
            left = left.format(self.__left(), self.__middle())
            right = "{0}{1}{2}".format("{0:<30s}", " "*9, "|")
            right = right.format(self.__right())
            return "{{0}}{{1:>{0}}}".format(config.screen_width-len(left)).format(left, right) # multiple formats strikes again

        print("{0}\n{1}\n{0}\n".format("-"*config.screen_width, mid_line()))
