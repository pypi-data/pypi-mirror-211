import base64


def string_to_file(
    text: str,
    filename: str = "myfile",
    download_text: str = "Download File",
) -> str:
    """
    Generates a downloadable text file containing the given text.

    Args:
        text (str): Text to be downloaded
        filename (str, optional): Name of the download file. (Defaults to "myfile")
        download_text (str, optional): Text to be displayed as the download link. (Defaults to "Download File")

    Raises:
        TypeError: If the input text is not a string.

    Returns:
        str: HTML download link
    """

    # Verify that text is a string
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Encode the text
    encoded_text = base64.b64encode(text.encode()).decode()
    mime_type = "data:text/plain;base64,"
    encoded_data = mime_type + encoded_text

    # Return the download link
    return f"<a href='{encoded_data}' download='{filename}.txt'>{download_text}</a>"
