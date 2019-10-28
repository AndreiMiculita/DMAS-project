from agent import Agent


class Home:
    def __init__(self, price, empty: bool, landmark: bool, occupant: Agent):
        self.price = price
        self.empty = empty
        # Landmarks are currently correctly identified on the grid, but are cast as Agents
        self.landmark = landmark
        self.occupant = occupant

    def __str__(self):
        return str(self.price)