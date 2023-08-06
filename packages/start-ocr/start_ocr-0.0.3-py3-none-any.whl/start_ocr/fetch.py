from collections.abc import Iterator
from pathlib import Path

import cv2
import numpy as np
import pdfplumber
import pytesseract
from pdfplumber.page import Page


def paged_text(page: Page) -> str:
    """pdfplumber features an experimental setting `layout=True`.
    Used here in tandem with another setting `keep_blank_chars` to monitor
    line breaks.

    Args:
        page (Page): pdfplumber Page.

    Returns:
        str: text found from the page.
    """
    return page.extract_text(layout=True, keep_blank_chars=True).strip()


def imaged_text(page: Page) -> str:
    """Use pytesseract to extract text from the apge by first
    converting the page to numpy format."""
    img = get_img_from_page(page)
    text = pytesseract.image_to_string(img)
    return text.strip()


def get_img_from_page(page: Page) -> np.ndarray:
    """Converts a `pdfplumber.Page` to an OpenCV formatted image file.

    Args:
        page (Page): pdfplumber.Page

    Returns:
        np.ndarray: OpenCV format.
    """
    obj = page.to_image(resolution=300).original
    im = np.array(obj)
    img = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    return img


def get_page_and_img(pdfpath: str | Path, index: int) -> tuple[Page, np.ndarray]:
    """Each page of a PDF file, can be opened and cropped via `pdfplumber`.
    To parse, it's necessary to convert the pdf to an `opencv` compatible-image format
    (i.e. `np.ndarray`). This function converts a `Path` object into a pair of objects:

    1. the first part is a `pdfplumber.Page`
    2. the second part is an openCV image, i.e. `np.ndarray`

    Examples:
        >>> page, im = get_page_and_img(Path().cwd() / "tests" / "data" / "lorem_ipsum.pdf", 0) # 0 marks the first page
        >>> page.page_number # the first page
        1
        >>> isinstance(page, Page)
        True
        >>> isinstance(im, np.ndarray)
        True
        >>> page.pdf.close()

    Args:
        pdfpath (str | Path): Path to the PDF file.
        index (int): Zero-based index that determines the page number.

    Returns:
        tuple[Page, np.ndarray]: Page identified by `index`  with image of the
            page  (in np format) that can be manipulated.
    """  # noqa: E501
    with pdfplumber.open(pdfpath) as pdf:
        page = pdf.pages[index]
        img = get_img_from_page(page)
        return page, img


def get_pages_and_imgs(
    pdfpath: str | Path,
) -> Iterator[tuple[Page, np.ndarray]]:
    """Get page and images in sequential order.

    Examples:
        >>> results = get_pages_and_imgs(Path().cwd() / "tests" / "data" / "lorem_ipsum.pdf")
        >>> result = next(results)
        >>> type(result)
        <class 'tuple'>
        >>> isinstance(result[0], Page)
        True
        >>> result[0].page_number == 1 # first
        True

    Args:
        pdfpath (Page | Path): Path to the PDF file.

    Yields:
        Iterator[tuple[Page, np.ndarray]]: Pages with respective images
    """  # noqa: E501
    with pdfplumber.open(pdfpath) as pdf:
        index = 0
        while index < len(pdf.pages):
            page = pdf.pages[index]
            yield page, get_img_from_page(page)
            index += 1


def get_reverse_pages_and_imgs(
    pdfpath: str | Path,
) -> Iterator[tuple[Page, np.ndarray]]:
    """Start from end page to get to first page to determine terminal values.

    Examples:
        >>> x = Path().cwd() / "tests" / "data" / "lorem_ipsum.pdf"
        >>> num_pages = pdfplumber.open(x).pages
        >>> results = get_reverse_pages_and_imgs(x)
        >>> result = next(results)
        >>> type(result)
        <class 'tuple'>
        >>> isinstance(result[0], Page)
        True
        >>> result[0].page_number == len(num_pages) # last page is first
        True

    Args:
        pdfpath (Page | Path): Path to the PDF file.

    Yields:
        Iterator[tuple[Page, np.ndarray]]: Pages with respective images
    """  # noqa: E501
    with pdfplumber.open(pdfpath) as pdf:
        index = len(pdf.pages) - 1
        while index >= 0:
            page = pdf.pages[index]
            yield page, get_img_from_page(page)
            index -= 1
