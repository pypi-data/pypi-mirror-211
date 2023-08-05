import pandas as pd

numeric = 'numeric'
bolean = 'bool'
categorical = 'category'
date_or_time = 'datetime'


numeric_types = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
bool_type = [bool]
categorical_type = ['object', pd.core.dtypes.dtypes.CategoricalDtype]