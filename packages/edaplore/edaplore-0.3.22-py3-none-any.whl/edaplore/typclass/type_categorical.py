from edaplore.types_clases.type_father import Type
from edaplore.types_clases import names
from edaplore.stats.miss_values import count_miss_vals
from edaplore.stats import categorical_stats
from edaplore.images.make_plot import dis_plot
from edaplore.html_templates.template_loader import find_template


# Class to handle Categorical data type and perform statistical analysis and plotting.
class Categorical(Type):

    # Render the HTML template specific to categorical data
    def render(self):
        return find_template('categorical_template.html').render(cat=self)

    # Function to calculate the total length of all category names
    def count_categ_names_len(self):
        return sum(len(el) for el in self.data.cat.categories)

    # Generate a distribution plot for the data if the total length of category names is <= 30
    def make_plot(self):
        if self.names_length > 30:
            return None
        self.isPlot = True
        return dis_plot(self.data)

    def __init__(self, data, column_name):
        super().__init__(data, column_name)

        self.data = data.astype('category')  # Convert data to categorical type
        self.type_name = names.categorical  # Set data type name
        self.count_values = len(data)  # Count total values in data
        self.miss_values = count_miss_vals(data)  # Count missing values

        self.categories = categorical_stats.get_value_counts(data)  # Get value counts for each category
        self.count_categories = len(self.categories)  # Number of unique categories in data

        self.isPlot = False  # Initialize flag to indicate whether a plot can be made
        self.names_length = self.count_categ_names_len()  # Calculate total length of category names
        self.categ_names = list(self.categories.index)  # List of unique category names

        self.dist_plot = self.make_plot()  # Generate a distribution plot
        self.rendered = self.render()  # Render HTML template for displaying data stats
