# Max iterations
max_iterations = 100
# Simulation stop
satisfaction_threshold = 0.9

# Width and height of the city grid
w, h = 16,  16

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
weight_list = [0.34, 0.33, 0.33]

# Ratio of empty houses
empty_ratio = 0.1

# Ratio of landmarks
landmark_ratio = 0.01

# how much to zoom in on the picture before displaying, please use integer for good results
zoom = 10

radius = 1

# Whether an agent checks their future neighbors before moving to a house
check_future_home = False
