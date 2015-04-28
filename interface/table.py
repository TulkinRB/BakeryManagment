#############################################################################################
#           File: table.py                                                                  #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 5/3/15                                                             #
#############################################################################################

from . import screen as scrn # to avoid problems with same name for 2 vars
import mysql.connector

def table(cursor, screen, menu=False, reset=True):
    
    """fetch all rows from cursor and print a table. return the rows

    user can press Enter (input an empty string) to continue
    the table will ignore any other input

    if menu is enabled, the table will act as a menu, and an option-ID column
    will be added to the left of the table.
    the function will return both rows list, and chosen row
    if go back option chosen, 0 will be returned instead of chosen row
    the table will ignore any input other than a vaild option-ID

    screen is the screen object printing to
    if reset is true the screen will be cleard before printing table
    """
    
    if not issubclass(type(cursor), mysql.connector.cursor.CursorBase): raise TypeError("cursor must be a MySQL cursor")
    if cursor.description is None: raise ValueError("cursor must have a result set")
    if not isinstance(screen, scrn.Screen): raise TypeError("screen must be a Screen object")
    
    # preparing the cells of the table

    title = [col[0] for col in cursor.description]
    try:
        rows = cursor.fetchall()
    except mysql.connector.errors.InterfaceError:
        raise ValueError("no unread results in cursor")
    if menu:
        title = [""] + title
        for row in range(len(rows)):
            rows[row] = (row+1, ) + rows[row]

    widths = [max(len(str(row[col])) for row in rows + [title]) for col in range(len(title))]
    row_width = sum(widths) + 3*len(widths) + 1

    # actual printing

    def row_format(*cols):

        row = " | ".join(["{{0:{0}}}".format(widths[col]).format(cols[col]) for col in range(len(cols))]) # with inner borders only
        row = ("| " + row + " |") # outer borders
        return row
        

    if reset: screen.reset()

    # title
    screen.output("-"*row_width)
    screen.output(row_format(*title))
    screen.output("-"*row_width)
    
    # go back option (if table is menu)
    if menu:
        # !! QUADRUPLE FORMAT !!    :)
        # same as the other duble fromats, this time the parameter is also a duble formatted string
        screen.output("{{0:<{0}}}|".format(row_width-1).format("| {{0:>{0}}} | Go Back ".format(widths[0]).format(0)))

    # rows
    for row in rows:
        screen.output(row_format(*row))
        
    screen.output("-"*row_width)
    screen.update()
    
    ans = screen.input()

    while True:
        if menu and ans == "0": return rows, 0
        if menu and ans.isdecimal() and int(ans) <= len(rows): return rows, rows[int(ans)-1]
        if not menu and ans == "": return rows
        screen.update()
        ans = screen.input()


