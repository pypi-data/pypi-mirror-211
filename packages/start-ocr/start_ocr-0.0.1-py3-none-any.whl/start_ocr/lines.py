import cv2
import numpy as np
from pdfplumber.page import Page

from .coordinates import CoordinatedImage
from .slice import get_contours

PERCENT_OF_MAX_PAGE = 0.94


def page_width_lines(im: np.ndarray) -> list[CoordinatedImage]:
    """Filter long horizontal lines:

    1. Edges of lines must be in the left of the page and on the right of the page
    2. Each line must be at least 1/2 the page width

    Examples:
        >>> from start_ocr import get_page_and_img
        >>> from pathlib import Path
        >>> page, im = get_page_and_img(Path().cwd() / "tests" / "data" / "test.pdf", 0)
        >>> res = page_width_lines(im)
        >>> len(res) # only one image matches the filter
        1

    """
    _, im_w, _ = im.shape
    results = []
    contours = get_contours(
        im=im,
        rectangle_size=(10, 10),
        test_dilation=True,
        test_dilated_image="temp/dilated.png",
    )
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        filtering_criteria = [
            w > im_w / 2,  # width greater than half
            x < im_w / 3,  # edge of line on first third
            (x + w) > im_w * (2 / 3),  # edge of line on last third
        ]
        if all(filtering_criteria):
            obj = CoordinatedImage(im, x, y, w, h)
            obj.greenbox()
            results.append(obj)
    cv2.imwrite("temp/boxes.png", im)
    return results


def footnote_lines(im: np.ndarray) -> list[CoordinatedImage]:
    """Filter short horizontal lines:

    1. > width of 400 pixels
    2. height of less than 44 pixels, using the test pdf, any larger than 44 pixels will make this include text as well.

    The footer represents content below the main content. This is also
    called the annex of the page.

    This detects a short line in the lower half of the page that has at least a width
    of 400 pixels and a , indicating a narrow box
    (as dilated by openCV). Text found below this box represents the annex.

    Examples:
        >>> from start_ocr import get_page_and_img
        >>> from pathlib import Path
        >>> page, im = get_page_and_img(Path().cwd() / "tests" / "data" / "test.pdf", 0)
        >>> res = footnote_lines(im)
        >>> len(res) # only one image matches the filter
        1

    """  # noqa: E501
    _, im_w, _ = im.shape
    contours = get_contours(
        im=im,
        rectangle_size=(50, 10),
        test_dilation=True,
        test_dilated_image="temp/dilated.png",
    )
    results = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        filtering_criteria = [
            x < (im_w / 2),
            (x + w) < (im_w / 2),
            (im_w / 2) > w > 400,
            h < 44,
        ]
        if all(filtering_criteria):
            obj = CoordinatedImage(im, x, y, w, h)
            obj.greenbox()
            results.append(obj)
    cv2.imwrite("temp/boxes.png", im)
    return results


def show_contours(im: np.ndarray, rectangle_size: tuple[int, int]) -> list:
    contours = get_contours(
        im,
        rectangle_size,
        test_dilation=True,
        test_dilated_image="temp/dilated.png",
    )
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        obj = CoordinatedImage(im, x, y, w, h)
        obj.greenbox()
    cv2.imwrite("temp/boxes.png", im)
    return contours


def get_page_end(im: np.ndarray, page: Page) -> tuple[float, float | None]:
    """Given an `im`, detect footnote line of annex and return relevant points in the y-axis as a tuple.

    Scenario | Description | y0 | y1
    :--:|:-- |:--:|:--:
    Footnote line exists | Page contains footnotes | int or float | int or float signifying end of page
    Footnote line absent | Page does not contain footnotes | int or float signifying end of page | `None`

    Examples:
        >>> from start_ocr import get_page_and_img
        >>> from pathlib import Path
        >>> page, im = get_page_and_img(Path().cwd() / "tests" / "data" / "test.pdf", 0)
        >>> res = get_page_end(im, page)
        >>> res
        (833.52, 879.8399999999999)

    Args:
        im (numpy.ndarray): the openCV image that may contain a footnote line
        page (Page): the pdfplumber.page.Page based on `im`

    Returns:
        tuple[float, float | None]: The annex line's y-axis (if it exists) and
            The page's end content line
    """  # noqa: E501
    im_h, _, _ = im.shape
    lines = footnote_lines(im)
    y1 = PERCENT_OF_MAX_PAGE * page.height
    if lines:
        fn_line_end = lines[0].y / im_h
        y0 = fn_line_end * page.height
        return y0, y1
    return y1, None
