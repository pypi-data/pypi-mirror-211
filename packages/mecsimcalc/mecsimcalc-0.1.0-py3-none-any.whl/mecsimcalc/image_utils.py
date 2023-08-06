import base64
import io
from typing import Union, Tuple

from PIL import Image

from general_utils import input_to_file, metadata_to_filetype

# Define a dictionary for file type conversions
file_type_mappings = {"jpg": "jpeg", "tif": "tiff", "ico": "x-icon", "svg": "svg+xml", "jpeg": "jpeg", "tiff": "tiff", "x-icon": "x-icon", "svg+xml": "svg+xml"}


def file_to_PIL(file: io.BytesIO) -> Image.Image:
    """
    Transforms a file into a Pillow Image object.

    Args:
        file (io.BytesIO): A file object containing image data (using open with 'rb' mode)

    Raises:
        ValueError: If the file object doesn't contain image data.

    Returns:
        PIL.Image.Image: An image object created from the file data.
    """

    try:
        return Image.open(file)
    except IOError as e:
        raise ValueError("Invalid file object. It does not contain image data.") from e


def input_to_PIL(
    input_file: str, get_file_type: bool = False
) -> Union[Image.Image, Tuple[Image.Image, str]]:
    """
    Decodes a Base64 encoded string into a Pillow image object, and optionally retrieves the file type.

    Args:
        input_file (str): Base64 encoded string containing image data.
        get_file_type (bool, optional): If True, the function also returns the file type. (Defaults to False)

    Returns:
        Union[PIL.Image.Image, Tuple[PIL.Image.Image, str]]: If get_file_type is False, a Pillow image object is returned.
                                                             If get_file_type is True, a tuple containing the Pillow image object and the file type is returned.
    """
    # Decode the base64 string into a file-like object and extract metadata
    file_data, metadata = input_to_file(input_file, metadata=True)

    # Load the file data into a Pillow Image
    img = file_to_PIL(file_data)

    if get_file_type:
        file_type = metadata_to_filetype(metadata)
        return img, file_type

    return img


def print_img(
    img: Image.Image,
    width: int = 200,
    height: int = 200,
    original_size: bool = False,
    download: bool = False,
    download_text: str = "Download Image",
    download_file_name: str = "myimg",
    download_file_type: str = "png",
) -> Union[str, Tuple[str, str]]:
    """
    Transforms a Pillow image into an HTML image, with an optional download link.

    Args:
        img (PIL.Image.Image): A Pillow image object.
        width (int, optional): The width for the displayed image, in pixels. (Defaults to 200)
        height (int, optional): The height for the displayed image, in pixels. (Defaults to 200)
        original_size (bool, optional): If True, the image will retain its original size. (Defaults to False)
        download (bool, optional): If True, a download link will be provided. (Defaults to False)
        download_text (str, optional): The text for the download link. (Defaults to "Download Image")
        download_file_name (str, optional): The name for the downloaded file. (Defaults to 'myimg')
        download_file_type (str, optional): The file type for the downloaded file. (Defaults to "png")

    Returns:
        Union[str, Tuple[str, str]]: If download is False, an HTML string containing the image is returned.
                                      If download is True, a tuple containing the HTML string for the image and the download link is returned.
    """
    # Create a copy for display, preserving the original image
    display_img = img.copy()

    # Correct file type using the mappings dictionary
    file_type = file_type_mappings.get(
        download_file_type.lower().replace(".", ""), "png"
    )

    # Create metadata with correct file type
    metadata = f"data:image/{file_type};base64,"

    if not original_size:
        display_img.thumbnail((width, height))

    # Get downloadable data (Full Resolution)
    buffer = io.BytesIO()
    img.save(buffer, format=img.format)
    encoded_data = metadata + base64.b64encode(buffer.getvalue()).decode()

    # Get displayable data (Custom Resolution)
    display_buffer = io.BytesIO()

    # Save the display image to the buffer
    display_img.save(display_buffer, format=img.format)

    # Get the encoded display data
    encoded_display_data = (
        metadata + base64.b64encode(display_buffer.getvalue()).decode()
    )

    # Convert Display image to HTML
    image = f"<img src='{encoded_display_data}'>"

    if not download:
        return image

    # Convert full resolution image to an HTML download link
    download_link = f"<a href='{encoded_data}' download='{download_file_name}.{img.format}'>{download_text}</a>"

    return image, download_link
