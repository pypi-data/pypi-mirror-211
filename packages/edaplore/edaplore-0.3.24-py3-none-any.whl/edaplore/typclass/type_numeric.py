from edaplore.typclass.type_father import Type
from edaplore.typclass import names
from edaplore.stats import miss_values
from edaplore.stats import numeric_stats
from edaplore.images.make_plot import dis_plot
from edaplore.html_templates.template_loader import find_template


# Class to handle Numeric data type and perform statistical analysis and plotting.
class Numeric(Type):
    # Render the HTML template specific to numeric data
    def render(self):
        return find_template('numeric_template.html').render(num=self)

    def __init__(self, data, column_name):
        super().__init__(data, column_name)

        self.type_name = names.numeric  # Set data type name

        self.count_values = len(data)  # Count total values in data
        self.miss_values = miss_values.count_miss_vals(data)  # Count missing values
        self.duplicates = numeric_stats.count_duplicates(data)  # Count duplicate values

        # Calculating basic stats for numeric data
        self.max = numeric_stats.count_max(data)  # Maximum value
        self.min = numeric_stats.count_min(data)  # Minimum value
        self.mean = round(numeric_stats.count_mean(data), 3)  # Mean value rounded to 3 decimal places
        self.std = round(numeric_stats.count_std(data), 3)  # Standard deviation rounded to 3 decimal places

        self.dist_plot = dis_plot(self.data)  # Generate a distribution plot
        self.rendered = self.render()  # Render HTML template for displaying data stats
