"""Tests for the `python` module."""

from textwrap import dedent

from markdown import Markdown


def test_output_markdown(md: Markdown) -> None:
    """Assert Markdown is converted to HTML.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes"
            print("**Bold!**")
            ```
            """
        )
    )
    assert html == "<p><strong>Bold!</strong></p>"


def test_output_html(md: Markdown) -> None:
    """Assert HTML is injected as is.

    Parameters:
        md: A Markdown instance (fixture).
    """
    html = md.convert(
        dedent(
            """
            ```python exec="yes" html="yes"
            print("**Bold!**")
            ```
            """
        )
    )
    assert html == "<p>**Bold!**\n</p>"
