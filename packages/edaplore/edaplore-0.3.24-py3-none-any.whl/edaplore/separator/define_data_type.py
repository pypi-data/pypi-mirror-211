import pandas as pd
# from edaplore.typclass import names


def is_data_frame(data):
    """
    Checks if the input is a DataFrame.

    :param data: The variable to be checked.
    :return: Boolean indicating whether the input is a DataFrame.
    """
    return isinstance(data, pd.DataFrame)


def is_series(data):
    """
    Checks if the input is a Series.

    :param data: The variable to be checked.
    :return: Boolean indicating whether the input is a Series.
    """
    return isinstance(data, pd.Series)


def is_categorical_type(data):
    """
    Checks if the input Series has a Categorical dtype.

    :param data: A pandas Series.
    :return: Boolean indicating whether the Series has a Categorical dtype.
    """
    return pd.api.types.is_categorical_dtype(data.dtype)


def is_numeric_type(data):
    """
    Checks if the input Series is Numeric, but not Boolean (values are not only 0 and 1).

    :param data: A pandas Series.
    :return: Boolean indicating whether the Series is Numeric but not Boolean.
    """
    if pd.api.types.is_numeric_dtype(data.dtype):
        if set(data.unique()).issubset({0, 1}):
            return False
        return True
    return False


def is_bool_type(data):
    """
    Checks if the input Series is Boolean (Boolean dtype or numeric with values 0 and 1).

    :param data: A pandas Series.
    :return: Boolean indicating whether the Series is Boolean.
    """
    if pd.api.types.is_bool_dtype(data.dtype):
        return True
    if pd.api.types.is_numeric_dtype(data.dtype):
        if set(data.unique()).issubset({0, 1}):
            return True
    return False


# def define_type_of_series(data):
#     """
#     Determines the type of a Series according to a custom classification.
#
#     :param data: A pandas Series.
#     :return: A string indicating the custom-defined type of the Series. If the input is not a Series, returns None.
#     """
#     if not is_series(data):
#         return None
#     if is_categorical_type(data):
#         return names.categorical
#     if is_numeric_type(data):
#         return names.numeric
#     if is_bool_type(data):
#         return names.bolean
