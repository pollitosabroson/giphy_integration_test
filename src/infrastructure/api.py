from fastapi import FastAPI, Query, HTTPException, Depends
from core.giphy_port import GiphyPort
from core.models import GiphyResponse, MultipleGiphyResponse
from infrastructure.giphy_adapter import GiphyAPIAdapter

app = FastAPI()


def get_giphy_service() -> GiphyPort:
    """
    Dependency injection function to provide an instance of the GiphyPort interface.

    Returns:
        GiphyPort: An instance of a class that implements the GiphyPort interface
                   (currently GiphyAPIAdapter).
    """  # NOQA
    return GiphyAPIAdapter()


@app.get("/get_giphy_gif", response_model=GiphyResponse)
async def get_giphy_gif_endpoint(
    text: str = Query(..., description="The search text for the GIF"),
    giphy_service: GiphyPort = Depends(get_giphy_service),
):
    """
    Endpoint to retrieve the URL of a single GIF from Giphy based on the 'text' query parameter.

    Args:
        text (str): The text to search for the GIF. This is a required query parameter.
        giphy_service (GiphyPort): An instance of the GiphyPort interface, injected as a dependency.

    Returns:
        GiphyResponse: A Pydantic model containing the URL of the found GIF.

    Raises:
        HTTPException (status_code=404): If no GIF is found for the provided text.
    """  # NOQA
    gif_url = giphy_service.get_gif_by_text(text, limit=1)
    if gif_url and isinstance(gif_url, str):
        return {"gif_url": gif_url}
    else:
        raise HTTPException(
            status_code=404, detail=f"No GIF was found for the text: '{text}'"
        )


@app.get("/get_giphy_gifs", response_model=MultipleGiphyResponse)
async def get_giphy_gifs_endpoint(
    text: str = Query(..., description="The search text for the GIFs"),
    limit: int = Query(3, description="Maximum number of GIFs to return"),
    rating: str = Query(
        "g", description="Content rating filter (g, pg, pg-13, r)"
    ),  # NOQA
    lang: str = Query("en", description="Language of the results"),
    giphy_service: GiphyPort = Depends(get_giphy_service),
):
    """
    Endpoint to retrieve multiple GIF URLs from Giphy based on the 'text' query parameter.

    Args:
        text (str): The text to search for the GIFs. This is a required query parameter.
        limit (int, optional): The maximum number of GIFs to retrieve. Defaults to 3.
        rating (str, optional): The content rating filter for the GIFs. Defaults to 'g'.
        lang (str, optional): The language code for the search results. Defaults to 'en'.
        giphy_service (GiphyPort): An instance of the GiphyPort interface, injected as a dependency.

    Returns:
        MultipleGiphyResponse: A Pydantic model containing a list of GIF URLs.

    Raises:
        HTTPException (status_code=404): If no GIFs are found for the provided text.
    """  # NOQA
    gif_urls = giphy_service.get_gif_by_text(
        text, limit=limit, rating=rating, lang=lang
    )
    if gif_urls and isinstance(gif_urls, list):
        return {"gif_urls": gif_urls}
    else:
        raise HTTPException(
            status_code=404, detail=f"No GIFs were found for the text: '{text}'"  # NOQA
        )
