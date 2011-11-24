#! /usr/bin/env python

#Ned's rumford soup recipe.
#An evolutionary algorithm to find a cheap, nutritious soup.


#recipe is a list of ingredients
#each ingredient is a number of a food
#of vitamins and minerals
def Nutrition(recipe, foodlist):

    #initializing a nutrient list
    nutrients = [0] * 36

    #a loop to add up the nutrients in the recipe to the nutrient list
    for ingredient in recipe:
        for i in range(36):
            nutrients[i] = nutrients[i] + foodlist[ingredient][2][i]

    #adjusting the protein so that protein = 20% of calories
    nutrients[0] = nutrients[0] * 0.625
    #zeroing out saturated fat -- don't want too much saturated fat.
    nutrients[4] = 0
    #adjusting fat so that fat = 30% of calories
    nutrients[3] = nutrients[3] * 1.21875
    #zeroing out mono and poly fats for now; gonna do more research.
    nutrients[5] = 0
    nutrients[6] = 0
    #adjusting carbs so that 50% of calories come from carbs.
    nutrients[1] = nutrients[1] * 1.5
    #zeroing out cholesterol; don't want too much of that, either.
    nutrients[7] = 0
    #zeroing out sodium; shouldn't be a problem with a salt shaker.
    nutrients[34] = 0

    #initialize the 'Score' variable
    score = 0

    #adding up all of the nutrients to come up with a 'score' variable.
    #at this point the nutrition function is very crude; will work more later.
    for nutrient in nutrients:
        
        #If there's more than 100%DV of a nutrient, just report it as 100.
        #otherwise, a recipe with a ridiculous amount of vitamin c may be
        #selected, even if it's deficient in other nutrients
        if nutrient > 100:
            score = score + 100
        else:
            score = score + nutrient
    return score

def Sex(parent1, parent2, number):

    #needs to use a random choice
    #from random import choice, random
    
    #The child is the product of a night of passionate sex between two parents.
    child = []

    #This loop picks a chromosome from either the father or the mother.
    for i in range(32):
        child.append(choice([parent1[i],parent2[i]]))

    #this is a mutation
    if random() < 0.05:
        child[randrange(32)] = randrange(number)

    #return the child list.
    return child


#this is loading the food list.
from loadingredients import loadfoodlist
foodlist = loadfoodlist()

#this is creating the seed population, a list of 4,000 random recipes
from random import choice, randrange, random
recipes = []

for i in range(4000):
    recipe = []
    for j in range(32):
        recipe.append(randrange(len(foodlist)))
    recipe.append(Nutrition(recipe,foodlist))
    recipes.append(recipe)

print("there is a random list of recipes")

#Yay!  I'm here at selection.  Here's the tricky part.  I'm using tournament
#selection.  The tournament contains 4 recipes.  It should be good.

parent1 = [0]*33
parent2 = [0]*33
newrecipes = [0]*4000
tournamentrecipes = [0]*8

#100 generations, for now
for i in range(100):

    print('Generation '+str(i))
    
#this will determine if the highest nutrition (3500) is there; if so it will
#break -- this is fairly expensive so I'm commenting it out -- in roulette
#wheel selection it never is anyway.
#    kingdawg = [0]*33
#    for recipe in recipes:
#        if recipe[32] > kingdawg[32]:
#            kingdawg = recipe

#    if kingdawg[32] >= 3500:
#        break

#this wasn't working for some reason, trying a different way.    
#    for recipe in recipes:
#        recipe.append(Nutrition(recipe, foodlist))

#    print('recipes should be 33 long')

    #god, this is ugly.  Oh well, it's just a first draft.
#    for i in range(0, 4000, 4):
#        if Nutrition(recipes[i], foodlist) > Nutrition(recipes[i+1], foodlist):
#            parent1 = recipes[i]
#        else:
#            parent1 = recipes[i+1]
#        if Nutrition(recipes[i+2], foodlist) > Nutrition(recipes[i+3], foodlist):
#            parent2 = recipes[i+2]
#        else:
#            parent2 = recipes[i+3]
#        newrecipes.append(Sex(parent1, parent2))
#        newrecipes.append(Sex(parent1, parent2))
#        newrecipes.append(Sex(parent1, parent2))
#        newrecipes.append(Sex(parent1, parent2))
#    recipes = newrecipes
#    
#   Trying a proper tournament selection (may slow things down, though.)
#    for i in range(4000):
#        #creating a list of recipes for the tournament.
#        for j in range(8):
#            tournamentrecipes[j] = (choice(recipes))
#        parent1 = [0]*33
#        parent2 = [0]*33
#        #Deathmatch:  8 recipes enter; two recipes leave.
#        for j in range(0,8,2):
#            if tournamentrecipes[j][32] > parent1[32]:
#                parent1 = tournamentrecipes[j]
#            if tournamentrecipes[j+1][32] > parent2[32]:
#                parent2 = tournamentrecipes[j+1]
#        
#        newrecipes[i] = Sex(parent1, parent2, len(foodlist))
#        newrecipes[i].append(Nutrition(newrecipes[i],foodlist))
#    recipes = newrecipes

#   Trying roulette wheel selection -- a little unsure about this, but let's
#   give it a whirl.

#this adds up the total fitness
    totalselection = 0

    #I'm adding a lowest recipe loop to determine optimum variance.
    betamax = [3500]*33
    for recipe in recipes:
        if recipe[32] < betamax[32]:
            betamax = recipe

    selectionvariance = betamax[32] - 250


    for recipe in recipes:
        #subtracting 2000 because there may not be enough variance
        #fitness function -- quick and dirty way to get variance.
        totalselection = totalselection + (recipe[32] - selectionvariance)

    for i in range(4000):
        roulettescore = random() * totalselection
        selection = 0
        for recipe in recipes:
            selection = selection + (recipe[32] - selectionvariance)
            if selection >= roulettescore:
                parent1 = recipe
                break

        roulettescore = random() * totalselection
        selection = 0
        for recipe in recipes:
            selection = selection + (recipe[32] - selectionvariance)
            if selection >= roulettescore:
                parent2 = recipe
                break

        newrecipes[i] = Sex(parent1, parent2, len(foodlist))
        newrecipes[i].append(Nutrition(newrecipes[i], foodlist))
    recipes = newrecipes
#now I'm at a really tricky part.  I intend to print the highest scoring
#recipe, but I'm not quite sure how to do that.  The recipes are just a list
#of numbers
#it's ugly, but I guess I'll just append the score to the end of the recipe.
#now, a recipe has 33 numbers, 32 ingredients and a score.
#trying this earlier in the program.
#for recipe in recipes:
#    recipe.append(Nutrition(recipe, foodlist))

#moving this to inside the loop for an end function; leaving it here for
#historical interest.
#selecting and displaying the most nutritious recipe.
kingdawg = [0]*33
for recipe in recipes:
    if recipe[32] > kingdawg[32]:
        kingdawg = recipe

#finding the 10 most nutritious recipes.
#will use this later.
from operator import itemgetter
kingdawgs = [0]*10
for i in range(10):
    kingdawgs[i] = [0]*33

for recipe in recipes:
    if recipe[32] > kingdawgs[9][32]:
        kingdawgs[9] = recipe
    kingdawgs.sort(reverse=True, key=itemgetter(32))

#g = open("recipes","w")
#g.write(

#Sorting it makes it easier to read, but I may want to do something else later.
kingdawg.sort()

for i in range(32):
    print(foodlist[kingdawg[i]][0][:-1])
