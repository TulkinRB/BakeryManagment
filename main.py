#############################################################################################
#           File: main.py                                                       #
#           Created By: Tal Rojansky - tulkinrb@gmail.com                                   #
#           Last Update: 7/3/15                                                             #
#############################################################################################

import config
import database
import interface
import oper

conn, cursor = database.connect()

def get_money():

    """return the amount of money in account, as saved in database"""

    cursor.execute("SELECT * FROM Money")
    return cursor.fetchone()[0] + cursor.fetchone()[0]

top_bar = ((lambda: "Bakery Managment System " + config.version), "notif", (lambda: "Money in account: " + get_money()))
screen = interface.screen.Screen(top_bar, [])

a = ("", (lambda: pass), [

        ("Add a Purchase", (lambda: pass), []), ####
        ("Manage Products", (lambda: pass), [

            ("Add a New Baking", (lambda: pass), []), ####
            ("View Bakings", (lambda: pass), []), ####
            ("Add a New Product", (lambda: pass), []), ####
            ("Remove a Product", (lambda: pass), []), ####
            ("Throw Away Products", (lambda: pass), []), ####
            ("View Products", oper.view_products, []),
            ("Add a New Category", oper.add_category, []),
            ("Remove a Category", (lambda: pass), []), ####
            ("View Categories", oper.view_categories, [])

        ]),
        ("Manage Ingredients", (lambda: pass), [

            ("Place a New Order", (lambda: pass), []), ####
            ("View Orders", (lambda: pass), []), ####
            ("Manage Supplies", (lambda: pass), [

                ("Add a New Supply", (lambda: pass), []), ####
                ("Remove a Supply", (lambda: pass), []), ####
                ("Throw Away Supplies", (lambda: pass), []), ####
                ("View Supplies", (lambda: pass), []),
                ("Add a New Supplier", (lambda: pass), []), ####
                ("Remove a Supplier", (lambda: pass), []), ####
                ("View Suppliers", oper.view_suppliers, []) ####

            ]),
            ("Add a New Ingredient", (lambda: pass), []), ####
            ("Remove an Ingredient", (lambda: pass), []), ####
            ("View Ingredients", oper.view_ingredients, []) ####

        ]),
        ("Manage Money Reports", (lambda: pass), [

            ("View Sales", (lambda: pass), [

                ("From This Month", oper.view_sales_this_month, []),
                ("From This Year", oper.view_sales_this_year, []),
                ("From a Specific Month", oper.view_sales_spec_month, []),
                ("From a Specific Year", oper.view_sales_spec_year, []),
                ("From All-Time", oper.view_sales_all_time, [])

            ]),
            ("View Orders", (lambda: pass), []), ####
            ("View Incomes and Outcomes", (lambda: pass), []), ####
            ("Add an Income", (lambda: pass), []), ####
            ("Add an Outcome", (lambda: pass), []) ####

        ])

    ])




