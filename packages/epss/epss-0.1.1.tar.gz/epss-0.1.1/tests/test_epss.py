#!/usr/bin/env python

"""Tests for `epss` package."""


import unittest
from click.testing import CliRunner

from epss import epss
from epss import cli


class TestEpss(unittest.TestCase):
    """Tests for `epss` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_object(self):
        """Test object creation."""
        client = epss.EPSS()


    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'epss.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
