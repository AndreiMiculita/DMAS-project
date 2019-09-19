from PIL import Image
import numpy as np
import random
from agent import Agent

w, h = 128, 128
max_price = 1000000

# if 0 - price will not have any noise
# if 1 - price will fluctuate with values between 0 and max_price
price_noise = 0.35

# weight of extreme prices, if 0 prices will be evenly distributed
price_segregation = 0.1


class Home:
    def __init__(self, price, address, occupant):
        self.price = price
        self.address = address
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
                price = random.randint(0, max_price)
            # Average the 2 pixels above and the 2 pixels to the left then add noise and mod
            else:
                price = np.average([city[x][y - 1].price, city[x][y - 2].price,
                                    city[x - 1][y].price, city[x - 2][y].price,
                                    city[x-1][y+1].price, city[x-2][y+1].price])
                price = price + random.randint(-price_noise*max_price, price_noise*max_price)

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

            # Generating a home with a price depending on its location and its address
            city[x][y] = Home(price=price, address=(x, y), occupant=Agent(100, 200, 50))

    data = np.zeros((h+2, w+2, 3), dtype=np.uint8)

    for (x, y), element in np.ndenumerate(city):
        if x > w or y > h:
            continue
        color = element.price / max_price * 255
        data[x][y] = [255, color, color]

    img = Image.fromarray(data, 'RGB')

    base_width = 640
    w_percent = (base_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((base_width, h_size), Image.NEAREST)
    img.show()
