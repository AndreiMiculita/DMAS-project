import random
from enum import Enum

import numpy as np


# class Religion(Enum):
#     IRRELIGIOUS = auto()
#     ROMAN_CATHOLIC = auto()
#     DUTCH_REFORMED = auto()
#     PROTESTANT = auto()
#     REFORMED_CHURCHES = auto()
#     MUSLIM = auto()
#     HINDU = auto()
#     JEWISH = auto()
#     BUDDHIST = auto()
#
#
# class Ethnicity(Enum):
#     DUTCH = auto()
#     GERMAN = auto()
#     TURKISH = auto()
#     MOROCCAN = auto()
#     INDONESIAN = auto()
#     SURINAMESE = auto()
#     AAD = auto()  # Antillean, Aruban, or Dutch Caribbean

# When a feature is an unordered category (e.g. religion, ethnicity)
class CategoricalFeature:
    categories: Enum

    def __init__(self, categories: Enum, threshold):
        self.categories = categories
        self.preference_matrix = np.ones((len(self.categories), len(self.categories)), dtype=float)
        self.threshold = threshold

    def preference(self, i, j):
        return self.preference_matrix[i][j] > self.threshold


# When a feature is a real number
class RealNumberFeature(object):
    def __init__(self, value: float, threshold, difference_function=lambda x: x):
        self.value = value
        self.difference_function = difference_function  # the function passed as a parameter
        self.threshold = threshold

    def preference(self, other):
        return self.difference_function(abs(other.value - self.value)) > self.threshold


# When a feature is a real number
class BinaryFeature(object):
    def __init__(self, value: bool):
        self.value = value

    def preference(self, other):
        return self.value == other.value


# An agent with the ability to make decisions
class Agent:
    satisfaction = 1
    satisfaction_threshold = 0.5

    def __init__(self, religion: CategoricalFeature, ethnicity: BinaryFeature, income: RealNumberFeature,
                 weights=None):
        self.religion = religion
        self.ethnicity = ethnicity
        self.income = income
        # The weights of each feature when determining if an agent is satisfied with their position
        if weights is None:
            weights = [1, 1, 1]
        self.weights = weights

    # Whether an agent is satisfied with their current position
    def satisfied(self, neighbors):
        # First put all the satisfactions in arrays, for each feature and each neighbor
        # There's probably an even shorter way of doing this in python
        neighbor_income_satisfactions = [self.income.preference(n.income) for n in neighbors]
        neighbor_religion_satisfactions = [self.ethnicity.preference(n.ethnicity) for n in neighbors]
        # Use income temporarily
        neighbor_ethnicity_satisfactions = [self.income.preference(n.income) for n in neighbors]

        # Calculate the average satisfaction for each feature
        avg_neighbor_income_satisfaction = np.average(neighbor_income_satisfactions)
        avg_neighbor_religion_satisfaction = np.average(neighbor_religion_satisfactions)
        avg_neighbor_ethnicity_satisfaction = np.average(neighbor_ethnicity_satisfactions)

        # 3 arrays can be treated as a matrix, np.average averages all of the numbers
        self.satisfaction = np.average(a=[avg_neighbor_income_satisfaction, avg_neighbor_religion_satisfaction,
                                          avg_neighbor_ethnicity_satisfaction], weights=self.weights)

        return self.satisfaction >= self.satisfaction_threshold

    def __str__(self):
        return str(id(self)) + " " + \
               str(self.religion) + " " + \
               str(self.ethnicity) + " " + \
               str(self.income)


if __name__ == "__main__":
    agent_list = [Agent(100, ethnicity=BinaryFeature(value=random.choice([True, False])),
                        income=RealNumberFeature(value=random.randint(0, 100), threshold=20)) for i in range(0, 100)]
    print([str(x) for x in agent_list])
    for x in range(0, 99):
        print(agent_list[x].satisfied([agent_list[x - 1], agent_list[x + 1]]))
