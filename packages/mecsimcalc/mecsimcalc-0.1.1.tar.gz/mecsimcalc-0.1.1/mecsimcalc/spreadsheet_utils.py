import io
import base64
import pandas as pd
from typing import Union, Tuple

from general_utils import input_to_file, metadata_to_filetype


def file_to_dataframe(file: io.BytesIO) -> pd.DataFrame:
    """
    Converts a base64 encoded file data into a pandas DataFrame.

    Args:
        input_file (io.BytesIO): Decoded file data.

    Raises:
        pd.errors.ParserError: If the file type is not supported.

    Returns:
        pd.DataFrame: Returns a DataFrame created from the file data.
    """

    # try to read the file as a CSV, if that fails try to read it as an Excel file
    try:
        df = pd.read_csv(file)
    except Exception:
        try:
            df = pd.read_excel(file)
        except Exception as e:
            raise pd.errors.ParserError("File Type Not Supported") from e

    return df


def input_to_dataframe(
    input_file: str, get_file_type: bool = False
) -> Union[pd.DataFrame, Tuple[pd.DataFrame, str]]:
    """
    Converts a base64 encoded file data into a pandas DataFrame.

    Args:
        input_file (str): The base64 encoded file data.
        get_file_type (bool, optional): If True, the function also returns the file type (Defaults to False)

    Returns:
        Union[pd.DataFrame, Tuple[pd.DataFrame, str]]: If get_file_type is False, returns a DataFrame created from the file data.
                                                       If get_file_type is True, returns a tuple containing the DataFrame and the file type.
    """

    file_data, metadata = input_to_file(input_file, metadata=True)

    # if get_file_type is True return the DataFrame and the file type,
    # otherwise just return the DataFrame
    if get_file_type:
        return file_to_dataframe(file_data), metadata_to_filetype(metadata)
    else:
        return file_to_dataframe(file_data)


def print_dataframe(
    df: pd.DataFrame,
    download: bool = False,
    download_text: str = "Download Table",
    download_file_name: str = "mytable",
    download_file_type: str = "csv",
) -> Union[str, Tuple[str, str]]:
    """
    Creates an HTML table from a pandas DataFrame and optionally provides a download link for the table.

    Args:
        df (pd.DataFrame): The DataFrame to be converted.
        download (bool, optional): If True, the function also provides a download link. (Defaults to False)
        download_text (str, optional): The text to be displayed on the download link. (Defaults to "Download Table")
        download_file_name (str, optional): The name of the downloaded file. (Defaults to "myfile")
        download_file_type (str, optional): The file type of the download. (Defaults to "csv")

    Returns:
        Union[str, Tuple[str, str]]: If download is False, returns the HTML table as a string.
                                      If download is True, returns a tuple of the HTML table and the HTML download link as strings.
    """

    # create HTML table if download is False
    if not download:
        return df.to_html()

    download_file_type = download_file_type.lower()

    # Create a buffer
    buf = io.BytesIO()

    if download_file_type in {
        "excel",
        "xlsx",
        "xls",
        "xlsm",
        "xlsb",
        "odf",
        "ods",
        "odt",
    }:
        # create excel file and download link
        df.to_excel(buf, index=False)
        buf.seek(0)  # move the cursor to the beginning of the file

        encoded_data = (
            "data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,"
            + base64.b64encode(buf.read()).decode()
        )
    else:
        # create csv file and download link
        df.to_csv(buf, index=False)
        buf.seek(0)

        encoded_data = "data:text/csv;base64," + base64.b64encode(buf.read()).decode()

    # Create the download link
    download_link = f"<a href='{encoded_data}' download='{download_file_name}.{download_file_type}'>{download_text}</a>"

    return df.to_html(), download_link
