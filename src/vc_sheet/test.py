from src.models import  Fund

from src.vc_sheet.constants import *

import time

from src.utils.scraper import get_html
from src.utils.scraper import move_down


def vc_scraper_funds():

    start_time = time.time()
    """
    Scrapes information about venture capital funds from a specified URL.

    Returns:
        dict: A dictionary containing the scraped data about venture capital funds.
    """
    soup = move_down(FUNDS_URL, 10)
    
    fund_elements = {
        'links': soup.find_all("a", class_="full-click w-inline-block"),
        'names': soup.find_all("h3", class_="list-heading list-pages"),
        'descriptions': soup.find_all("div", class_="shortdesccard w-richtext"),
        'photos': soup.find_all("div", class_="list-photo investor-cards _55"),
        'websites': soup.find_all("a", class_="contact-icon site-link w-inline-block"),
        'twitters': soup.find_all("a", class_="contact-icon x w-inline-block"),
        'linkedins': soup.find_all("a", class_="contact-icon linkedin w-inline-block"),
        'crunchbases': soup.find_all("a", class_="contact-icon crunchbase w-inline-block"),
        'invests': soup.find_all("div", class_="align-row no-sho-mo")
    }
    
    final_fund_invest = [
        [item.get_text() for item in div.find_all('div', class_='pill-item')]
        for div in fund_elements['invests']
    ]
    
    funds = []
    fund_sectors = []
    fund_countries_invest = []
    check_size_range = []
    partner_names = []
    partner_links = []

    for i in range(len(fund_elements['names'])):
        additional_info = fund_additional_data(f"https://www.vcsheet.com{fund_elements['links'][i].get('href')}")
        
        fund = Fund(
            name=fund_elements['names'][i].text.strip(),
            description=fund_elements['descriptions'][i].text.strip(),
            photo=fund_elements['photos'][i].get("style").replace("background-image:url(", "").replace(")", "").replace('"', ''),
            website=fund_elements['websites'][i].get("href"),
            twitter=fund_elements['twitters'][i].get("href"),
            linkedin=fund_elements['linkedins'][i].get("href"),
            crunch_base=fund_elements['crunchbases'][i].get("href"),
            contact=additional_info.get("contact"),
            location=additional_info.get("location")
        )
        
        funds.append(fund)
        fund_sectors.append(additional_info.get("sector_focus"))
        fund_countries_invest.append(additional_info.get("countries_invest_in"))
        check_size_range.append(additional_info.get("check_size_range"))
        partner_names.append(additional_info.get("partner_names"))
        partner_links.append(additional_info.get("partner_links"))

    print("--- %s seconds ---" % (time.time() - start_time))
    return {
        "funds": funds,
        "final_fund_invest": final_fund_invest,
        "fund_sectors": fund_sectors,
        "fund_countries_invest": fund_countries_invest,
        "check_size_range": check_size_range,
        "partner_names": partner_names,
        "partner_links": partner_links
    }

def fund_additional_data(url: str) -> dict:
    """
    Scrapes additional information about a specific venture capital fund from a given URL.

    Args:
        url (str): The URL of the fund's page to scrape.

    Returns:
        dict: A dictionary containing additional information about the fund.
    """
    soup = get_html(url)
    all_sections = soup.find_all("div", class_="quick-view-row")
    fund_contact = soup.find("div", class_="quick-deal-response right")
    fund_location = "".join([
        div.text.strip() for div in soup.find_all("div", class_="quick-deal-response") if "right" not in div.get("class", [])
    ])
    
    additional_info = {
        "check_size_range": [],
        "lead_in": [],
        "sector_focus": [],
        "countries_invest_in": []
    }
    
    for i, section in enumerate(all_sections):
        pill_items = [pill.get_text(strip=True) for pill in section.find_all("div", class_="pill-item")]
        if i == 2:
            additional_info["check_size_range"] = pill_items
        elif i == 4:
            additional_info["lead_in"] = pill_items
        elif i == 5:
            additional_info["sector_focus"] = pill_items
        elif i == 6:
            additional_info["countries_invest_in"] = pill_items
    
    partner_elements = soup.find_all("a", class_="mini-profile-overlay fund-p w-inline-block")
    partner_names = [
        heading.text.strip() for heading in soup.find_all("div", class_="list-heading")
    ][1:]  # Ignoring the first element as in the original code

    return {
        "contact": fund_contact.text.strip() if fund_contact else None,
        "location": fund_location,
        "check_size_range": additional_info["check_size_range"],
        "lead_in": additional_info["lead_in"],
        "sector_focus": additional_info["sector_focus"],
        "countries_invest_in": additional_info["countries_invest_in"],
        "partner_names": partner_names,
        "partner_links": [link.get("href") for link in partner_elements]
    }

print(vc_scraper_funds())