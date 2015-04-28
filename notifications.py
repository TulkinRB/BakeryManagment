#############################################################################################
#           File: notifications.py                                                          #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 7/3/15                                                             #
#############################################################################################

import mysql.connector.cursor

initted = False
cur = None

def read_file(file):
    f = open(file)
    text = f.read()
    f.close()
    return text



def init(cursor):

    """initialize notification events module"""

    if not issubclass(type(cursor), mysql.connector.cursor.CursorBase): raise TypeError("cursor must be a MySQL cursor")
    global cur, initted
    cur = cursor
    initted = True



sql_rotten_supplies_check = read_file("sql\\notif_rotten_suppplies_check.sql")
sql_rotten_supplies_oper = read_file("sql\\notif_rotten_suppplies_oper.sql")
rotten_supplies_set = set() # each member is

def rotten_supplies():

    cur.execute(sql_rotten_supplies_check)
    notifs = []
    for row in cursor:
        if (row[2], row[3])
        text = "The {0} from {1} became rotten.".format(row[0], row[1])
        select_to = "throw them away."
        def oper(screen):
            cur.execute(sql_rotten_supplies_oper, (row[2], row[3]))
        notifs.append((text, select_to, oper))
    return notifs
