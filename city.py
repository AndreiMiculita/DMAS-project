import random
import sys

import numpy as np
from PIL import Image

from agent import Agent, RealNumberFeature, BinaryFeature, CategoricalFeature, Religion, religion_preference_matrix

# Width and height of the city grid
w, h = 128, 128

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

# Ratio of empty houses
empty_ratio = 0.01

# how much to zoom in on the picture before displaying, please use integer for good results
zoom = 5


class Home:
    def __init__(self, price, address, empty: bool, occupant: Agent):
        self.price = price
        self.address = address
        self.empty = empty
        self.occupant = occupant

    def __str__(self):
        return str(self.price)


if __name__ == "__main__":
    # City is a matrix with a padding
    city = np.zeros((w + 2, h + 2), dtype=object)
    for x in range(-2, w + 2):
        for y in range(-2, h + 2):
            # These are 2 rows/columns that will not show in the bitmap,
            # but we will use them to generate the first row/column
            if x < 0 or y < 0 or x > w or y > h:
                price = random.randint(min_price, max_price)
            # Average the 2 pixels above and the 2 pixels to the left then add noise and mod
            else:
                price = np.average([city[x][y - 1].price, city[x][y - 2].price,
                                    city[x - 1][y].price, city[x - 2][y].price,
                                    city[x - 1][y + 1].price, city[x - 2][y + 1].price])
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
                eth = random.randint(1, 5) == 1
                a = Agent(religion=CategoricalFeature(value=random.choice(list(Religion)),
                                                      preference_matrix=religion_preference_matrix),
                          ethnicity=BinaryFeature(value=eth),
                          income=RealNumberFeature(value=random.randint(min_income, max_income), threshold=20))
            else:
                a = None
            # Generating a home with a price depending on its location and its address
            city[x][y] = Home(price=price, address=(x, y), empty=empty, occupant=a)

    data = np.zeros((h + 2, w + 2, 3), dtype=np.uint8)

    sys.stdout = open("out.csv", "w")

    # Only one time step for now
    for _ in range(0, 1):
        # Go through the entire city to check whether occupants are satisfied
        for (x, y), house in np.ndenumerate(city):
            # Skip edge for now
            if not house.empty and x > 0 and y > 0 and x < 129 and y < 129:
                neighboring_houses = [city[x - 1][y - 1], city[x - 1][y], city[x - 1][y + 1],
                                      city[x][y - 1], city[x][y + 1],
                                      city[x + 1][y - 1], city[x + 1][y], city[x + 1][y + 1]]
                house_neighbors = []
                # Only take into account neighbors from non-empty houses
                for hs in neighboring_houses:
                    if not hs.empty:
                        house_neighbors.append(hs.occupant)
                agent = house.occupant
                satisfaction = agent.satisfied(house_neighbors)
                if satisfaction[0]:
                    print(f"{str(x)}, {str(y)}, {str(agent)}, satisfied, {', '.join(map(str, satisfaction[1]))}")
                else:
                    print(f"{str(x)}, {str(y)}, {str(agent)}, not satisfied, {', '.join(map(str, satisfaction[1]))}")

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
    img.show(title="Prices")

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
    img.show(title="Incomes")

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
    img.show(title="Etnicities")
