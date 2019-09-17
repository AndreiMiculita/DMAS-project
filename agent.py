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
    def __init__(self, value: float, difference_function, threshold):
        self.value = value
        self.difference_function = difference_function  # the function passed as a parameter
        self.threshold = threshold

    def preference(self, other):
        return self.difference_function(abs(other.value - self.value)) > self.threshold


# An agent with the ability to make decisions
class Agent:
    def __init__(self, religion: CategoricalFeature, ethnicity: CategoricalFeature, income: RealNumberFeature):
        self.income = income
        self.religion = religion
        self.ethnicity = ethnicity
