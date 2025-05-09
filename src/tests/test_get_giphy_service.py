import unittest
from unittest.mock import patch

from infrastructure.api import get_giphy_service
from infrastructure.giphy_adapter import GiphyAPIAdapter
from core.giphy_port import GiphyPort


class TestGetGiphyService(unittest.TestCase):

    def test_get_giphy_service_returns_giphy_api_adapter_instance(self):
        """
        Test that the get_giphy_service function returns an instance of GiphyAPIAdapter.
        """
        service = get_giphy_service()
        self.assertIsInstance(service, GiphyAPIAdapter)
        self.assertIsInstance(service, GiphyPort)

    @patch("os.getenv")
    def test_giphy_api_adapter_initialization_from_env(self, mock_getenv):
        """
        Test that GiphyAPIAdapter initializes its API key from environment variables if not provided.
        """
        mock_getenv.return_value = "test_api_key_from_env"
        adapter = GiphyAPIAdapter()
        self.assertEqual(adapter.api_key, "test_api_key_from_env")
        mock_getenv.assert_called_once_with("GIPHY_API_KEY")

    def test_giphy_api_adapter_initialization_with_provided_key(self):
        """
        Test that GiphyAPIAdapter initializes its API key with the provided value.
        """
        provided_key = "test_provided_api_key"
        adapter = GiphyAPIAdapter(api_key=provided_key)
        self.assertEqual(adapter.api_key, provided_key)

    def test_giphy_api_adapter_initialization_no_key_raises_error(self):
        """
        Test that GiphyAPIAdapter raises ValueError if no API key is provided and not found in env.
        """
        with patch("os.getenv", return_value=None):
            with self.assertRaises(ValueError) as context:
                GiphyAPIAdapter()
            self.assertIn(
                "La API Key de Giphy no se ha proporcionado ni se ha encontrado en las variables de entorno (GIPHY_API_KEY).",
                str(context.exception),
            )  # NOQA


if __name__ == "__main__":
    unittest.main()
