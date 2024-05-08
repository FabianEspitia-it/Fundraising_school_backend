import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import src.models as models




SEARCH_URL = "https://www.google.com/search"


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options)

    return driver

driver = create_driver()


def search_linkedin_url(name: str) -> str | list[str]:
    search = f"site:linkedin.com {name} "
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82'
    }

    content = requests.get(SEARCH_URL, headers=headers, params={'q': search}).text

    soup = BeautifulSoup(content, 'html.parser')

    search = soup.find(id='search')
    first_link = search.find('a')

    return first_link['href']


def convert_linkedin_url(url) -> None | str:
    # Define the expected LinkedIn path after the domain
    linkedin_path = "/in/"

    # Find the index where the LinkedIn path starts
    path_index = url.find(linkedin_path)

    # If the path is found, create the new URL with the correct domain
    if path_index != -1:
        base_domain = "https://www.linkedin.com"
        new_url = base_domain + url[path_index:]
        return new_url
    else:
        return None


def get_linkedin_profile(url: str) -> dict:
    global driver
    driver.get(url)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    general_info = soup.select('.not-first-middot span')

    location: str = general_info[0].text
    followers_amount: str = "".join([char for char in general_info[2].text.strip() if char.isdigit()])

    education_items = soup.select(".education__list-item")

    return [location, followers_amount, education_items]

def linkedin_data(full_name : str):

    linkedin_url = search_linkedin_url(full_name)

    if linkedin_url is list[str]:
        linkedin_url = linkedin_url[0]

    user_linkedin_url = convert_linkedin_url(linkedin_url)

    if linkedin_url is None:
        return None

    profile_data = get_linkedin_profile(linkedin_url)

    db_user = models.User(location=profile_data[0], 
                          followers_amount= profile_data[1], 
                          photo_url = photo_url, 
                          linkedin_url = user_linkedin_url)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    

    
