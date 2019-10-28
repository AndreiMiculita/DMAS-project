import random

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from agent import Agent, RealNumberFeature, BinaryFeature, CategoricalFeature, religion_preference_matrix
from landmark import Landmark, CategoricalFeature, religion_preference_matrix
from home import Home

# Max iterations
max_iterations = 30
# Simulation stop
satisfaction_threshold = 0.9

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
weight_list = [0, 1, 0]

# Ratio of empty houses
empty_ratio = 0.1

# Ratio of landmarks
landmark_ratio = 0.01

# how much to zoom in on the picture before displaying, please use integer for good results
zoom = 10

# Whether an agent checks their future neighbors before moving to a house
check_future_home = False


def neighbors(a, radius, rowNumber, columnNumber, agent):
    house_neighbors = []
    # empty = 0
    # print(rowNumber, columnNumber, end="")
    for i in range(rowNumber - radius, rowNumber + radius + 1):
        for j in range(columnNumber - radius, columnNumber + radius + 1):
            if 0 <= i < len(a) and 0 <= j < len(a[0]):
                if not a[i][j].empty and a[i][j].occupant != agent:
                    house_neighbors.append(a[i][j].occupant)
                #     print("neighbor", i, j, end="")
                # else:
                    # empty+=1
                    # print("empty", i, j, end="")
    # print("neighbors: ", len(house_neighbors), "empty: ", empty)
    return house_neighbors


def generate_city():
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

            # 1 in 10 probability of an empty house, 1 in 100 for a landmark. Landmark takes priority over empty
            empty = random.randint(1, 1 / empty_ratio) == 1
            landmark = random.randint(1, 1 / landmark_ratio) == 1
            if landmark:
                empty = 0

            # If both empty and landmark are false, make an agent
            if not empty or not landmark:
                # Creating a random agent that lives in that home
                eth = (random.randint(1, 2) == 1)
                a = Agent(religion=CategoricalFeature(value=random.randint(1, 9),
                                                      preference_matrix=religion_preference_matrix),
                          ethnicity=BinaryFeature(value=eth),
                          income=RealNumberFeature(value=random.randint(min_income, max_income), threshold=30000),
                          landmark=0,
                          weights=weight_list)
            # If empty is true, make the space empty
            elif empty:
                a = None
            # Lastly if not empty and landmark is true, make a landmark of a random religion
            else:
                a = Landmark(religion=CategoricalFeature(value=random.randint(1, 9),
                                                         preference_matrix=religion_preference_matrix),
                             landmark=1)

            # Generating a home with a price depending on its location
            grid[x][y] = Home(price=price, empty=empty, landmark=landmark, occupant=a)
    return grid


def time_step(i):
    if i % 100 == 0:
        print(i)

    city_satisfactions = []
    # Go through the entire city to check whether occupants are satisfied
    for (x, y), house in np.ndenumerate(city):
        # Skip edge for now
        if not (house.empty or house.landmark):
            agent = house.occupant
            house_neighbors = neighbors(city, 1, x, y, agent)
            satisfaction = agent.satisfied(house_neighbors)
            city_satisfactions.append(int(satisfaction > 0.5))
            # If the agent is not satisfied with their current position, try to move
            if not satisfaction > 0.5:
                if i == max_iterations - 1:
                    print(f"{str(x)}, {str(y)}, {str(agent)}, not satisfied,"
                          f" {satisfaction}")
                # Move the agent to a random empty house that they are satisfied with
                # first build a list of prospects
                prospects = []
                for (xm, ym), housem in np.ndenumerate(city):
                    if housem.empty:
                        # In some cases we want them to not check the future home, and move randomly
                        if not check_future_home:
                            prospects.append((xm, ym))
                        else:
                            # checking if prospect is satisfying
                            p_house_neighbors = neighbors(city, 1, xm, ym, agent)
                            if agent.satisfied(p_house_neighbors) > 0.5:
                                prospects.append((xm, ym))
                if prospects:  # if list is not empty, move to a random element
                    target_house = city[random.choice(prospects)]
                    target_house.occupant = house.occupant
                    target_house.empty = False
                    house.occupant = None
                    house.empty = True
            else:
                if i == max_iterations - 1:
                    print(f"{str(x)}, {str(y)}, {str(agent)}, satisfied, {satisfaction}")

    return np.average(city_satisfactions)


def get_frame(city):
    data = np.zeros((h + 1, w + 1, 3), dtype=np.uint8)

    # Plot incomes
    for (x, y), house in np.ndenumerate(city):
        if x > w or y > h:
            continue
        if not (house.empty or house.landmark):
            # equation of a line through 2 points (min_income, 0) and (max_income,255)
            color = (house.occupant.income.value - min_income) * 255 / (max_income - min_income)
            data[x][y] = [color, 255, color]
        elif house.landmark:
            data[x][y] = [255, 255, 0]
        else:
            data[x][y] = [0, 0, 0]

    img_income = Image.fromarray(data, 'RGB')

    # Upscale image so it's easier to see
    img_income = img_income.resize((int(w * zoom), int(h * zoom)), Image.NEAREST)


    # Plot ethnicities
    for (x, y), house in np.ndenumerate(city):
        if x > w or y > h:
            continue
        if not (house.empty or house.landmark):
            if house.occupant.ethnicity.value:
                data[x][y] = [128, 128, 255]
            else:
                data[x][y] = [255, 255, 255]
        elif house.landmark:
            data[x][y] = [255, 255, 0]
        else:
            data[x][y] = [0, 0, 0]

    img_ethnicity = Image.fromarray(data, 'RGB')
    # Upscale image so it's easier to see
    img_ethnicity = img_ethnicity.resize((int(w * zoom), int(h * zoom)), Image.NEAREST)

    return img_income, img_ethnicity


if __name__ == "__main__":
    city = generate_city()

    # Bitmap for the gifs
    data = np.zeros((h + 1, w + 1, 3), dtype=np.uint8)

    # Plot house prices
    for (x, y), house in np.ndenumerate(city):
        if x > w or y > h:
            continue
        if not (house.empty or house.landmark):
            color = house.price / max_price * 255
            data[x][y] = [255, color, color]
        elif house.landmark:
            data[x][y] = [255, 255, 0]
        else:
            data[x][y] = [0, 0, 0]

    img = Image.fromarray(data, 'RGB')

    # Upscale image so it's easier to see
    img = img.resize((int(w * zoom), int(h * zoom)), Image.NEAREST)
    img.save("out/house_prices.png")

    # sys.stdout = open("out.csv", "w")

    avg_satisfaction_over_time = []

    frames_religion = []
    frames_ethnicity = []
    frames_income = []
    # Go up to max_iterations
    for i in range(0, max_iterations):
        frame_income, frame_ethnicity = get_frame(city)
        frames_income.append(frame_income)
        frames_ethnicity.append(frame_ethnicity)

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
                             loop=1)
    frames_income[0].save('out/income.gif', append_images=frames_income[1:], save_all=True, duration=500, loop=1)

