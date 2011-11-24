#This is a program to load a food list into memory.
#it works with my Rumford Soup program.
def loadfoodlist():

    f = open("ingredients.txt", "r")

    """ Okay, here's the deal:
    There's a list of ingredients called ingredients.
    an ingredient is a list which contains three elements; the first element
    is the name of the ingredient, the second element is the serving size of
    the ingredient (for a standard serving) and the third element is a list
    of nutrients within that ingredient.
    Basically, like this:
    ['Asparagus',[1.0, 'cup', 1.4, 'g'],[1.4, 1.5, 1.4] """

    ingredients = [] # this is just initializing the list.

    #this is the main loop.
    while 1:
        ingredient = [] # this is initializing the ingredient.

        while 1:
            line = f.readline()

            if line == '':
                break

            ingredient.append(line) #the first line is the name

            f.readline() # this line is useless

            serving = f.readline().split() #this stores the serving size
            mass = f.readline().split() #this stores the mass for later use

            f.readline() # this line is useless
            f.readline() # same here

            calories = f.readline().split() # Now the fun begins!

            # This line is important, I'm just trying to emphasize it.
            multiplier = 50 / float(calories[1]) #This is the multiplier 
                                          #to multiply to get a 50 calories
                                          #serving

            """ Okay, so the second element in an ingredient contains data 
            about a serving size for the ingredient.  it's a list which
            contains the mass and volume of a serving.   first element is
            volume, second element is units of volume, third element is mass,
            fourth element is units of mass.  So if a serving of lettuce were 
            1.5 cups, and that weighed 160 grams, it would be 
            [1.5, 'cup', 160, 'g'] """

            ingredient.append([float(serving[1]) * multiplier, serving[2], float(mass[2]) * multiplier, mass[3]])

            f.readline() # calories from fat; redundant.
            f.readline() # calories from saturated fat; again redundant.

            nutrients = [] # initializing the nutrients list

            #this loop goes through the file and loads the nutrients into a 
            #list.
            while 1:
                line = f.readline().split('\t')
                if line[0] == '\n':
                    break

                elif len(line) < 3:
                    continue

                elif line[2] == '%DV\n':
                    continue

                elif line[2] == '--\n':
                    nutrients.append(0)
                    #print(line[0])
                    continue

                nutrients.append(float(line[2]) * multiplier)
                #print(line[0])
                continue

            ingredient.append(nutrients)
            break

        if line == '':
            break

        ingredients.append(ingredient)

    #just for testing purposes.
    #print(ingredients)

    f.close
    return ingredients