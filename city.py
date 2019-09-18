from PIL import Image
import numpy as np
import random
from agent import Agent

w, h = 128, 128

class Home:
    def __init__(self, price, address, occupant):
        self.price = price
        self.address = address
        self.occupant = occupant
    def __str__(self):
        return str(self.price)

city = np.zeros((w, h), dtype=object)
for x in range(0, w):
    for y in range(0, h):
        # Generating a home with a price depending on its location and its address
        city[x][y] = Home(price=random.randint(0, 255), address=(x,y), occupant=Agent(100, 200, 50))
        
print(city)

data = np.full((h, w, 3), 255, dtype=np.uint8)

for (x, y), element in np.ndenumerate(city):
    data[x][y] = [255, element.price, element.price]
    
img = Image.fromarray(data, 'RGB')

img.save('my.png')

basewidth = 1024
img = Image.open('my.png')
wpercent = (basewidth/float(img.size[0]))
hsize = int((float(img.size[1])*float(wpercent)))
img = img.resize((basewidth,hsize), Image.NEAREST)
img.save('sompic.png') 
img.show()
