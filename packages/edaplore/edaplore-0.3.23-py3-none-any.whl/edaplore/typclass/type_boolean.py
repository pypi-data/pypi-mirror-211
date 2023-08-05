from edaplore.typclass.type_father import Type
from edaplore.typclass import names
from edaplore.stats.miss_values import count_miss_vals
from edaplore.stats import boolean_stats
from edaplore.images.make_plot import count_plot
from edaplore.html_templates.template_loader import find_template


# Class to handle Boolean data type and perform statistical analysis and plotting.
class Boolean(Type):

    # Render the HTML template specific to boolean data
    def render(self):
        return find_template('boolean_template.html').render(boolean=self)

    def __init__(self, data, column_name):
        super().__init__(data, column_name)

        self.type_name = names.bolean  # Set data type name
        self.count_values = len(data)  # Count total values in data
        self.miss_values = count_miss_vals(data)  # Count missing values
        self.ratio = boolean_stats.count_ration(data)  # Calculate ratio of True to False values
        self.count_categories = 2  # Number of categories in Boolean type (True and False)

        self.dist_plot = count_plot(self.data)  # Generate a distribution plot
        self.rendered = self.render()  # Render HTML template for displaying data stats
