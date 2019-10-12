import random

import numpy as np

from agent import Agent, CategoricalFeature, BinaryFeature, RealNumberFeature
from city import Home


def generate_city(w, h, min_price, max_price, price_noise, price_segregation, empty_ratio, religion_preference_matrix, min_income, max_income, weight_list):
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
            else:
                a = None
            # Generating a home with a price depending on its location and its address
            grid[x][y] = Home(price=price, address=(x, y), empty=empty, occupant=a)
    return grid