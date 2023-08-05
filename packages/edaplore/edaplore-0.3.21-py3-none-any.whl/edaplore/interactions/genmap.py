import edaplore.images.make_plot as plot
from edaplore.html_templates.template_loader import find_template


class GenMap:
    def render(self):
        """
        Renders a Jinja template with the GenMap object.

        :return: A string containing the rendered HTML template.
        """
        template = find_template('genmap_template.html').render(gm=self)
        return template

    def mis_vals(self):
        """
        Creates visualizations for missing values in the data.
        """
        df = self.data.isna()
        self.miss_heatmap = plot.heat_map_general(df.transpose())
        self.miss_barplot = plot.barplot_general(x=df.sum().index, y=df.sum().values)

    def corr_matrix(self):
        """
        Creates a correlation heatmap for numeric columns in the data.
        """
        df = self.data.corr(numeric_only=True)
        self.corr_heatmap = plot.heat_map_general(df, annot=True)

    def __init__(self, data):
        """
        Initializes the GenMap class, creates visualizations for missing values and correlation heatmap.

        :param data: A pandas DataFrame object.
        """
        self.data = data
        self.miss_heatmap = None
        self.miss_barplot = None
        self.mis_vals()
        self.corr_heatmap = None
        self.corr_matrix()
        self.rendered = self.render()
