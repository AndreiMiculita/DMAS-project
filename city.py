from PIL import Image
import numpy as np
import random
from agent import Agent

w, h = 128, 128
max_price = 255
price_noise = 40
price_segregation = 0.1


class Home:
    def __init__(self, price, address, occupant):
        self.price = price
        self.address = address
        self.occupant = occupant

    def __str__(self):
        return str(self.price)


if __name__ == "__main__":
    city = np.zeros((w, h), dtype=object)
    for x in range(-2, w):
        for y in range(-2, h):
            # These are 2 rows/columns that will not show in the bitmap,
            # but we will use them to generate the first row/column
            if x == -2 or y == -2 or x == -1 or y == -1:
                price = random.randint(0, max_price)
            # Average the 2 pixels above and the 2 pixels to the left then add noise and mod
            else:
                price = ((city[x][y-1].price + city[x][y-2].price + city[x-1][y].price + city[x-2][y].price)/4
                         + random.randint(-price_noise, price_noise)) % max_price

            # Move all values toward 0 and max_price a bit, depending on which they are closer to
            # Do a weighted average - price_segregation is the weight of the endpoints
            if price < max_price/2:
                price = price/(1 + price_segregation)
            else:
                price = (price + max_price * price_segregation) / (1 + price_segregation)
            # Generating a home with a price depending on its location and its address
            city[x][y] = Home(price=price, address=(x, y), occupant=Agent(100, 200, 50))

    print(city)

    data = np.full((h, w, 3), 255, dtype=np.uint8)

    for (x, y), element in np.ndenumerate(city):
        color = element.price / max_price * 255
        data[x][y] = [255, color, color]

    img = Image.fromarray(data, 'RGB')

    base_width = 640
    w_percent = (base_width/float(img.size[0]))
    h_size = int((float(img.size[1])*float(w_percent)))
    img = img.resize((base_width, h_size), Image.NEAREST)
    img.show()
