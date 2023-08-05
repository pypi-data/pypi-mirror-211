import pandas as pd


# Class to handle combination of multiple data columns into a pandas DataFrame
class Combiner:
    # Constructor
    def __init__(self, x=None, y=None, hue=None):
        # Check if 'x', 'y', 'hue' are provided, if yes then use their column names
        # Else set respective attributes to None
        self.x = x.column_name if x else None
        self.y = y.column_name if y else None
        self.hue = hue.column_name if hue else None

        # Create a dictionary to store column_name: data pairs
        container = {el.column_name: el.data for el in [x, y, hue] if el}

        # Convert the dictionary to a pandas DataFrame
        self.data_frame = pd.DataFrame(container)

        # Prepare arguments for seaborn plotting functions
        self.args = {'data': self.data_frame}
        if self.x:
            self.args['x'] = self.x
        if self.y:
            self.args['y'] = self.y
        if self.hue:
            self.args['hue'] = self.hue
