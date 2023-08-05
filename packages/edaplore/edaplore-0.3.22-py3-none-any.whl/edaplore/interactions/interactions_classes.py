# Import Combiner class for data combination
from edaplore.separator.combine import *

# Importing plot module for creating different types of plots
import src.edaplore.images.make_plot as plot

# Importing classes for handling templates and rendering HTML
from jinja2 import Environment, FileSystemLoader

from edaplore.html_templates.template_loader import find_template


# Defining class for interaction between two numeric features
class NumNum:
    # Function to render HTML templates
    def render(self):
        return find_template('interaction_num_num.html').render(plot_names=self.plots)

    # Initialize the class with two numeric features
    def __init__(self, num1, num2):
        self.plots = []
        self.name = f'{num1.column_name}_{num2.column_name}'
        comb = Combiner(x=num1, y=num2)

        # Create and store different plots for the features
        line_plot = plot.line_plot(comb)
        self.plots.append(line_plot)

        joint_plot = plot.joint_plot(comb)
        self.plots.append(joint_plot)

        kde_plot = plot.kde_plot(comb)
        self.plots.append(kde_plot)

        # Render the HTML template with the created plots
        self.rendered = self.render()


# Defining class for interaction between a numeric and a categorical feature
class NumCat:
    # Same render function as above
    def render(self):
        return find_template('interaction_num_num.html').render(plot_names=self.plots)

    # Initialize the class with a numeric and a categorical feature
    def __init__(self, num1, cat1):
        self.plots = []
        self.name = f'{num1.column_name}_{cat1.column_name}'
        comb = Combiner(x=cat1, y=num1)

        # Create and store different plots for the features
        bar_plot = plot.bar_plot(comb)
        self.plots.append(bar_plot)

        violin_plot = plot.violin_plot(comb)
        self.plots.append(violin_plot)

        strip_plot = plot.strip_plot(comb)
        self.plots.append(strip_plot)

        # Render the HTML template with the created plots
        self.rendered = self.render()


# Defining class for interaction between two categorical features
class CatCat:
    # Same render function as above
    def render(self):
        return find_template('interaction_num_num.html').render(plot_names=self.plots)

    # Initialize the class with two categorical features
    def __init__(self, cat1, cat2):
        self.plots = []
        self.name = f'{cat1.column_name}_{cat2.column_name}'
        comb = Combiner(x=cat1, hue=cat2)

        # Create and store different plots for the features
        count_plt = plot.count_plot_combiner(comb)
        self.plots.append(count_plt)

        # Render the HTML template with the created plots
        self.rendered = self.render()


# Defining class for interaction between two numeric features and a categorical feature
class Num2Cat:
    # Same render function as above
    def render(self):
        return find_template('interaction_num_num.html').render(plot_names=self.plots)

    # Initialize the class with two numeric features and a categorical feature
    def __init__(self, num1, num2, cat1):
        self.plots = []
        self.name = f'{num1.column_name}_{num2.column_name}_{cat1.column_name}'
        comb = Combiner(x=num1, y=num2, hue=cat1)

        # Create and store different plots for the features
        scat = plot.scatter_plot(comb)
        self.plots.append(scat)

        line = plot.line_plot(comb)
        self.plots.append(line)

        pair = plot.pair_plot(comb)
        self.plots.append(pair)

        joint = plot.joint_plot(comb)
        self.plots.append(joint)

        # Render the HTML template with the created plots
        self.rendered = self.render()


# Defining class for interaction between a numeric and two categorical features
class NumCat2:
    # Same render function as above
    def render(self):
        return find_template('interaction_num_num.html').render(plot_names=self.plots)

    # Initialize the class with a numeric and two categorical features
    def __init__(self, num1, cat1, cat2):
        self.plots = []
        self.name = f'{num1.column_name}_{cat1.column_name}_{cat2.column_name}'
        comb = Combiner(x=cat1, y=num1, hue=cat2)

        # Create and store different plots for the features
        bar = plot.bar_plot(comb)
        self.plots.append(bar)

        violin = plot.violin_plot(comb)
        self.plots.append(violin)

        heatmap = plot.heat_map(comb)
        self.plots.append(heatmap)

        # Render the HTML template with the created plots
        self.rendered = self.render()
