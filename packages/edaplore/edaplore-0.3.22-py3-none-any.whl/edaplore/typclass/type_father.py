# Base class for handling different data types
class Type:
    # Constructor
    def __init__(self, data, column_name):
        self.data = data  # Data column
        self.column_name = column_name  # Name of the data column
        self.type_name = ''  # Name of the type. To be set by subclasses.

        # Statistics to be computed in subclasses
        self.count_values = 0  # Total number of values (not including missing)
        self.miss_values = 0  # Total number of missing values
