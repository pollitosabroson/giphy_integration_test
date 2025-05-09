import requests
import os
from dotenv import load_dotenv
from core.giphy_port import GiphyPort
from typing import Optional, List

load_dotenv()


class GiphyAPIAdapter(GiphyPort):
    """
    Adapter class responsible for interacting with the Giphy API to search for GIFs.

    This class implements the GiphyPort interface, providing a concrete way to
    communicate with the Giphy API based on text queries.
    """  # NOQA

    def __init__(self, api_key: Optional[str] = None):
        """
        Initializes the GiphyAPIAdapter with the Giphy API key.

        The API key can be provided directly or will be loaded from the environment
        variable 'GIPHY_API_KEY' using the dotenv library.

        Args:
            api_key (Optional[str], optional): Your Giphy API key. Defaults to None.

        Raises:
            ValueError: If the Giphy API key is not provided and cannot be found
                        in the environment variables.
        """  # NOQA
        if api_key is None:
            self.api_key = os.getenv("GIPHY_API_KEY")
            if self.api_key is None:
                raise ValueError(
                    "The Giphy API Key has not been provided and was not found in the environment variables (GIPHY_API_KEY)."  # NOQA
                )
        else:
            self.api_key = api_key
        self.api_url = "https://api.giphy.com/v1/gifs/search"

    def get_gif_by_text(
        self, text: str, limit: int = 1, rating: str = "g", lang: str = "en"
    ) -> Optional[str | List[str]]:
        """
        Retrieves the URL(s) of GIF(s) from the Giphy API based on a search text.

        Args:
            text (str): The text to search for the GIF. This is the 'q' parameter for the Giphy API.
            limit (int, optional): The maximum number of GIFs to return. This corresponds to the
                                   'limit' parameter of the Giphy API. Defaults to 1.
            rating (str, optional): The content rating filter for the GIFs. This corresponds to the
                                    'rating' parameter of the Giphy API. Defaults to 'g'.
                                    Supported values: 'g', 'pg', 'pg-13', 'r'.
            lang (str, optional): The language code for the search results. This corresponds to the
                                  'lang' parameter of the Giphy API. Defaults to 'en'.
                                  Refer to the Giphy API documentation for supported language codes.

        Returns:
            Optional[str | List[str]]:
                - If `limit` is 1, returns the URL of the first GIF found as a string,
                  or None if no GIFs are found or an error occurs.
                - If `limit` is greater than 1, returns a list of URLs of the found GIFs,
                  or None if no GIFs are found or an error occurs.

        Raises:
            requests.exceptions.RequestException: If there is an error during the communication
                                                 with the Giphy API (e.g., network issues).
            ValueError: If the JSON response from the Giphy API cannot be decoded.
        """  # NOQA
        params = {
            "api_key": self.api_key,
            "q": text,
            "limit": limit,
            "rating": rating,
            "lang": lang,
        }
        try:
            response = requests.get(self.api_url, params=params)
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status()
            data = response.json()
            if data and "data" in data and len(data["data"]) > 0:
                if limit == 1:
                    return data["data"][0]["images"]["original"]["url"]
                else:
                    gif_urls = [
                        item["images"]["original"]["url"]
                        for item in data["data"]  # NOQA
                    ]
                    return gif_urls
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the Giphy API: {e}")
            return None
        except ValueError as e:
            print(f"Error decoding Giphy API JSON response: {e}")
            return None
