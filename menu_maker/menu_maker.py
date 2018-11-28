import menu_maker as mm
import apsw

def connect_to_db(dbfile):
    connection = apsw.Connection(mm.dbfile)
    return(connection.cursor())


def choose_meal(nutrition_reqs, nutrition_tol, meal_type, dbfile):
    '''Choose a suitable meal from the database.
    
    Inputs:
    nutrition_reqs: a dict of nutrition requirements for this meal
    nutrition_tol: a dict of nutrition tolerance for this meal 
    meal_type: str, can be breakfast, lunch, dinner, dessert, or snack
    
    Output: 
    meal: an object corresponding to the selected row of the recipes db
    '''
    # query the database for a random meal that meet the criteria 

    # connect to db
    cursor = connect_to_db(dbfile)

    '''
    query_out = cursor.execute("""SELECT * FROM recipes 
                               WHERE
                               (calories BETWEEN {} AND {})
                               AND (carbs BETWEEN {} AND {})
                               AND (fat BETWEEN {} AND {})
                               AND (protein BETWEEN {} AND {})
                               AND (sodium BEWEEN {} AND {})
                               AND (meal_type == {})
                               ORDER BY RANDOM()
                               LIMIT 1
                               """.format(nutrition_reqs['calories'], nutrition_tol['calories'][0],  nutrition_tol['calories'][1],
                                          nutrition_reqs['carbs'], nutrition_tol['carbs'][0],  nutrition_tol['carbs'][1],
                                          nutrition_reqs['fat'], nutrition_tol['fat'][0],  nutrition_tol['fat'][1],
                                          nutrition_reqs['protein'], nutrition_tol['protein'][0],  nutrition_tol['protein'][1],
                                          nutrition_reqs['sodium'], nutrition_tol['sodium'][0],  nutrition_tol['sodium'][1],
                                          meal_type
                                         ))
    '''

     # just calories for now
    query_out = cursor.execute("""SELECT * FROM recipes
                                  WHERE calories BETWEEN {} and {}
                                  ORDER BY RANDOM()
                                  LIMIT 1""".format(nutrition_tol['calories'][0],
                                                    nutrition_tol['calories'][1]))
   
    # choose a meal at random
    # TODO: later, a more sophisticated version of this could be done
    # choose in some non-random way

    meal = query_out.fetchall()
    return(meal)


def get_meal_nutrition(nutrition_reqs_daily, nutrition_tol_daily, meal_significance, meal_type):
    '''Define the goal nutrition requirements and tolerance for a given meal. 
    
    Inputs:
    nutrition_reqs_daily: a dict of nutrition requirements for this day
    nutrition_tol_daily: a dict of nutrition tolerance for this day 
    meal_significance: a dict of relative number of goal nutrients per meal
    meal_type: a string, can be "breakfast", "lunch", "dinner", "snack", or "dessert"
    
    Outputs:
    nutrition_reqs_meal: a dict of nutrition requirements for this meal
    nutrition_tol_meal: a dict of nutrition tolerance for this meal 
    '''
    nutrition_reqs_meal = {'calories': nutrition_reqs_daily['calories'] * meal_significance[meal_type],
                           'carbs': nutrition_reqs_daily['carbs'] * meal_significance[meal_type] ,
                           'fat': nutrition_reqs_daily['fat'] * meal_significance[meal_type],
                           'protein': nutrition_reqs_daily['protein'] * meal_significance[meal_type] ,
                           'sodium': nutrition_reqs_daily['sodium'] * meal_significance[meal_type] 
                          }
    # tuples with upper and lower tolerances
    nutrition_tol_meal = {'calories': (nutrition_reqs_meal['calories'] - nutrition_tol_daily['calories'][0]*meal_significance[meal_type],
                                       nutrition_reqs_meal['calories'] + nutrition_tol_daily['calories'][1]*meal_significance[meal_type]),
                          'carbs': (nutrition_reqs_meal['carbs'] - nutrition_tol_daily['carbs'][0]*meal_significance[meal_type],
                                    nutrition_reqs_meal['carbs'] + nutrition_tol_daily['carbs'][1]*meal_significance[meal_type]),
                          'fat': (nutrition_reqs_meal['fat'] - nutrition_tol_daily['fat'][0]*meal_significance[meal_type],
                                  nutrition_reqs_meal['fat'] + nutrition_tol_daily['fat'][1]*meal_significance[meal_type]),
                          'protein': (nutrition_reqs_meal['protein'] - nutrition_tol_daily['protein'][0]*meal_significance[meal_type],
                                      nutrition_reqs_meal['protein'] + nutrition_tol_daily['protein'][1]*meal_significance[meal_type]),
                          'sodium': (nutrition_reqs_meal['sodium'] - nutrition_tol_daily['sodium'][0]*meal_significance[meal_type],
                                     nutrition_reqs_meal['sodium'] + nutrition_tol_daily['sodium'][1]*meal_significance[meal_type]),
                         }
    
    return(nutrition_reqs_meal, nutrition_tol_meal)


def make_daily_plan(nutrition_reqs_daily, nutrition_tol_daily, meal_significance):
    '''Choose a suitable set of meals for the day from the database.
    
    Inputs:
    nutrition_reqs_daily: a dict of nutrition requirements for this day
    nutrition_tol_daily: a dict of nutrition tolerance for this day 
    meal_significance: a dict of relative number of goal nutrients per meal
    
    
    Outputs:
    meal_plan: dict corresponding to the selected row of the recipes db for
               each meal
    '''

    br_nutrition_reqs, br_nutrition_tol = get_meal_nutrition(nutrition_reqs_daily,
                                                             nutrition_tol_daily,
                                                             meal_significance,
                                                             meal_type='breakfast')
    lu_nutrition_reqs, lu_nutrition_tol = get_meal_nutrition(nutrition_reqs_daily,
                                                             nutrition_tol_daily,
                                                             meal_significance,
                                                             meal_type='lunch')
    di_nutrition_reqs, di_nutrition_tol = get_meal_nutrition(nutrition_reqs_daily,
                                                             nutrition_tol_daily,
                                                             meal_significance,
                                                             meal_type='dinner')
    sn_nutrition_reqs, sn_nutrition_tol = get_meal_nutrition(nutrition_reqs_daily,
                                                             nutrition_tol_daily,
                                                             meal_significance,
                                                             meal_type='snack')
    de_nutrition_reqs, de_nutrition_tol = get_meal_nutrition(nutrition_reqs_daily,
                                                             nutrition_tol_daily,
                                                             meal_significance,
                                                             meal_type='dessert')

    # now should update the tolerances between each meal so that the total is good
    meal_plan = {'breakfast': choose_meal(br_nutrition_reqs, br_nutrition_tol, 'breakfast', mm.dbfile),
                 'lunch': choose_meal(lu_nutrition_reqs, lu_nutrition_tol, 'lunch', mm.dbfile),
                 'dinner': choose_meal(di_nutrition_reqs, di_nutrition_tol, 'dinner', mm.dbfile),
                 'snack': choose_meal(sn_nutrition_reqs, sn_nutrition_tol, 'snack', mm.dbfile),
                 'dessert': choose_meal(de_nutrition_reqs, de_nutrition_tol, 'dessert', mm.dbfile)}

    return(meal_plan)