import unittest
from pydantic import ValidationError

from core.models import GiphyResponse, MultipleGiphyResponse


class TestGiphyModels(unittest.TestCase):

    def test_giphy_response_valid_url(self):
        """Test that GiphyResponse correctly handles a valid GIF URL."""
        data = {"gif_url": "https://media.giphy.com/media/jXD7k3dmJIWp6/giphy.gif"}
        response = GiphyResponse(**data)
        self.assertEqual(
            response.gif_url, "https://media.giphy.com/media/jXD7k3dmJIWp6/giphy.gif"
        )

    def test_giphy_response_no_url(self):
        """Test that GiphyResponse correctly handles the case where no GIF URL is provided."""
        data = {}
        response = GiphyResponse(**data)
        self.assertIsNone(response.gif_url)

    def test_giphy_response_invalid_type(self):
        """Test that GiphyResponse raises ValidationError for an invalid gif_url type."""
        data = {"gif_url": 123}
        with self.assertRaises(ValidationError):
            GiphyResponse(**data)

    def test_multiple_giphy_response_valid_urls(self):
        """Test that MultipleGiphyResponse correctly handles a list of valid GIF URLs."""
        urls = [
            "https://media.giphy.com/media/jXD7k3dmJIWp6/giphy.gif",
            "https://media.giphy.com/media/fe4dDMD2cAU5j6FHYb/giphy.gif",
        ]
        data = {"gif_urls": urls}
        response = MultipleGiphyResponse(**data)
        self.assertEqual(response.gif_urls, urls)
        self.assertIsInstance(response.gif_urls, list)
        for url in response.gif_urls:
            self.assertIsInstance(url, str)

    def test_multiple_giphy_response_empty_urls(self):
        """Test that MultipleGiphyResponse correctly handles an empty list of GIF URLs."""
        data = {"gif_urls": []}
        response = MultipleGiphyResponse(**data)
        self.assertEqual(response.gif_urls, [])
        self.assertIsInstance(response.gif_urls, list)

    def test_multiple_giphy_response_no_urls(self):
        """Test that MultipleGiphyResponse correctly handles the case where no GIF URLs are provided."""
        data = {}
        response = MultipleGiphyResponse(**data)
        self.assertIsNone(response.gif_urls)

    def test_multiple_giphy_response_invalid_type(self):
        """Test that MultipleGiphyResponse raises ValidationError for an invalid gif_urls type."""
        data = {"gif_urls": "not a list"}
        with self.assertRaises(ValidationError):
            MultipleGiphyResponse(**data)

    def test_multiple_giphy_response_invalid_url_in_list(self):
        """Test that MultipleGiphyResponse raises ValidationError for an invalid URL type in the list."""
        data = {"gif_urls": ["valid_url", 123]}
        with self.assertRaises(ValidationError):
            MultipleGiphyResponse(**data)


if __name__ == "__main__":
    unittest.main()
