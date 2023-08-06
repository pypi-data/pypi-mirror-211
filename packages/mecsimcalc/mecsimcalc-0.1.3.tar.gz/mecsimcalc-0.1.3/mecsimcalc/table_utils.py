import pandas as pd
from typing import List


def table_to_dataframe(
    column_headers: List[str], rows: List[List[str]]
) -> pd.DataFrame:
    """
    Create a DataFrame from given rows and column headers

    Args:
        column_headers (List[str]): List of column headers.
        rows (List[List[str]]): List of rows to be converted into a DataFrame. Each row is a list of strings.

    Raises:
        ValueError: If each row does not have the same length as the column headers.

    Return:
        pd.DataFrame: DataFrame constructed from rows and headers.
    """
    # Ensure that each row has the same length as the column headers
    for row in rows:
        if len(row) != len(column_headers):
            raise ValueError("Each row must have the same length as the column headers")

    return pd.DataFrame(rows, columns=column_headers)


def print_table(column_headers: List[str], rows: List[List[str]]) -> str:
    """
    Create an HTML table from given rows and column headers.

    Args:
        column_headers (List[str]): The header for each column.
        rows (List[List[str]]): A list of rows (each row is a list of strings).

    Return:
        str: HTML table.
    """
    # Use DataFrame for table creation
    df = table_to_dataframe(column_headers, rows)

    # Return the table using pandas to_html
    return df.to_html(index=False, border=1, escape=True)
