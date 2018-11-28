import menu_maker as mm
#import menu_maker.menu_maker as mmm

# I found this with a macro calculator
nutr_req_daily = {'calories': 1800,
                  'carbs': 142 ,
                  'fat': 189,
                  'protein': 63 ,
                  'sodium': 2000 
                 }
# set a huge tolerance for now since my database is pretty empty
nutr_tol_daily = {'calories': (50000, 50000),
                  'carbs': (50000, 50000),
                  'fat': (50000, 50000),
                  'protein': (50000, 50000),
                  'sodium': (50000, 5000)
                 }

# make a daily meal plan
meal_plan = mm.make_daily_plan(nutr_req_daily, nutr_tol_daily, mm.meal_significance)

# spit it out 
print('\noutput meal plan:')
print(meal_plan)