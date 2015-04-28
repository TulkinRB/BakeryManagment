#############################################################################################
#           File: oper.py                                                                   #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 8/3/15                                                             #
#############################################################################################

"""
This file includes all the functions that act as operations in the menu system.
They will be passed as arguments to the menus' call method, and will be called when
corresponding option will be chosen
"""

import mysql.connector.cursor
import time
import interface.table
import interface.menu_tree

cursor = None
initted = False

def init(cur):

    """initialize the menu operations module"""

    global cursor, initted
    cursor = cur
    initted = True

def read_file(file):
    f = open(file)
    text = f.read()
    f.close()
    return text



    

def add_purchase(self): # self is the Menu_Node running the operation, it passes itself as argument, in case the operation is not 'leaf', but changing the menu.

    """add a purchase from customer to the Sales and SaleDetails tables"""

    if not initted:
        raise Exception("module not initialized")
    screen = self._Menu_Node__tree._Menu_Tree__screen # hack pythons private attributes
    cursor._connection.commit()
    cursor._connection.start_transaction()
    sql = ""
    ### get queries that adds new outcome and sale
    cursor.execute(sql, multi=True)
    ### get sql query that gets all products
    cursor.execute(sql)
    rows, product = interface.table.table(cursor, screen, menu=True)
    if product == 0: #go back
        cursor._connection.rollback()
        return
    screen.reset()
    screen.output("Enter Amount of {0}".format(product[1]))
    screen.update()
    amount = screen.input()
    screen.reset()
    screen.output("Enter Discount on {0}".format(product[1]))
    screen.update()
    discount = screen.input()
    ### get query to add product into purchase
    cursor.execute(sql, product[0], amount, discount)
    pass
    ## to complete

## products

def view_products(self): #### recipes
    sql = read_file("sql\\view_products.sql")
    screen = self._Menu_Node__tree._Menu_Tree__screen
    cursor.execute(sql)
    interface.table.table(cursor, screen)

def add_category(self):
    sql = read_file("sql\\add_category.sql")
    screen = self._Menu_Node__tree._Menu_Tree__screen
    screen.reset()
    screen.output("Enter Category Name")
    screen.update()
    name = screen.input()
    if len(name) > 25:
        screen.output("Name Can't Be Longer Than 25 Characters")
        while True:
            screen.update()
            name = screen.input()
            if len(name) <= 25: break
    screen.reset()
    screen.output("Enter a Description (You Can Leave It Blank)")
    screen.update()
    desc = screen.input()
    if len(desc) > 100:
        screen.output("Description Can't Be Longer Than 100 Characters")
        while True:
            screen.update()
            desc = screen.input()
            if len(desc) <= 100: break
    cursor.execute(sql, (name, desc))

def view_categories(self):
    sql = read_file("sql\\view_categories.sql")
    screen = self._Menu_Node__tree._Menu_Tree__screen
    cursor.execute(sql)
    interface.table.table(cursor, screen)

## products end


## ingredients

## supplies
    
def view_sppliers(self):
    sql = read_file("sql\\view_suppliers.sql")
    screen = self._Menu_Node__tree._Menu_Tree__screen
    cursor.execute(sql)
    interface.table.table(cursor, screen)

## supplies end

def view_ingredients(self):
    sql = read_file("sql\\view_ingredients.sql")
    screen = self._Menu_Node__tree._Menu_Tree__screen
    cursor.execute(sql)
    interface.table.table(cursor, screen)

## ingredients end

## view sales

def view_sales_this_month(self):
    ## get sql
    screen = self._Menu_Node__tree._Menu_Tree__screen
    cursor.execute(sql)
    interface.table.table(cursor, screen)
    
def view_sales_this_year(self):
    ## get sql
    screen = self._Menu_Node__tree._Menu_Tree__screen
    cursor.execute(sql)
    interface.table.table(cursor, screen)
    
def view_sales_spec_month(self):
    ## get sql
    screen = self._Menu_Node__tree._Menu_Tree__screen
    screen.output("Enter Month and Year, Seperated By '/'")
    while True:
        screen.update()
        ans = screen.input().split("/")
        if len(ans) != 2: continue
        if not ans[0].isdecimal(): continue
        if not ans[1].isdecimal(): continue
        if int(ans[0]) > 12: continue
        month, year = int(ans[0]), int(ans[1])
        break
    cursor.execute(sql, (month, year))
    interface.table.table(cursor, screen)
    
def view_sales_spec_year(self):
    ## get sql
    screen = self._Menu_Node__tree._Menu_Tree__screen
    screen.output("Enter Year")
    while True:
        screen.update()
        ans = screen.input()
        if not ans.isdecimal(): continue
        year = int(ans)
        break
    cursor.execute(sql, (year, ))
    interface.table.table(cursor, screen)
    
def view_sales_all_time(self):
    ## get sql
    screen = self._Menu_Node__tree._Menu_Tree__screen
    cursor.execute(sql)
    interface.table.table(cursor, screen)
    
