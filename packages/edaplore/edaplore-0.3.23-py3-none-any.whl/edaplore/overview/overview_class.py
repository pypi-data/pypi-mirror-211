import edaplore.typclass.names as names

from edaplore.html_templates.template_loader import find_template


class Overview:
    def count_categories_and_miss(self):
        """
        Counts the number of missing values and the number of numeric, boolean, and categorical types.

        :return: None
        """
        for el in self.data:
            self.miss_vals += el.miss_values

            if names.numeric == el.type_name:
                self.count_numeric += 1

            if names.bolean == el.type_name:
                self.count_boolean += 1

            if names.categorical == el.type_name:
                self.count_categorical += 1

    def render(self):
        """
        Renders a Jinja template using the overview data.

        :return: A string containing the rendered HTML template.
        """
        template = find_template('overview_template.html').render(overview=self)
        return template

    def __init__(self, data):
        """
        Initializes the Overview class, performing counting of categories and missing values.

        :param data: A list of 'Type' objects to be used in the overview.
        """
        self.data = data
        self.count_columns = len(data)
        self.count_rows = data[0].count_values

        self.miss_vals = 0
        self.count_numeric = 0
        self.count_boolean = 0
        self.count_categorical = 0

        self.count_categories_and_miss()
        self.rendered = self.render()
