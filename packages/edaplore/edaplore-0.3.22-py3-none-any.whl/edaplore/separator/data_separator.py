from edaplore.separator import define_data_type
import edaplore
import src.edaplore.typclass

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder


class Separator:
    # One-hot encoding for categorical features with no more than 3 unique values
    def one_hot_encode(self):
        encoder = OneHotEncoder(sparse=False)

        for col in self.col_names:
            if define_data_type.is_categorical_type(self.data[col]):
                if self.data[col].nunique() <= 3:
                    # Apply one-hot encoding and create a new DataFrame
                    encoded_cols = encoder.fit_transform(self.data[[col]])
                    df_encoded = pd.DataFrame(encoded_cols, columns=[f'{col}_{cat}' for cat in encoder.categories_[0]])

                    # Drop original column and concatenate the DataFrame with encoded columns
                    self.data = self.data.drop(col, axis=1)
                    self.data = pd.concat([self.data, df_encoded], axis=1)

    # Fill missing values: mean for numeric columns, mode for others
    def fill_mis_values(self):
        for col in self.col_names:
            if define_data_type.is_numeric_type(self.data[col]):
                self.data[col].fillna(self.data[col].mean(), inplace=True)
            else:
                self.data[col].fillna(self.data[col].mode()[0], inplace=True)

        # If there are still NaN values, fill with mean (for numeric columns) and 'missing' (for others)
        self.data.fillna(self.data.mean(), inplace=True)
        self.data.fillna('missing', inplace=True)

    # Drop outliers, defined as values that are above the 95th percentile by default
    def drop_outlier(self, threshold=0.95):
        numeric_cols = self.data.select_dtypes(include=[np.number])  # Select only numeric columns
        quantiles = numeric_cols.quantile(threshold)

        # Create boolean masks for values below or equal to the threshold
        masks = numeric_cols.apply(lambda x: x <= quantiles[x.name])

        # Keep only rows where all numeric values are below the threshold
        self.data = self.data[masks.all(axis=1)]
        self.data = self.data.reset_index(drop=True)

    # Constructor: initialize data, apply preprocessing steps if specified, and separate columns by data type
    def __init__(self, data, fill_mis=False, drop_outliers=False, threshold=0.95, ohe=False):
        if define_data_type.is_data_frame(data):
            self.data = data
            self.col_names = list(data.columns)

            # Apply preprocessing steps if specified
            if fill_mis:
                self.fill_mis_values()
            if drop_outliers:
                self.drop_outlier(threshold)
            if ohe:
                self.one_hot_encode()

            self.col_names = list(self.data.columns)

            # Initialize dictionaries to store separated columns
            self.numeric = {}
            self.boolean = {}
            self.categorical = {}

            self.data_classes = []

            self.separate()

            self.numeric_list = list(self.numeric.values())
            self.categorical_list = list(self.categorical.values())
            self.boolean_list = list(self.boolean.values())

    # Separate columns by data type
    def separate(self):
        cat_cols = self.data.select_dtypes(include=['object']).columns
        for col in self.col_names:
            if define_data_type.is_bool_type(self.data[col]):
                C = src.edaplore.typclass.type_boolean.Boolean(self.data[col], col)
                self.boolean[col] = C
                self.data_classes.append(C)
                continue

            if define_data_type.is_numeric_type(self.data[col]):
                C = src.edaplore.typclass.type_numeric.Numeric(self.data[col], col)
                self.numeric[col] = C
                self.data_classes.append(C)
                continue

            if define_data_type.is_categorical_type(self.data[col]) or self.data[col].name in cat_cols:
                C = src.edaplore.typclass.type_categorical.Categorical(self.data[col], col)
                self.categorical[col] = C
                self.data_classes.append(C)
                continue
