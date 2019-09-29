# DMAS-project
#### Modelling Segregation Effects using a Simulation Including Non-Binary Features and Global Variables


To run this, first install all dependencies with `pip install -r requirements.txt`.

`agent.py` contains the code defining an agent (house occupant) with their features and decision logic. If run by itself, the script makes a 1d array of 100 random agents and checks if each one is satisfied with their 2 neighbors.

`city.py` is a script that simulates the city grid, initializes the shape of the city, empty houses and house prices. Empty houses show up as black squares. It generates the following animated images:

`religions_over_time.gif` (not yet tested)
`ethnicities_over_time.gif`
`incomes_over_time.gif`

`avg_satisfaction.png` shows the evolution of the average satisfaction of all residents of the city over time

By changing the `weight_list` global variable, we can notice segregation by the highest weighted feature. It has been tested for ethnicity 1, others 0 and for income 1, others 0.

For the sake of diversity, religion and ethnicity have been modeled differently. Religion is n-categorical while ethnicity is binary. For ethnicity, a high average city satisfaction threshold is easy to reach, taking ~20 steps for Moore neighborhoods (see `ethnicities.gif`).

Income is continuous. An agent is satisfied with a neighbor's income if the difference between their incomes is lower than a threshold. For incomes in [100, 100k], difference 30k for satisfaction, Moore neighborhoods, it took 1863 to reach 0.9 average city satisfaction threshold (see `avg_satisfaction.png` and `income.gif`).

If the .gifs are not playing convert to mp4 using `ffmpeg -i income.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" income.mp4
`