import os

import pandas as pd

from parsers.input import input_parser
from constants.columns import (
    DATE_COL,
    YEAR_COL,
    MONTH_COL,
    TRANSACTION_COL,
    TRANSACTION_TYPE_COL,
    NOTE_COL
)
from constants.filenames import (
    ANALYSIS_FOLDER_NAME,
    COSTS_SUMMARY_BY_MONTH_AND_TYPE,
    COSTS_SUMMARY_BY_MONTH,
    COSTS_SUMMARY_BY_TYPE,
    REVENUES_SUMMARY_BY_MONTH
)


def main():

    args = input_parser()

    expenses_df = pd.read_csv(args.path, dtype={DATE_COL: str, TRANSACTION_COL: float, TRANSACTION_TYPE_COL: str, NOTE_COL: str})

    expenses_df[YEAR_COL] = expenses_df[DATE_COL].apply(lambda x: x.split('-')[0])
    expenses_df[MONTH_COL] = expenses_df[DATE_COL].apply(lambda x: x.split('-')[1])

    # Select the costs
    costs_df = expenses_df[expenses_df[TRANSACTION_COL] < 0].reset_index(drop=True)
    # Select the revenues
    revenues_df = expenses_df[expenses_df[TRANSACTION_COL] > 0].reset_index(drop=True)

    # Summary of the costs
    costs_summary_by_month = costs_df.groupby(
        [MONTH_COL])[TRANSACTION_COL].agg(['sum', 'mean']).reset_index().sort_values(
            by=[MONTH_COL]).reset_index(drop=True)

    costs_summary_by_month_and_type = costs_df.groupby(
        [MONTH_COL, TRANSACTION_TYPE_COL])[TRANSACTION_COL].agg(['sum', 'mean']).reset_index().sort_values(
            by=[MONTH_COL, TRANSACTION_TYPE_COL]).reset_index(drop=True)

    costs_summary_by_type = costs_df.groupby(
        [TRANSACTION_TYPE_COL])[TRANSACTION_COL].sum().reset_index().sort_values(
            by=[TRANSACTION_TYPE_COL]).reset_index(drop=True)

    # Summary of the costs
    revenues_summary_by_month = revenues_df.groupby(
        [MONTH_COL])[TRANSACTION_COL].agg(['sum', 'mean']).reset_index().sort_values(
            by=[MONTH_COL]).reset_index(drop=True)

    # Analysis
    # costs_summary_by_month_analysis = costs_summary_by_month.describe()
    # costs_summary_by_month_and_type_analysis = costs_summary_by_month_and_type.describe()
    # costs_summary_by_type_analysis = costs_summary_by_type.describe()

    if args.save:

        output_path = os.path.join(os.path.dirname(args.path), ANALYSIS_FOLDER_NAME)
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        fiscal_year = list(expenses_df[YEAR_COL].unique())[0]

        costs_summary_by_month.to_csv(
            os.path.join(
                output_path,
                f'{fiscal_year}-{COSTS_SUMMARY_BY_MONTH}'), index=False)

        costs_summary_by_month_and_type.to_csv(
            os.path.join(
                output_path,
                f'{fiscal_year}-{COSTS_SUMMARY_BY_MONTH_AND_TYPE}'), index=False)
        costs_summary_by_type.to_csv(
            os.path.join(
                output_path,
                f'{fiscal_year}-{COSTS_SUMMARY_BY_TYPE}'), index=False)

        revenues_summary_by_month.to_csv(
            os.path.join(
                output_path,
                f'{fiscal_year}-{REVENUES_SUMMARY_BY_MONTH}'), index=False)


if __name__ == '__main__':
    main()
