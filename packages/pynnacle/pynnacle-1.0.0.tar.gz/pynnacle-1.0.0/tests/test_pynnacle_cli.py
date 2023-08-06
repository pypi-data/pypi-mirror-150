#!/usr/bin/env python3
"""Tests for CLI scripts"""

# Core Library modules
import sys

# Third party modules
from click.testing import CliRunner

# First party modules
from pynnacle import pynnacle_cli


def test_author() -> None:
    """Test function to assert correct author name."""
    runner = CliRunner()
    result = runner.invoke(pynnacle_cli.author)
    assert result.exit_code == 0
    assert result.output == "Author name: Stephen R A King\n"


def test_author_verbose() -> None:
    """Test function to assert correct verbose author name."""
    runner = CliRunner()
    result = runner.invoke(pynnacle_cli.author, ["--verbose"])
    assert result.exit_code == 0
    assert (
        result.output == "Author name: Stephen R A King\n"
        "Author eMail: name@isp.com\n"
    )


def test_author_help() -> None:
    """Test function to assert correct author help text."""
    runner = CliRunner()
    result = runner.invoke(pynnacle_cli.author, ["--help"])
    assert result.exit_code == 0
    assert "  Display Author Name" in result.output
