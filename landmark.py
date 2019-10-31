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


# When a feature is an unordered category (e.g. religion, ethnicity)
class CategoricalFeature:
    categories: Enum

    def __init__(self, value, preference_matrix, threshold=0.5):
        self.value = value
        self.preference_matrix = preference_matrix
        self.threshold = threshold

    def preference(self, other):
        return self.preference_matrix[self.value][other.value] > self.threshold



class Landmark:

    def __init__(self, religion: CategoricalFeature, landmark):
        self.religion = religion
        self.landmark = landmark


