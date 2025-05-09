from typing import Optional, List


class GiphyPort:
    """
    Abstract interface defining the contract for interacting with the Giphy service to retrieve GIFs.

    This class declares the `get_gif_by_text` method, which concrete implementations
    (adapters) must provide to make the call to the Giphy API.

    Raises:
        NotImplementedError: Raised if a class inheriting from `GiphyPort` does not implement
                             the `get_gif_by_text` method.
    """  # NOQA

    def get_gif_by_text(
        self, text: str, limit: int = 1, rating: str = "g", lang: str = "en"
    ) -> Optional[str | List[str]]:
        """
        Retrieves the URL(s) of GIF(s) from the Giphy service based on a search text.

        Args:
            text (str): The search text to find the GIF. This is the term that will be sent
                        to the Giphy API to search for relevant GIFs.
            limit (int, optional): The maximum number of GIFs to return. Defaults to 1.
                                   If more than one GIF is requested, the return value will be a list of URLs.
            rating (str, optional): The content rating filter for the GIFs. Defaults to 'g' (general audience).
                                    Other common options include 'pg', 'pg-13', and 'r'. Refer to the Giphy
                                    API documentation for the complete list of supported values.
            lang (str, optional): The language code for the search results. Defaults to 'en' (English).
                                 Refer to the Giphy API documentation for the complete list of supported
                                 language codes.

        Returns:
            Optional[str | List[str]]:
                - If `limit` is 1, returns a string (`str`) representing the URL of the found GIF,
                  or `None` if no GIF is found or if an error occurs.
                - If `limit` is greater than 1, returns a list (`List[str]`) of URLs of the found GIFs,
                  or `None` if no GIFs are found or if an error occurs.
        """  # NOQA
        raise NotImplementedError
