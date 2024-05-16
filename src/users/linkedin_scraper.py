import os

from bs4 import BeautifulSoup
from linkedin_api import Linkedin
from src.utils.scraper import internet_search
from src.models import User


linkedin_connect = Linkedin(os.getenv("LINKEDIN_USER"), os.getenv("LINKEDIN_PASSWORD"))


def search_linkedin_url(name: str) -> str | None:
    """
    Searches for a LinkedIn profile URL based on the provided name.

    Args:
        name: A string representing the name of the person to search for on LinkedIn.

    Returns:
        If a LinkedIn profile URL is found in the search results, returns the URL.
        If no LinkedIn profile URL is found, returns None.
    """
    content: str = internet_search(f"site:linkedin.com {name}").text
    soup = BeautifulSoup(content, 'html.parser')

    search_results = soup.select('.tF2Cxc')
    if search_results:
        return search_results[0].find('a')['href']

    return None


def linkedin_public_identifier(url) -> str | None:
    """
    Converts a LinkedIn profile URL to public identifier.

    Args:
        url: A string representing the LinkedIn profile URL.

    Returns:
        If the URL contains '/in/' or '/school/', returns the public identifier.
        If '/in/' or '/school/' is not found in the URL, returns None.
    """
    path_index = url.find("/in/")
    if path_index != -1:
        return url[path_index:].split("/")[2]

    path_index = url.find("/school/")
    if path_index != -1:
        return url[path_index:].split("/")[2]

    return None


def get_linkedin_profile(public_identifier: str) -> User:

    profile_data = linkedin_connect.get_profile(public_identifier)

    return User()


def linkedin_data(full_name: str):
    linkedin_url = search_linkedin_url(full_name)
    if not linkedin_url:
        return None

    user_public_identifier = linkedin_public_identifier(linkedin_url)
    if not user_public_identifier:
        return None

    profile_data = get_linkedin_profile(user_public_identifier)

    return profile_data
