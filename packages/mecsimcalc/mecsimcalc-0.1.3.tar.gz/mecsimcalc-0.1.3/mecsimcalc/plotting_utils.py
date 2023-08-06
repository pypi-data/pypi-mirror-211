import io
import base64
from typing import Union, Tuple

import matplotlib.pyplot as plt
import matplotlib.figure as figure


def print_plot(
    plot_obj: Union[plt.Axes, figure.Figure],
    width: int = 500,
    dpi: int = 100,
    download: bool = False,
    download_text: str = "Download Plot",
    download_file_name: str = "myplot",
) -> Union[str, Tuple[str, str]]:
    """
    Converts a matplotlib plot into an HTML image tag and optionally provides a download link for the image.

    Args:
        plot_obj (Union[plt.Axes, figure.Figure]): The matplotlib plot to be converted.
        width (int, optional): The width of the image in pixels. (Defaults to 500)
        dpi (int, optional): The DPI of the image. (Defaults to 100)
        download (bool, optional): If set to True, a download link will be provided. (Defaults to False)
        download_text (str, optional): The text to be displayed for the download link. (Defaults to "Download Plot")
        download_file_name (str, optional): The name of the downloaded file. (Defaults to 'myplot')

    Returns:
        Union[str, Tuple[str, str]]: If download is False, returns the HTML image as a string.
                                      If download is True, returns a tuple of the HTML image and the download link as strings.
    """

    # Check if plot_obj is a matplotlib Axes object
    if isinstance(plot_obj, plt.Axes):
        plot_obj = plot_obj.get_figure()

    # Save plot to a buffer in memory
    buffer = io.BytesIO()
    plot_obj.savefig(buffer, format="png", dpi=dpi)

    # Close the plot
    if hasattr(plot_obj, "close"):
        plot_obj.close()

    # Convert the buffer to a base64 string
    buffer.seek(0)
    base64_str = "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode(
        "utf-8"
    )

    # Create the html image tag
    html_img = f"<img src='{base64_str}' width='{width}'>"

    if not download:
        return html_img

    # Create the download link
    download_link = (
        f"<a href='{base64_str}' "
        f"download='{download_file_name}.png'>{download_text}</a>"
    )

    return html_img, download_link
