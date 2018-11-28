import apsw  # that was a bitch to install; only works with python 3 on my machine
import numpy as np
import pandas as pd

from .menu_maker import *

# a list of submodules, if I make them, so I can do 
# from menu_maker import *
__all__ = ['menu_maker']

# set up important variables
# location of recipes database
dbfile = "/Users/brittanyhoward/Desktop/menu_maker/recipes_db/recipes.db"

######## preferences ###########
# change this according to personal preferences
meal_significance = {'breakfast': 0.2,
                    'lunch': 0.25,
                    'dinner': 0.3,
                    'snack': 0.125,
                    'dessert': 0.125
                    }
assert(np.sum(list(meal_significance.values())) == 1.)