import unittest
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from infrastructure.api import app, get_giphy_service


class TestGiphyEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_get_giphy_gif_success(self):
        """Test successful retrieval of a single GIF URL."""
        mock_giphy_service = MagicMock(spec=get_giphy_service())
        mock_giphy_service.get_gif_by_text.return_value = (
            "https://example.com/single.gif"
        )
        app.dependency_overrides[get_giphy_service] = lambda: mock_giphy_service

        response = self.client.get("/get_giphy_gif?text=cats")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"gif_url": "https://example.com/single.gif"})

        app.dependency_overrides = {}  # Reset overrides

    def test_get_giphy_gif_not_found(self):
        """Test the case where no GIF is found for the given text."""
        mock_giphy_service = MagicMock(spec=get_giphy_service())
        mock_giphy_service.get_gif_by_text.return_value = None
        app.dependency_overrides[get_giphy_service] = lambda: mock_giphy_service

        response = self.client.get("/get_giphy_gif?text=nonexistent")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(), {"detail": "No GIF was found for the text: 'nonexistent'"}
        )

        app.dependency_overrides = {}  # Reset overrides

    def test_get_giphy_gifs_success(self):
        """Test successful retrieval of multiple GIF URLs."""
        mock_giphy_service = MagicMock(spec=get_giphy_service())
        mock_giphy_service.get_gif_by_text.return_value = [
            "https://example.com/gif1.gif",
            "https://example.com/gif2.gif",
        ]
        app.dependency_overrides[get_giphy_service] = lambda: mock_giphy_service

        response = self.client.get("/get_giphy_gifs?text=dogs&limit=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "gif_urls": [
                    "https://example.com/gif1.gif",
                    "https://example.com/gif2.gif",
                ]
            },
        )

        app.dependency_overrides = {}  # Reset overrides

    def test_get_giphy_gifs_not_found(self):
        """Test the case where no GIFs are found for the given text."""
        mock_giphy_service = MagicMock(spec=get_giphy_service())
        mock_giphy_service.get_gif_by_text.return_value = []
        app.dependency_overrides[get_giphy_service] = lambda: mock_giphy_service

        response = self.client.get("/get_giphy_gifs?text=unlikely")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(), {"detail": "No GIFs were found for the text: 'unlikely'"}
        )

        app.dependency_overrides = {}  # Reset overrides

    def test_get_giphy_gifs_with_optional_params(self):
        """Test retrieval of multiple GIFs with optional parameters."""
        mock_giphy_service = MagicMock(spec=get_giphy_service())
        mock_giphy_service.get_gif_by_text.return_value = [
            "https://example.com/rated_gif.gif"
        ]
        app.dependency_overrides[get_giphy_service] = lambda: mock_giphy_service

        response = self.client.get("/get_giphy_gifs?text=safe&limit=1&rating=g&lang=en")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"gif_urls": ["https://example.com/rated_gif.gif"]}
        )

        mock_giphy_service.get_gif_by_text.assert_called_once_with(
            "safe", limit=1, rating="g", lang="en"
        )  # Arguments passed positionally

        app.dependency_overrides = {}  # Reset overrides


if __name__ == "__main__":
    unittest.main()
