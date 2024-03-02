# TODO:
# - Create a repository on GitHib
# - Push this code
# - Set as enviroment variable the paths and the file names
# - Set as constants the columns names

import os
import pandas as pd
import utils.constants as C

SOURCE_PATH = os.environ[C.PATH_ENV_VARIABLE]
OUTPUT_PATH = os.path.join(SOURCE_PATH, 'results')
EXPENSES_FILENAME = os.environ[C.EXPENSES_ENV_VARIABLE]
SUMMARY_BY_MONTH_FILENAME = os.environ[C.SUMMARY_BY_MONTH_ENV_VARIABLE]
SUMMARY_BY_TYPE_FILENAME = os.environ[C.SUMMARY_BY_TYPE_ENV_VARIABLE]

to_save = True

if __name__ == '__main__':

    expenses_df = pd.read_csv(os.path.join(SOURCE_PATH, EXPENSES_FILENAME))

    expenses_df[C.MONTH_COL] = expenses_df[C.DATE_COL].apply(lambda x: x.split('-')[1])
    MONTH_MAP = dict(map(lambda i, j: (i, j), expenses_df[C.MONTH_COL].unique(), range(1, 13)))
    expenses_df[C.MONTH_NUMBER_COL] = expenses_df[C.MONTH_COL].apply(lambda x: MONTH_MAP[x])
    expenses_df[C.TRANSACTION_COL] = expenses_df[C.TRANSACTION_COL].apply(lambda x: float(x.replace(',', '.')))

    # Select the costs
    costs_df = expenses_df[expenses_df[C.TRANSACTION_COL] < 0].reset_index(drop=True)
    # Select the revenues
    revenues = expenses_df[expenses_df[C.TRANSACTION_COL] > 0].reset_index(drop=True)

    # Summary of the cost
    summary_by_month = costs_df.groupby(
        [C.MONTH_COL, C.MONTH_NUMBER_COL, C.TRANSACTION_TYPE_COL])[C.TRANSACTION_COL].sum().reset_index()
    summary_by_month = summary_by_month.sort_values(
        by=[C.MONTH_NUMBER_COL, C.TRANSACTION_TYPE_COL]).reset_index(drop=True)

    # TODO:
    # - Average cost per month
    # - Month where the cost was the lowest
    # - Month where the cost was the highest

    summary_by_type = costs_df.groupby(
        [C.TRANSACTION_TYPE_COL])[C.TRANSACTION_COL].sum().reset_index().sort_values(
            by=[C.TRANSACTION_TYPE_COL]).reset_index(drop=True)

    if to_save:

        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)

        summary_by_month.to_csv(os.path.join(OUTPUT_PATH, SUMMARY_BY_MONTH_FILENAME), index=False)
        summary_by_type.to_csv(os.path.join(OUTPUT_PATH, SUMMARY_BY_TYPE_FILENAME), index=False)
