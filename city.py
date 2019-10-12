import random
import sys

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from agent import Agent, RealNumberFeature, BinaryFeature, CategoricalFeature, Religion, religion_preference_matrix

# Max iterations
max_iterations = 50
satisfaction_threshold = 0.9
agent_satisfaction_threshold = 0.3

# Width and height of the city grid
w, h = 16, 16

# Min and max prices of homes
min_price = 10000
max_price = 1000000

# Min/max income of residents
min_income = 100
max_income = 100000

# if 0 - price will not have any noise
# if 1 - price will fluctuate with values between 0 and max_price
price_noise = 0.3

# weight of extreme prices, if 0 prices will be evenly distributed
price_segregation = 0.1

# Importance of religion, ethnicity and income respectively for each agent
## sum should be = 1
weight_list = [.1, .8, .1]

# Ratio of empty houses
empty_ratio = 0.05

# how much to zoom in on the picture before displaying, please use integer for good results
zoom = 10

check_future_home = False


class Home:
    def __init__(self, price, address, empty: bool, occupant: Agent):
        self.price = price
        self.address = address
        self.empty = empty
        self.occupant = occupant

    def __str__(self):
        return str(self.price)


def neighbors(a, rowNumber, columnNumber, radius): # parameter order was incorrect
    return [[a[i][j] if 0 <= i < len(a) and 0 <= j < len(a[0]) else None
             for j in range(columnNumber - 1 - radius, columnNumber + radius)]
            for i in range(rowNumber - 1 - radius, rowNumber + radius)]


def generate_city():
    #print("hello")
    # City is a matrix with a padding
    grid = np.zeros((w + 2, h + 2), dtype=object)
    for x in range(-2, w + 2):
        for y in range(-2, h + 2):
            # These are 2 rows/columns that will not show in the bitmap,
            # but we will use them to generate the first row/column
            if x < 0 or y < 0 or x >= w or y >= h:
                price = random.randint(min_price, max_price)
            # Average some neighboring houses then add noise
            else:
                price = np.average([grid[x][y - 1].price, grid[x][y - 2].price,
                                    grid[x - 1][y].price, grid[x - 2][y].price,
                                    grid[x - 1][y + 1].price, grid[x - 2][y + 1].price])
                price = price + random.randint(-price_noise * max_price, price_noise * max_price)

                # Noise may have made price above max, limit it to the [0, max_price] interval
                if price > max_price:
                    price = max_price
                elif price < 0:
                    price = 0

            # Move all values toward 0 and max_price a bit, depending on which they are closer to
            # Do a weighted average - price_segregation is the weight of the endpoints
            if price < max_price / 2:
                price = price / (1 + price_segregation)
            else:
                price = (price + max_price * price_segregation) / (1 + price_segregation)

            # 1 in 10 probability of an empty house
            empty = random.randint(1, 1 / empty_ratio) == 1

            if not empty:
                # Creating a random agent that lives in that home
                eth = (random.randint(1, 2) == 1)
                a = Agent(religion=CategoricalFeature(value=random.randint(1, 9),
                                                      preference_matrix=religion_preference_matrix),
                          ethnicity=BinaryFeature(value=eth),
                          income=RealNumberFeature(value=random.randint(min_income, max_income), threshold=30000),
                          weights=weight_list)
               # print("agent: ", a.ethnicity.value)
            else:
                a = None
            # Generating a home with a price depending on its location and its address
            grid[x][y] = Home(price=price, address=(x, y), empty=empty, occupant=a)
    return grid

###----------------------------------------------------
def happiness(x, y, city, radius, agent):

    neighbour_count = 0
    ethnicity_satisfaction = 0
    religion_satisfaction = 0
    income_satisfaction = 0
    neighboring_houses = flatten(neighbors(city, x, y, radius))
    neighboring_houses = list(filter(None.__ne__, neighboring_houses))
    house_neighbors = []
    for hs in neighboring_houses:
        if not agent == hs.occupant:
            if not hs.empty:
                neighbour_count += 1
                #non-binary, use preference matrix
                religion_satisfaction += int(religion_preference_matrix[agent.religion.value-1][hs.occupant.religion.value-1])
                #binary, so just add up all matches
                if agent.ethnicity.value == hs.occupant.ethnicity.value:
                    ethnicity_satisfaction += 1
                #continuous, use difference
                income_satisfaction += min(agent.income.value, hs.occupant.income.value) / max(agent.income.value, hs.occupant.income.value)
                house_neighbors.append(hs.occupant)
    #no neighbours leads to total dissatisfaction
    if neighbour_count == 0:
        total_satisfaction = 0
    else:
        #TODO: maybe we need different ways to measure individual happiness scores
        religion_score = religion_satisfaction / neighbour_count
        ethnicity_score = ethnicity_satisfaction / neighbour_count    
        income_score = income_satisfaction / neighbour_count
        total_satisfaction = religion_score* weight_list[0] + ethnicity_score*weight_list[1] + income_score*weight_list[2]
    #print("total: ", total_satisfaction)
    return total_satisfaction
    
def time_step(i):
    if i % 100 == 0:
        print(i)
    city_satisfactions = []
	#happy = happiness_measure()
    # Go through the entire city to check whether occupants are satisfied
    for (x, y), house in np.ndenumerate(city):
        # Skip edge for now
        if not house.empty:
            agent = house.occupant
            satisfaction = happiness(x,y,city, 1, agent)
            if satisfaction <= agent_satisfaction_threshold:
                city_satisfactions.append(0)
            else:
                city_satisfactions.append(1)
            if satisfaction <= agent_satisfaction_threshold:
#                if i == max_iterations - 1:
 #                   print(f"{str(x)}, {str(y)}, {str(agent)}, not satisfied,"
  #                        f" {', '.join(map(str, satisfaction[1]))}, {satisfaction[2]}")
                # Move the agent to a random empty house that they are satisfied with
                # first build a list of prospects
                prospects = []
                for (xm, ym), housem in np.ndenumerate(city):
                    if housem.empty:
                        # In some cases we want them to not check the future home, and move randomly
                        if not check_future_home:
                            prospects.append((xm, ym))
                        #TODO: get check future home to work as well
                        """    
                        else:
                            # checking if prospect is satisfying
                            p_neighboring_houses = flatten(neighbors(city, xm, ym, 1))
                            p_neighboring_houses = list(filter(None.__ne__, p_neighboring_houses))
                            p_house_neighbors = []
                            # Only take into account neighbors from non-empty houses
                            for hs in p_neighboring_houses:
                                if not hs.empty:
                                    p_house_neighbors.append(hs.occupant)
                            if agent.satisfied(p_house_neighbors)[0]:
                                prospects.append((xm, ym))
                        """
                if prospects:  # if list is not empty, move to a random element
                    target_house = city[random.choice(prospects)]
                    target_house.occupant = house.occupant
                    target_house.empty = False
                    house.occupant = None
                    house.empty = True
 #           else:
  #              if i == max_iterations - 1:
   #                 print(f"{str(x)}, {str(y)}, {str(agent)}, satisfied, {', '.join(map(str, satisfaction[1]))}")
    print("satisfaction")
    print(satisfaction)
    print("agent2")
    print(agent)
    print("city satisfaction")
    print(city_satisfactions)
    return np.average(city_satisfactions)


flatten = lambda l: [item for sublist in l for item in sublist]

if __name__ == "__main__":
    city = generate_city()
    # Bitmap for the gifs
    data = np.zeros((h + 1, w + 1, 3), dtype=np.uint8)

    #sys.stdout = open("out.csv", "w")

    avg_satisfaction_over_time = []

    frames_religion = []
    frames_ethnicity = []
    frames_income = []
    # Go up to max_iterations
    for i in range(0, max_iterations):
        print(i)

        # Plot incomes
        for (x, y), house in np.ndenumerate(city):
            if x > w or y > h:
                continue
            if not house.empty:
                # equation of a line through 2 points (min_income, 0) and (max_income,255)
                color = (house.occupant.income.value - min_income) * 255 / (max_income - min_income)
                data[x][y] = [color, 255, color]
            else:
                data[x][y] = [0, 0, 0]

        img = Image.fromarray(data, 'RGB')

        # Upscale image so it's easier to see
        img = img.resize((int(w * zoom), int(h * zoom)), Image.NEAREST)

        frames_income.append(img)

        # Plot ethnicities
        for (x, y), house in np.ndenumerate(city):
            if x > w or y > h:
                continue
            if not house.empty:
                if house.occupant.ethnicity.value:
                    data[x][y] = [128, 128, 255]
                else:
                    data[x][y] = [255, 255, 255]
            else:
                data[x][y] = [0, 0, 0]

        img = Image.fromarray(data, 'RGB')

        # Upscale image so it's easier to see
        img = img.resize((int(w * zoom), int(h * zoom)), Image.NEAREST)
        frames_ethnicity.append(img)

        avg_satisfaction = time_step(i)
        if avg_satisfaction > satisfaction_threshold:
            print(f"Average agent satisfaction {avg_satisfaction} is above {satisfaction_threshold} after {i} steps.")
            break

        avg_satisfaction_over_time.append(avg_satisfaction)
    plt.plot(avg_satisfaction_over_time)
    plt.title("Average satisfaction over time")
    plt.xlabel("Number of steps")
    plt.ylabel("Average satisfaction of all agents")
    plt.savefig("out/avg_satisfaction.png")
    print(f"average satisfaction: {avg_satisfaction}")

    frames_ethnicity[0].save('out/ethnicities.gif', append_images=frames_ethnicity[1:], save_all=True, duration=200,
                             loop=0)
    frames_income[0].save('out/income.gif', append_images=frames_income[1:], save_all=True, duration=500, loop=0)

    # Plot house prices
    for (x, y), house in np.ndenumerate(city):
        if x > w or y > h:
            continue
        if not house.empty:
            color = house.price / max_price * 255
            data[x][y] = [255, color, color]
        else:
            data[x][y] = [0, 0, 0]

    img = Image.fromarray(data, 'RGB')

    # Upscale image so it's easier to see
    img = img.resize((int(w * zoom), int(h * zoom)), Image.NEAREST)
    img.save("out/house_prices.png")
