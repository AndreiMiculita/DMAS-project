import random
import sys
from enum import Enum, auto

import numpy as np


class Religion(Enum):
    IRRELIGIOUS = 1
    ROMAN_CATHOLIC = 2
    DUTCH_REFORMED = 3
    PROTESTANT = 4
    REFORMED_CHURCHES = 5
    MUSLIM = 6
    HINDU = 7
    JEWISH = 8
    BUDDHIST = 9


# How much each religion likes each other religion
religion_preference_matrix = np.identity(9, dtype=float)


class Ethnicity(Enum):
    DUTCH = auto()
    GERMAN = auto()
    TURKISH = auto()
    MOROCCAN = auto()
    INDONESIAN = auto()
    SURINAMESE = auto()
    AAD = auto()  # Antillean, Aruban, or Dutch Caribbean


# When a feature is an unordered category (e.g. religion, ethnicity)
class CategoricalFeature:
    categories: Enum

    def __init__(self, value, preference_matrix, threshold=0.5):
        self.value = value
        self.preference_matrix = preference_matrix
        self.threshold = threshold

    def preference(self, other):
        return self.preference_matrix[self.value][other.value] > self.threshold


# When a feature is a real number
class RealNumberFeature(object):
    def __init__(self, value: float, threshold=20000, difference_function=lambda x: x):
        self.value = value
        self.difference_function = difference_function  # the function passed as a parameter
        self.threshold = threshold

    def preference(self, other):
        return self.difference_function(abs(other.value - self.value)) < self.threshold


# When a feature is binary
class BinaryFeature(object):
    def __init__(self, value: bool):
        self.value = value

    def preference(self, other):
        return self.value == other.value


# An agent with the ability to make decisions
class Agent:
    satisfaction_threshold = 0.5

    def __init__(self, religion: CategoricalFeature, ethnicity: BinaryFeature, income: RealNumberFeature, landmark,
                 weights=None):
        self.religion = religion
        self.ethnicity = ethnicity
        self.income = income
        # The weights of each feature when determining if an agent is satisfied with their position
        if weights is None:
            weights = [0, 1, 0]
        self.weights = weights
        self.landmark = landmark

    def income_satisfaction_calculation(self, other_income):
        sat = min(self.income.value, other_income.value)/max(self.income.value, other_income.value)
        return sat

    # Whether an agent is satisfied with their current position
    def satisfied(self, neighbors):
        # First put all the satisfactions in arrays, for each feature and each neighbor
        # There's probably an even shorter way of doing this in python
        # Use income temporarily
        if self.weights[0]!=0:
            neighbor_religion_satisfactions = [self.religion.preference(n.religion) for n in neighbors if not n.landmark]
        else:
            neighbor_religion_satisfactions = [0]
        if self.weights[1]!=0:
            neighbor_ethnicity_satisfactions = [self.ethnicity.preference(n.ethnicity) for n in neighbors if not n.landmark]
        else:
            neighbor_ethnicity_satisfactions = [0]
        if self.weights[2]!=0:
            neighbor_income_satisfactions = [self.income_satisfaction_calculation(n.income) for n in neighbors if not n.landmark]
        else:
            neighbor_income_satisfactions = [0]
        # Calculate the average satisfaction for each feature
        avg_neighbor_religion_satisfaction = np.average(neighbor_religion_satisfactions)
        avg_neighbor_ethnicity_satisfaction = np.average(neighbor_ethnicity_satisfactions)
        avg_neighbor_income_satisfaction = np.average(neighbor_income_satisfactions)

        # If there is a landmark within the neighbors that shares a religion with the agent
        # then maximise religion satisfaction

        #use this if religion works.
        for n in neighbors:
            if n.landmark:
                #print("About to check for landmark religion")
                if self.religion.preference(n.religion):
                    avg_neighbor_religion_satisfaction = 1
                    #print("I changed the satisfaction")

        # 3 arrays can be treated as a matrix, np.average averages all of the numbers
        self.satisfaction = np.average(a=[avg_neighbor_religion_satisfaction,
                                          avg_neighbor_ethnicity_satisfaction,
                                          avg_neighbor_income_satisfaction], weights=self.weights)

        # Returns a list where the first element is whether they're satisfied or not, and the 2nd element
        # is a list containing the individual satisfactions
        return self.satisfaction

    def __str__(self):
        return str(id(self)) + ", " + \
               str(self.religion.value) + ", " + \
               str(self.ethnicity.value) + ", " + \
               str(self.income.value)


if __name__ == "__main__":
    agent_list = [Agent(religion=CategoricalFeature(value=random.choice(list(Religion)),
                                                    preference_matrix=religion_preference_matrix),
                        ethnicity=BinaryFeature(value=random.choice([True, False])),
                        income=RealNumberFeature(value=random.randint(0, 100), threshold=20)) for _ in range(0, 100)]
    print([str(x) for x in agent_list])
    sys.stdout = open("out/out.csv", "w")
    for index, agent in enumerate(agent_list[1:]):
        # Check whether an agent is satisfied with their neighbors
        satisfaction = agent.satisfied([agent_list[index - 1], agent_list[index + 1]])
        if satisfaction[0]:
            print(f"{str(index)}, {str(agent)}, satisfied, {', '.join(map(str, satisfaction[1]))}")
        else:
            print(f"{str(index)}, {str(agent)}, not satisfied, {', '.join(map(str, satisfaction[1]))}")
