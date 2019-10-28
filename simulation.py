import numpy as np
import random


# Width and height of the city grid
w, h = 10, 10

# Ratio of empty houses
empty_ratio = 0.1

# threshold for happiness
happy_threshold = 0.5

# number of ethnicities
number_ethnicities = 3
ratio_ethnicities = (.5, .3, .2) # sum must be 1
#ethnicity=('Dutch', 'German', 'Turkish')

# Initialize empty grids
city = np.zeros((w, h), dtype=object)
happiness = np.zeros((w,h), dtype=object)

#----------------ERRORS-----------------------
if len(ratio_ethnicities) != number_ethnicities:
    raise SyntaxError("l.17.   len(ratio_ethnicities) has to match number_ethnicities")
ratio_count = 0
for i in range(len(ratio_ethnicities)):
    ratio_count += ratio_ethnicities[i]
if ratio_count != 1:
    raise SyntaxError("l.18.   Sum of ratio_ethnicities has to be 1")


###-----------------FUNCTIONS---------------------

# measure agent happiness 
def happiness_measure(x,y):
    neighbours = 0
    same_ethnicity = 0
    if city[x,y] == 0:
        happiness[x,y] = 0
    else:
        for i in (-1,0,1):
            for j in (-1,0,1):
                if i==0 and j==0:
                    continue
                else:
                    neighbours += 1
                    if x+i not in range(0,w) or y+j not in range(0,h):
                        neighbours -= 1
                    else:
                        if city[x+i, y+j] == 0:
                            neighbours -=1
                        elif city[x,y] == city[x+i, y+j]:
                            same_ethnicity +=1  
                    if neighbours is 0:
                        happiness[x,y] = 2
                    else:
                        if same_ethnicity/neighbours >= happy_threshold:
                            happiness[x,y] = 1
                        else:
                            happiness[x,y] = 2

# measure happiness for the whole city                               
def city_happiness():
    for x in range(w):
        for y in range(h):
            happiness_measure(x,y)

#moving an individual 
def move_agent(x,y):
    if happiness[x,y] is 2:
        free = np.where(city == 0)
        freeX = free[0]
        freeY = free[1]
        empty_house = random.randint(0,len(free[1])-1)
        new_house = (freeX[empty_house], freeY[empty_house])
        city[new_house[0], new_house[1]] = city[x,y]
        city[x,y] = 0

        


###---------------START OF SIMULATION---------------------------
        
# create agents
number_agents = int(w*h*(1-empty_ratio))
agent_list = []
subgroup_counter = 1
for i in ratio_ethnicities:
    subgroup = i*number_agents
    for j in range(int(subgroup)):
        agent_list.append(subgroup_counter)
    subgroup_counter += 1
        
    
# randomly place agents on the grid
for i in agent_list:
    house = (random.randint(0,w-1), random.randint(0,h-1))
    while city[house[0], house[1]] is not 0:
        house = (random.randint(0,w-1), random.randint(0,h-1))
    if city[house[0], house[1]] is 0:
        city[house[0], house[1]] = i

# get initial city and happiness grids
print("INITIAL CITY")
print(city)
city_happiness()
print("INITIAL HAPPINESS")  
print(happiness)    
   
count = 0
#for i in range(10):
while 2 in happiness:
    x,y = random.randint(0, w-1), random.randint(0, h-1)
    city_happiness()
    move_agent(x, y)
    city_happiness()
    count += 1
    if (count % 500==0):# or count in range(1,10):
        print("city after " + str(count) + " iterations")
        print(city)
        print("happiness after " + str(count) + " iterations")
        print(happiness)
        print(count)
    
# print final city and happiness grids
print("Final City rached after " + str(count) + " iteration")
print(city)
print("Final Happiness")
print(happiness)
