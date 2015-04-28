#############################################################################################
#           File: screen.py                                                                 #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 7/3/15                                                             #
#############################################################################################

from config import screen_width, screen_height
import math
function = type(lambda x: x)
builtin = type(len)

class Screen():

    """simple GUI on a text based shell

    top-bar format:
    (left, middle, right):
    each a function with no arguments that returns a string, called each screen update
    if string 'notif' is given, a function that displays the number of notifications will be used

    width/height - window size (in characters)
    set to the config value by default

    notifications menu:
    notif_width - width of notifications menu in characters
    notif_events - list of functions without arguments, each returns a list of notifications
    events should make sure themselves not to return the same notification twice

    notification format: (<text>, <select to text>, <operation>)
    text(str) - notification description - printed in the menu
    select to text(str) - description of operation, printed 'select to ' + your text
    operation(function) - called when notification is chosen, get screen as argument, returns None

    prints only until the end of the screen, any left characters will not be printed
    < and > characters are used to scroll left and right 10 characters
    << and >> are used to scroll 25 characters
    the screen wont scroll off it's edge
    """

    __top_bar = [(lambda: ""), (lambda: ""), (lambda: "")]
    __width = 0
    __height = 0
    __shell = []
    __shell_cnt = 0
    __scroll = 0 # horizontal
    __notifications = []
    __notif_events = []
    __notif_width = 0 # will be 65 default

    def __init__(self, top_bar, notif_events, notif_width=65, width=screen_width, height=screen_height):

        if not isinstance(top_bar, tuple): raise TypeError("top_bar in invaild format, for details use help(Screen)")
        if not len(top_bar) == 3: raise ValueError("top_bar in invaild format, for details use help(Screen)")

        for component in range(3):
            if top_bar[component] == "notif": top_bar[component] = (lambda: "You have {0} notifications".format(len(self.__notifications)))

        if not isinstance(top_bar[0], (function, builtin)): raise TypeError("top_bar in invaild format, for details use help(Screen)")
        try:
            if not isinstance(top_bar[0](), str): raise TypeError()
        except TypeError: # will get here if top_bar[0] gets arguments or is not callable too
            raise TypeError("top_bar in invaild format, for details use help(Screen)")
        if not isinstance(top_bar[1], (function, builtin)): raise TypeError("top_bar in invaild format, for details use help(Screen)")
        try:
            if not isinstance(top_bar[1](), str): raise TypeError()
        except TypeError: # will get here if top_bar[1] gets arguments or is not callable too
            raise TypeError("top_bar in invaild format, for details use help(Screen)")
        if not isinstance(top_bar[2], (function, builtin)): raise TypeError("top_bar in invaild format, for details use help(Screen)")
        try:
            if not isinstance(top_bar[2](), str): raise TypeError()
        except TypeError: # will get here if top_bar[2] gets arguments or is not callable too
            raise TypeError("top_bar in invaild format, for details use help(Screen)")

        if not isinstance(width, int): raise TypeError("width must be int, for details use help(Screen)")
        if not isinstance(height, int): raise TypeError("height must be int, for details use help(Screen)")

        if not isinstance(notif_width, int): raise TypeError("notif_width must be int, for details use help(Screen)")
        if notif_width > width: raise ValueError("notif_width cannot be bigger than width")

        if not isinstance(notif_events, list): raise TypeError("notif_events in invaild format, for details use help(Screen)")
        for event in notif_events:
            if not isinstance(event, function): raise TypeError("notif_events in invaild format, for details use help(Screen)")

        self.__top_bar = top_bar
        self.__width = width
        self.__height = height
        self.__notif_events = notif_events
        self.__notif_width = notif_width
        self.__notifications = []
        self.reset()

    
    ## screen object's interface methods

    def reset(self, reset_scroll=True):

        """reset the current output, does not effect the shell until update() is called"""

        # the shell starts with empty strings as place holders to fill all the screen, each output override one of them
        # this mechanism is used to line the output to the top, and to clear the shell (sort of)
        self.__shell = [""]*(self.__height - 4) # -3 for top bar, -1 because the line count starts from 1
        self.__shell_cnt = 1 # to keep a blank line below top bar, this line should only be accessed by the notifications menu
        if reset_scroll: self.__scroll = 0

    def output(self, value=""):

        """add a line to the output, does not effect the shell until update() is called"""
        
        value = str(value)
        try:
            self.__shell[self.__shell_cnt] = value
            self.__shell_cnt += 1
        except IndexError:
            self.__shell.append(value)
            self.__shell_cnt += 1 # so next time there will be index error too

    def input(self):

        """get a string input from the shell, special characters wont be returned"""

        ans = input()
        
        if ans == "<":  # short scroll left
            self.__scroll = max(self.__scroll-10, 0)
            self.update()
            return self.input()
        
        if ans == "<<":  # long scroll left
            self.__scroll = max(self.__scroll-25, 0)
            self.update()
            return self.input()
        
        if ans == ">":  # short scroll right
            max_len = max(len(line) for line in self.__shell)
            self.__scroll = min(self.__scroll+10, max(max_len-self.__width, 0))
            self.update()
            return self.input()
        
        if ans == ">>":  # long scroll right
            max_len = max(len(line) for line in self.__shell)
            self.__scroll = min(self.__scroll+25, max(max_len-self.__width, 0))
            self.update()
            return self.input()

        if ans == "?": # open notifications menu
            self.notif()
            self.update()
            return self.input()
        
        return ans

    def update(self):

        """update the current output to the shell, does not effect output"""

        # top bar
        def mid_line():

            left =  "{0}{1}".format("|  {0:<30s}", " "*10)
            left = left.format(self.__top_bar[0]())
            mid = "{0}{1}".format("{1:<30s}", " "*10)
            mid = mid.format(self.__top_bar[1]())
            right = "{0}{1}{2}".format("{0:<25s}", " "*9, "|")
            right = right.format(self.__top_bar[2]())
            return "{{0}}{{1:^{0}}}{{2}}".format(self.__width-len(left)-len(right)).format(left, mid, right) # multiple formats strikes again

        print("\n{0}\n{1}\n{0}".format("-"*self.__width, mid_line()))

        print("\n".join([line[self.__scroll:self.__scroll+self.__width] for line in self.__shell])) # slicing is used to cut any characters off the edge



    ## notifications menu methods

    def __get_events(self):

        """check all notification-events, and update the notifications list"""

        self.__notifications += sum((event() for event in self.__notif_events), []) # hack the sum to work with lists :)
        

    def __print_notif(self, width, height_space):
        
        """update the output with the drop_down notifications menu shown, does not effect shell until update() is called

        width is the width in characters of the menu
        height_space is the space in characters between the menu ad the bottom of the screen
        the menu can go under it (and even below the bottom of the screen) if more space
        is needed for the options, but it wont go above it
        """

        def option_format(index, text, select_to, max_len, width):

            """like Menu_Node's format, but splitting lines, adding 'select to' line, and adding borders

            the text part will be splitted into number of lines if necessary, to fit in
            a width characters width drop_down menu
            same thing with select_to, which will start in the line below the text
            return a list of the lines
            """

            text_width = width - max_len - 7 # text without option id
            lines = fit_into(text, text_width) + fit_into("Select to " + select_to, text_width)
            lines = [lines[0]] + [" "*(max_len+3) + lines[line] for line in range(1, len(lines))] # indenting the lines to fit with the first
            lines[0] = "{{0:{0}}} - {1!s}".format(max_len, lines[0]).format(index) # formatting the first line with the option id
            lines = ["| {{0:{0}}} |".format(width-4).format(line) for line in lines] # adding borders
            lines += ["|" + " "*(width-2) + "|", "|" + "-"*(width-2) + "|"] # blank line + border
            return lines



        def fit_into(text, width, sep=" "):

            """split the text into number of lines to fit in width characters per line

            sep is the seperator between words, the option will only be splitted between words, unless a single word is longer than width
            return a list of the lines
            """

            lines = []
            words = text.split(sep)
            line = []

            for word in words:
                if (sum(len(i) for i in line) + len(sep)*len(line) + len(word)) > width:
                    if not line == []: lines += [sep.join(line)]
                    while len(word) > width: # in case a single word is too long
                        lines += [word[:width]]
                        word = word[width:]
                    line = [word]
                    continue
                
                line += [word]
            if not line == []: lines += [sep.join(line)]
            return lines


        # calculate the number of digits in the max id. this is used to line all the id's to the right on the end of the longest id
        digits = lambda x: math.floor(math.log10(x)) + 1 if x != 0 else 1
        max_id_len = digits(len(self.__notifications))

        lines = [] # before "blitting" on the screen
        if len(self.__notifications) == 0:
            lines = ["|" + " "*(width-2) + "|"]*5
            lines.append("| {{0:^{0}}} |".format(width-4).format("You have no unread notifications"))

        else:
            lines.append("|" + " "*(width-2) + "|")
            lines.append("| {{0:{0}}} - Mark all as read {{1:>{1}}}".format(max_id_len, width-max_id_len-22).format(0, "|"))
            lines.append("|" + " "*(width-2) + "|")
            lines.append("|" + "-"*(width-2) + "|")
            for notif in range(len(self.__notifications)):
                lines += option_format(notif+1, self.__notifications[notif][0], self.__notifications[notif][1], max_id_len, width)

        lines += ["|" + " "*(width-2) + "|"]*(self.__height - len(lines) - height_space - 4) # -3 for to bar, -1 for border line
        if lines[-1] == ("|" + " "*(width-2) + "|"): lines.append("|" + "-"*(width-2) + "|") # the if is to prevent it from doubleing the border

        # "blit" to the screen
        while len(self.__shell) < len(lines):
            self.__shell.append("") # making sure lines is not longer than shell
                                    # without it, an index error may occur
        for i in range(len(lines)):
            self.__shell[i] = "{{0:<{0}}}".format(self.__scroll+self.__width-width).format(self.__shell[i])
            self.__shell[i] = self.__shell[i][:self.__scroll+self.__width-width]
            self.__shell[i] += lines[i]


    def __notif_input(self):

        """handles input for the notifications menu

        only accepts vaild optionIDs and '?' to close the menu
        any other input is invaild and will be ignored
        if a vaild optionID is chosen, run the corresponding notification's operation
        if 0 is chosen, clear the notifications list
        return True if an option is chosen, False if '?' is chosen
        """

        while True:
            self.update()
            ans = input()
            if ans == "?": return False
            if not ans.isdecimal(): continue # invaild
            if int(ans) > len(self.__notifications): continue
            if ans == "0":
                if len(self.__notifications) == 0: continue # no options - invaild
                self.__notifications = []
                return True
            self.__notifications.pop(int(ans)-1)[2](self) # mark as read + run operation
            return True




    def notif(self, width=None, height_space=10):

        """open the notifications menu

        runs completly on its own, checks events, print the menu, and run actions
        based on user's input.
        after it closes, the screen will be restored to it's state before the menu started

        width is the width in characters of the menu, default is the width
        given in the initializing of the screen (if None is given)
        height_space is the space in characters between the menu ad the bottom of the screen
        the menu can go under it (and even below the bottom of the screen) if more space
        is needed for the options, but it wont go above it
        """

        if width is None: width = self.__notif_width
        if not isinstance(width, int): raise TypeError("width must be int")
        if width > self.__width: raise ValueError("width cannot be bigger than screen's width")
        if not isinstance(height_space, int): raise TypeError("height_space must be int")

        shell = list(self.__shell) # to restore later
        shell_cnt = self.__shell_cnt

        self.__get_events()

        self.__print_notif(width, height_space)
        while self.__notif_input():
            self.__shell = list(shell)
            self.__print_notif(width, height_space)

        self.__shell = list(shell)
        self.__shell_cnt = shell_cnt
            
        


notif_done_dict = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False}
def message_test(number):
    def returned(screen):
        screen.reset()
        screen.output("This is message " + str(number))
        screen.update()
        screen.input()
    return returned

notif_dict = {1: ("This is notification 1", "view message 1", message_test(1)), 2: ("This is notification 2", "view message 2", message_test(2)), 3: ("This is notification 3", "view message 3", message_test(3)), 4: ("This is notification 4", "view message 4", message_test(4)), 5: ("This is notification 5", "view message 5", message_test(5)), 6: ("This is notification 6", "view message 6", message_test(6)), 7: ("This is notification 7", "view message 7", message_test(7)), 8: ("This is notification 8", "view message 8", message_test(8))}

def event_test(number):
    def returned():
        if notif_done_dict[number]: return []
        notif_done_dict[number] = True
        return [notif_dict[number]]
    return returned


default_screen = Screen(((lambda: "left"), (lambda: "mid"), (lambda: "right")), [event_test(i) for i in range(1, 9)])
        





    
