from collections.abc import Iterator
from pathlib import Path

import cv2
import numpy
import pdfplumber
from pdfplumber.page import Page


def get_img_from_page(page: Page) -> numpy.ndarray:
    """Converts a `pdfplumber.Page` to an OpenCV formatted image file.

    Args:
        page (Page): pdfplumber.Page

    Returns:
        numpy.ndarray: OpenCV format.
    """
    obj = page.to_image(resolution=300).original
    return cv2.cvtColor(numpy.array(obj), cv2.COLOR_RGB2BGR)


def get_page_and_img(pdfpath: str | Path, index: int) -> tuple[Page, numpy.ndarray]:
    """Each page of a PDF file, can be opened and cropped via `pdfplumber`.
    To parse, it's necessary to convert the pdf to an `opencv` compatible-image format
    (i.e. `numpy.ndarray`). This function converts a `Path` object into a pair of objects:

    1. the first part is a `pdfplumber.Page`
    2. the second part is an openCV image, i.e. `numpy.ndarray`

    Examples:
        >>> import numpy
        >>> page, im = get_page_and_img(Path().cwd() / "tests" / "data" / "test.pdf", 0) # 0 marks the first page
        >>> page.page_number # the first page
        1
        >>> isinstance(page, Page)
        True
        >>> isinstance(im, numpy.ndarray)
        True
        >>> page.pdf.close()

    Args:
        pdfpath (str | Path): Path to the PDF file.
        index (int): Zero-based index that determines the page number.

    Returns:
        tuple[Page, numpy.ndarray]: Page identified by `index`  with image of the
            page  (in numpy format) that can be manipulated.
    """  # noqa: E501
    with pdfplumber.open(pdfpath) as pdf:
        page = pdf.pages[index]
        img = get_img_from_page(page)
        return page, img


def get_pages_and_imgs(
    pdfpath: str | Path,
) -> Iterator[tuple[Page, numpy.ndarray]]:
    """Get page and images in sequential order.

    Examples:
        >>> results = get_pages_and_imgs(Path().cwd() / "tests" / "data" / "test.pdf")
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
        Iterator[tuple[Page, numpy.ndarray]]: Pages with respective images
    """
    with pdfplumber.open(pdfpath) as pdf:
        index = 0
        while index < len(pdf.pages):
            page = pdf.pages[index]
            yield page, get_img_from_page(page)
            index += 1


def get_reverse_pages_and_imgs(
    pdfpath: str | Path,
) -> Iterator[tuple[Page, numpy.ndarray]]:
    """Start from end page to get to first page to determine terminal values.

    Examples:
        >>> x = Path().cwd() / "tests" / "data" / "test.pdf"
        >>> results = get_reverse_pages_and_imgs(x)
        >>> result = next(results)
        >>> type(result)
        <class 'tuple'>
        >>> isinstance(result[0], Page)
        True
        >>> result[0].page_number == len(pdfplumber.open(x).pages) # last first
        True

    Args:
        pdfpath (Page | Path): Path to the PDF file.

    Yields:
        Iterator[tuple[Page, numpy.ndarray]]: Pages with respective images
    """  # noqa: E501
    with pdfplumber.open(pdfpath) as pdf:
        index = len(pdf.pages) - 1
        while index >= 0:
            page = pdf.pages[index]
            yield page, get_img_from_page(page)
            index -= 1
