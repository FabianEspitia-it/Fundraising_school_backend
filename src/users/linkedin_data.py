import requests
from bs4 import BeautifulSoup

from src.users.constants import SEARCH_URL


def search_linkedin_url(name: str) -> str | None:
    search = f"site:linkedin.com {name}"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82'
    }
    content = requests.get(SEARCH_URL, headers=headers, params={'q': search}).text
    soup = BeautifulSoup(content, 'html.parser')
    search_results = soup.select('.tF2Cxc')
    if search_results:
        first_link = search_results[0].find('a')['href']
        return first_link
    else:
        return None


def convert_linkedin_url(url) -> str | None:
    linkedin_path = "/in/"
    path_index = url.find(linkedin_path)
    if path_index != -1:
        base_domain = "https://www.linkedin.com"
        new_url = base_domain + url[path_index:]
        return new_url
    else:
        return None


def get_linkedin_profile(url: str) -> dict:


    return {}


def linkedin_data(full_name: str):
    linkedin_url = search_linkedin_url(full_name)
    if not linkedin_url:
        return None

    user_linkedin_url = convert_linkedin_url(linkedin_url)
    if not user_linkedin_url:
        return None

    profile_data = get_linkedin_profile(user_linkedin_url)
    profile_data["linkedin_url"] = user_linkedin_url

    return profile_data
