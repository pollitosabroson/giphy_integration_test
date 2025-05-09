from pydantic import BaseModel
from typing import Optional, List


class GiphyResponse(BaseModel):
    """
    Pydantic model to represent the response when a single GIF is requested from Giphy.

    Attributes:
        gif_url (Optional[str]): The URL of the found GIF. If no GIF is found
                                 or if an error occurs, this value will be `None`.
    """  # NOQA

    gif_url: Optional[str] = None


class MultipleGiphyResponse(BaseModel):
    """
    Pydantic model to represent the response when multiple GIFs are requested from Giphy.

    Attributes:
        gif_urls (Optional[List[str]]): A list of URLs of the found GIFs. If no GIFs are
                                       found or if an error occurs, this list will be `None`.
    """  # NOQA

    gif_urls: Optional[List[str]] = None
