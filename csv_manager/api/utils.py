'''Supporter variables and functions for api app'''


df_filtering_functions = {
    'gt': lambda dtf, col, value: dtf[dtf[col] > value],
    'ge': lambda dtf, col, value: dtf[dtf[col] >= value],
    'lt': lambda dtf, col, value: dtf[dtf[col] < value],
    'le': lambda dtf, col, value: dtf[dtf[col] <= value],
    'eq': lambda dtf, col, value: dtf[dtf[col] == value],
    'ne': lambda dtf, col, value: dtf[dtf[col] != value],
    'contains':
        lambda dtf, col, value: dtf[dtf[col].str.contains(value)],
    'is_null':
    lambda dtf, col, value: dtf[dtf[col].isnull() if value == 'True'
                                else dtf[col].notnull()],
}
