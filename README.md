# DMAS-project
#### Modelling Segregation Effects using a Simulation Including Non-Binary Features and Global Variables


To run this, first install all dependencies with `pip install -r requirements.txt`.

`agent.py` contains the code defining an agent (house occupant) with their features and decision logic. If run by itself, the script makes a 1d array of 100 random agents and checks if each one is satisfied with their 2 neighbors.

`city.py` is a script that simulates the city grid, initializes the shape of the city, empty houses and house prices. Empty houses show up as black squares. The 3 images generated are:
* red - house prices
* green - resident incomes
* lavender blue - ethnicities (not working properly at the moment)

The actual simulation with time steps/moving agents has not been implemented yet, just populating the town and the agent decision logic.