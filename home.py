from agent import Agent


class Home:
    def __init__(self, price, empty: bool, occupant: Agent):
        self.price = price
        self.empty = empty
        self.occupant = occupant

    def __str__(self):
        return str(self.price)