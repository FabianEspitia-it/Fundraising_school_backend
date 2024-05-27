import requests
import time

from src.utils.constants import SEARCH_URL
from urllib.request import urlopen
from bs4 import BeautifulSoup

from selenium import webdriver


def move_down(url:str, scroll_count: int) -> BeautifulSoup:

    """
    Scrolls down a webpage a specified number of times and returns the page source as a BeautifulSoup object.

    Args:
        url (str): The URL of the webpage to scroll.
        scroll_count (int): The number of times to scroll down the page.

    Returns:
        BeautifulSoup: A BeautifulSoup object containing the HTML of the scrolled page.
    """

    driver = webdriver.Chrome()  

    driver.get(url)

    scroll_number = scroll_count

    for _ in range(scroll_number):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  

    
    html = driver.page_source

    driver.quit()

    return BeautifulSoup(html, "html.parser")


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
