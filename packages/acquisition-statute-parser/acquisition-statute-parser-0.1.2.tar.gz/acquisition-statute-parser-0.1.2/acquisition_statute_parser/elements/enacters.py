import re
from typing import Any, Match, Optional, Union

from bs4 import BeautifulSoup, NavigableString, PageElement


def pre_singular_enacter_mark(
    elem: PageElement,
) -> bool | Match | None:
    NOW_THEREFORE_MARK = re.compile(
        r"""
            NOW
            \,
            \s*
            THEREFORE
            \,
            \s*
            I\,
        """,
        re.X,
    )
    return (
        isinstance(elem.next_element, NavigableString)
        and elem.next_element is not None
        and NOW_THEREFORE_MARK.search(elem.next_element)
    )


def pre_collegiate_enacter_mark(
    elem: PageElement,
) -> bool | Match | None:
    """Get elements before the phrase 'Be it enacted', etc."""
    GENERAL_ENACTING_MARK = re.compile(
        r"""
        ^ # start
        \s*
        (
            (
                Be|
                By # mistyped 'By' (should be 'Be')
            )
            \s+
            (
                it
                \s+
            )? # includes missing 'it'
            enacted
        )
        |(
            By
            \s+
            authority
            \s+
            of
            \s+
            the
            \s+
            United
            \s+
            States
        )""",
        re.X,
    )

    return (
        isinstance(elem.next_element, NavigableString)
        and elem.next_element is not None
        and GENERAL_ENACTING_MARK.search(elem.next_element)
    ) or (
        isinstance(elem, NavigableString)
        and GENERAL_ENACTING_MARK.search(elem)
    )


def get_enacter_marker(
    soup: BeautifulSoup, classification: str
) -> PageElement | None:
    """Get the element which marks the start of the 'enacters' of the law.

    Args:
        soup (BeautifulSoup): The html markup of the whole statute
        classification (str): Flag which is either "collegiate" or "singular"

    Returns:
        Optional[PageElement]: The page element (representing the enacter) to be used by the calling function
    """
    pre_marker = None

    if classification == "collegiate":
        pre_marker = soup.find(pre_collegiate_enacter_mark)

    elif classification == "singular":
        pre_marker = soup.find(pre_singular_enacter_mark)

    else:
        return None

    return pre_marker.next_element if pre_marker else None
