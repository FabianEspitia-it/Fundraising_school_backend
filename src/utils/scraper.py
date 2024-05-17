import datetime

from src.utils.constants import SEARCH_URL
from urllib.request import urlopen
from bs4 import BeautifulSoup

import requests


def internet_search(search: str) -> requests.Response:
    """
    Performs an internet search using the specified search query.

    Args:
        search: A string representing the search query to be used for the internet search.

    Returns:
        A requests.Response object containing the response from the internet search.
    """
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/98.0.4758.82'
    }
    return requests.get(SEARCH_URL, headers=headers, params={'q': search})


def get_html(url: str) -> BeautifulSoup:
    """
    Retrieves the HTML content of a webpage located at the specified URL and parses it using BeautifulSoup.

    Args:
        url: A string representing the URL of the webpage to retrieve.

    Returns:
        A BeautifulSoup object containing the parsed HTML content of the webpage.
    """
    html = urlopen(url).read().decode("utf-8")

    return BeautifulSoup(html, "html.parser")


def get_time_period(values: dict) -> tuple[None | datetime.datetime, None | datetime.datetime]:
    start_date: None | datetime.datetime = None
    end_date: None | datetime.datetime = None

    if values.get("timePeriod"):
        if values["timePeriod"].get("startDate"):
            start_year = values["timePeriod"]["startDate"].get("year", 0)
            start_month = values["timePeriod"]["startDate"].get("month", 0)

            start_date = datetime.datetime(start_year, start_month, 1)

        if values["timePeriod"].get("endDate"):
            end_year = values["timePeriod"]["endDate"].get("year", 0)
            end_month = values["timePeriod"]["endDate"].get("month", 0)

            end_date = datetime.datetime(end_year, end_month, 1)

    return start_date, end_date
