"""Tests for the HTML parser module."""

import os
import unittest
from pathlib import Path

from src.core.models import Gag
from src.core.parser import HtmlParser


class TestHtmlParser(unittest.TestCase):
    """Test cases for the HTML parser."""

    def setUp(self):
        """Set up the test case."""
        # Find the test data file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_file = os.path.join(current_dir, "test_9gag_data_simplified.html")

        # Ensure the test file exists
        self.assertTrue(
            Path(self.test_file).exists(), f"Test file not found: {self.test_file}"
        )

    def test_read_html_file(self):
        """Test reading an HTML file."""
        # Read the HTML file
        soup = HtmlParser.read_html_file(self.test_file)

        # Check that we got a BeautifulSoup object back
        self.assertIsNotNone(soup)

        # Verify the title matches what we expect
        title = soup.find("title").text
        self.assertEqual(title, "9GAG Test Data")

    def test_extract_saved_gags(self):
        """Test extracting saved gags from HTML."""
        # Extract gags with only saved selected
        gags = HtmlParser.parse_file(
            self.test_file, saved_gags=True, upvoted_gags=False
        )

        # Verify we got the right number of gags
        self.assertEqual(len(gags), 5, f"Expected 5 saved gags, got {len(gags)}")

        # Verify the IDs are correct
        expected_ids = ["a1PGwdR", "aGgM5ow", "aVgMoZ2", "aZpe6RG", "aBgVEb5"]
        actual_ids = [gag.id for gag in gags]
        self.assertListEqual(actual_ids, expected_ids)

        # Verify the titles are correct
        self.assertEqual(gags[0].title, "Sometimes, history hurts.")
        self.assertEqual(gags[2].title, "Netflix and chill")

    def test_extract_upvoted_gags(self):
        """Test extracting upvoted gags from HTML."""
        # Extract gags with only upvoted selected
        gags = HtmlParser.parse_file(
            self.test_file, saved_gags=False, upvoted_gags=True
        )

        # Verify we got the right number of gags
        self.assertEqual(len(gags), 8, f"Expected 8 upvoted gags, got {len(gags)}")

        # Check a few specific gags
        self.assertIn(
            "a1Pjqv2", [gag.id for gag in gags], "Expected gag ID a1Pjqv2 not found"
        )
        self.assertIn(
            "aW4nMjA", [gag.id for gag in gags], "Expected gag ID aW4nMjA not found"
        )

        # Find and verify a specific gag
        test_gag = next((gag for gag in gags if gag.id == "aW4nMjA"), None)
        self.assertIsNotNone(test_gag, "Couldn't find test gag with ID aW4nMjA")
        self.assertEqual(test_gag.title, "The real MVP")

    def test_extract_all_gags(self):
        """Test extracting both saved and upvoted gags."""
        # Extract all gags
        gags = HtmlParser.parse_file(self.test_file, saved_gags=True, upvoted_gags=True)

        # Verify we got the right number of gags (5 saved + 8 upvoted = 13)
        self.assertEqual(len(gags), 13, f"Expected 13 total gags, got {len(gags)}")

        # Check that both saved and upvoted gags are included
        self.assertIn(
            "a1PGwdR",
            [gag.id for gag in gags],
            "Expected saved gag ID a1PGwdR not found",
        )
        self.assertIn(
            "aW4nMjA",
            [gag.id for gag in gags],
            "Expected upvoted gag ID aW4nMjA not found",
        )

    def test_error_handling(self):
        """Test error handling for non-existent files."""
        # Try to parse a non-existent file
        with self.assertRaises(FileNotFoundError):
            HtmlParser.parse_file("non_existent_file.html")


if __name__ == "__main__":
    unittest.main()
