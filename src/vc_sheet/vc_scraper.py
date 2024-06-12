from src.models import  Fund

from src.vc_sheet.constants import *

from src.utils.scraper import get_html
from src.utils.scraper import move_down


def vc_scraper_funds():
    """
    Scrapes information about venture capital funds from a specified URL.

    Returns:
        dict: A dictionary containing the scraped data about venture capital funds, including:
            - "funds" (list[Fund]): A list of Fund objects containing details about each fund.
            - "final_fund_invest" (list[list[str]]): A list of investment information for each fund.
            - "fund_sectors" (list[list[str]]): A list of sectors each fund focuses on.
            - "fund_countries_invest" (list[list[str]]): A list of countries each fund invests in.
            - "check_size_range" (list[str]): A list of check size ranges for each fund.
            - "partner_names" (list[list[str]]): A list of partner names for each fund.
            - "partner_links" (list[list[str]]): A list of links to partner profiles for each fund.
    """

    print("Start scraping process")

    soup = move_down(FUNDS_URL, 10)
    print("Moved down the page")

    fund_link = soup.find_all("a", class_="full-click w-inline-block")
    print("Found fund links")

    fund_name = soup.find_all("h3", class_="list-heading list-pages")
    print("Found fund names")

    fund_description = soup.find_all("div", class_="shortdesccard w-richtext")
    print("Found fund descriptions")

    fund_photo = soup.find_all("div", class_="list-photo investor-cards _55")
    print("Found fund photos")

    fund_website = soup.find_all("a", class_="contact-icon site-link w-inline-block")
    print("Found fund websites")

    fund_twitter = soup.find_all("a", class_="contact-icon x w-inline-block")
    print("Found fund Twitter links")

    fund_linkedin = soup.find_all("a", class_="contact-icon linkedin w-inline-block")
    print("Found fund LinkedIn links")

    fund_crunch_base = soup.find_all("a", class_="contact-icon crunchbase w-inline-block")
    print("Found fund Crunchbase links")

    fund_invest = soup.find_all("div", class_="align-row no-sho-mo")
    print("Found fund investment information")

    final_fund_invest: list[list[str]] = []

    for parent_div in fund_invest:
        filtered_pill_items = [div for div in parent_div.find_all('div', class_='pill-item') if div.get('class') == ['pill-item']]
        final_fund_invest.append([item.get_text() for item in filtered_pill_items])
    print("Processed investment information")

    funds: list[Fund] = []
    fund_sectors = []
    fund_countries_invest = []
    check_size_range = []
    partner_names = []
    partner_links = []

    for n in range(0, len(fund_name)):
        print(f"Processing fund {n+1}/{len(fund_name)}")

        additional_info = fund_additional_data(f"https://www.vcsheet.com{fund_link[n].get('href')}")
        additional_info = fund_additional_data(f"https://www.vcsheet.com{fund_link[n].get('href')}")
        print("Retrieved additional fund data")

        fund = Fund(
            name=fund_name[n].text.strip() if n < len(fund_name) else None,
            description=fund_description[n].text.strip() if n < len(fund_description) else None,
            photo=str(fund_photo[n].get("style")).replace("background-image:url(", "").replace(")", "").replace('"', '') if n < len(fund_photo) else None,
            website=fund_website[n].get("href") if n < len(fund_website) else None,
            twitter=fund_twitter[n].get("href") if n < len(fund_twitter) else None,
            linkedin=fund_linkedin[n].get("href") if n < len(fund_linkedin) else None,
            crunch_base=fund_crunch_base[n].get("href") if n < len(fund_crunch_base) else None,
            contact=additional_info.get("contact"),
            location=additional_info.get("location")
        )
        print(f"Created Fund object for fund {n+1}")

        fund_sectors.append(additional_info.get("sector_focus"))
        fund_countries_invest.append(additional_info.get("countries_invest_in"))
        check_size_range.append(additional_info.get("check_size_range"))
        partner_names.append(additional_info.get("partner_names"))
        partner_links.append(additional_info.get("partner_links"))

        funds.append(fund)
        print(f"Appended fund {n+1} to the funds list")

    print("Finished processing all funds")
    return funds, final_fund_invest, fund_sectors, fund_countries_invest, check_size_range, partner_names, partner_links


def fund_additional_data(url: str) -> dict:
    """
    Scrapes additional information about a specific venture capital fund from a given URL.

    Args:
        url (str): The URL of the fund's page to scrape.

    Returns:
        dict: A dictionary containing additional information about the fund, including:
            - "contact" (str): Contact information for the fund.
            - "location" (str): The location of the fund.
            - "check_size_range" (list[str]): The check size range the fund invests in.
            - "lead_in" (list[str]): Information about lead investments.
            - "sector_focus" (list[str]): The sectors the fund focuses on.
            - "countries_invest_in" (list[str]): The countries the fund invests in.
            - "partner_names" (list[str]): Names of the partners in the fund.
            - "partner_links" (list[str]): Links to the profiles of the partners.
    """
    print(f"Scraping additional data for URL: {url}")
    soup = get_html(url)
    print(f"Retrieved HTML content for URL: {url}")

    all_sections = soup.find_all("div", class_="quick-view-row")
    fund_contact = soup.find("div", class_="quick-deal-response right")
    fund_location = soup.find_all("div", class_="quick-deal-response")
    final_fund_location = "".join([div.text.strip() for div in fund_location if "right" not in div.get("class", [])])
    check_size_range = []
    lead_in = []
    sector_focus = []
    countries_invest_in = []

    partner_names = []
    partner_links = soup.find_all("a", class_="mini-profile-overlay fund-p w-inline-block")

    partners_headings = soup.find_all("div", class_="list-heading")
    partners_titles = soup.find_all("div", class_="list-title")

    for heading, _ in zip(partners_headings, partners_titles):
        partner_names.append(heading.text.strip())
    print(f"Retrieved partner names and titles for URL: {url}")

    counter: int = 0

    for section in all_sections:
        pill_items = section.find_all("div", class_="pill-item")
        pill_list = [pill.get_text(strip=True) for pill in pill_items]

        if counter == 2:
            check_size_range = pill_list
        elif counter == 4:
            lead_in = pill_list
        elif counter == 5:
            sector_focus = pill_list
        elif counter == 6:
            countries_invest_in = pill_list

        counter += 1

    partner_names.pop(0)
    print(f"Processed additional data sections for URL: {url}")

    # Ensure the number of partner names and links match
    assert len(partner_names) == len(partner_links), f"Mismatch in partner names ({len(partner_names)}) and links ({len(partner_links)}) for URL: {url}"

    return {
        "contact": fund_contact.text.strip() if fund_contact else None,
        "location": final_fund_location,
        "check_size_range": check_size_range,
        "lead_in": lead_in,
        "sector_focus": sector_focus,
        "countries_invest_in": countries_invest_in,
        "partner_names": partner_names,
        "partner_links": [link.get("href") for link in partner_links],
    }


def vc_scraper_partners(url: str) -> dict:

    """
    Scrapes information about partners from a specific URL.

    Args:
        url (str): The URL of the partner's page to scrape.

    Returns:
        dict: A dictionary containing details about the partner, including:
            - "email" (str): The partner's email address.
            - "description" (str): A description or bio of the partner.
            - "crunch_base" (str): A link to the partner's Crunchbase profile.
            - "website" (str): A link to the partner's website.
            - "twitter" (str): A link to the partner's Twitter profile.
            - "linkedin" (str): A link to the partner's LinkedIn profile.
            - "photo" (str): A URL to the partner's photo.
            - "role" (str): The partner's role or title.
    """
    
    soup_partner = get_html(f"https://www.vcsheet.com{url}")

    partner_email: str = soup_partner.find("a", class_="list-card contact-card email w-inline-block")
    partner_description: str = soup_partner.find("div", class_="short-bio bg more-pad w-richtext")
    partner_crunch_base: str = soup_partner.find("a", class_="list-card contact-card crunchbase w-inline-block")
    partner_webiste: str = soup_partner.find("a", class_="button link-out-button in-line w-inline-block")
    parner_twitter: str = soup_partner.find("a", class_="list-card contact-card twitter dm w-inline-block")
    partner_linkedin: str = soup_partner.find("a", class_="list-card contact-card linkedin w-inline-block")
    partner_photo: str = soup_partner.find("a", class_="profile-photo la w-inline-block")
    partner_role: str = soup_partner.find("div", class_="bio-subtitle")


    return  {
            "email" : partner_email.get("href").replace("mailto:", "").replace("?subject=Pitch", "") if partner_email else None,
            "description" : partner_description.text.strip() if partner_description else None,
            "crunch_base" : partner_crunch_base.get("href") if partner_crunch_base else None,
            "website" : partner_webiste.get("href") if partner_webiste else None,
            "twitter" : parner_twitter.get("href") if parner_twitter else None,
            "linkedin" : partner_linkedin.get("href") if partner_linkedin else None,
            "photo" : str(partner_photo.get("style")).replace("background-image:url(", "").replace(")", "")
            .replace('"', '') if partner_photo else None,
            "role" : partner_role.text.strip() if partner_role else None
            }


"""
SCRAPERS THAT WE DONT NEED AT THE MOMENT

def vc_scraper_sheets():
    soup = get_html()

    vc_images = soup.find_all("div", class_="content-thumb")
    titles = soup.find_all("div", class_="content-label bold")
    descriptions = soup.find_all("div", class_="fund-desc-wrap")
    crunch_base_url = soup.find_all("a", class_="contact-icon crunchbase w-inline-block")
    linkedin_url = soup.find_all("a", class_="contact-icon linkedin w-inline-block")
    twitter_url = soup.find_all("a", class_="contact-icon w-inline-block")
    website_url = soup.find_all("a", class_="contact-icon site-link w-inline-block")

    return ""


def vc_scraper_all_sheets():
    soup = get_html(ALL_SHEETS_URL)

    funds_name = soup.find_all("div", class_="card-row-name")
    funds_description = soup.find_all("div", class_="small-description max-height")
    funds_image = soup.find_all("div", class_="card-row-thumb taller")
    funds_amount = soup.find_all("div", class_="pill-total")

def vc_scraper_investors() -> None:
    
    soup = move_down(INVESTORS_URL, 35)


    investor_name = soup.find_all("h3", class_="list-heading list-pages") 
    investor_photo = soup.find_all("div", class_="list-photo investor-cards _55")
    investor_role = soup.find_all("div", class_="html-embed w-embed")
    investor_description = soup.find_all("div", class_="shortdesccard more-top w-richtext")
    investor_email = soup.find_all("a", class_="contact-icon email w-inline-block") 
    investor_twitter = soup.find_all("a", class_="contact-icon x w-inline-block")
    investor_linkedin = soup.find_all("a", class_="contact-icon linkedin w-inline-block")
    investor_crunch_base = soup.find_all("a", class_="contact-icon crunchbase w-inline-block")
    investor_youtube = soup.find_all("a", class_="contact-icon video w-inline-block")
    investor_invest = soup.find_all("div", class_="align-row center-mobile")

    final_investor_vc = []

    
    for parent_div in investor_invest:
       
        filtered_pill_items = [div for div in parent_div.find_all('div', class_='pill-item') if div.get('class') == ['pill-item']]
        
        final_investor_vc.append([item.get_text() for item in filtered_pill_items])
    
    investors : list[Investor] = []

    for n in range(0, len(investor_name)):
        investor =Investor(
            name = investor_name[n].text.strip() if n < len(investor_name) else None,
            photo = str(investor_photo[n].get("style")).replace("background-image:url(", "")
            .replace(")", "")
            .replace('"', '') if n < len(investor_photo) else None,
            role = investor_role[n].text.strip(),
            description = investor_description[n].text.strip() if n < len(investor_description) else None,
            email = investor_email[n].get("href").replace("mailto:", "").replace("?subject=Pitch", "")
            if n < len(investor_email) else None,
            twitter = investor_twitter[n].get("href") if n < len(investor_twitter) else None,
            linkedin = investor_linkedin[n].get("href") if n < len(investor_linkedin) else None,
            crunch_base = investor_crunch_base[n].get("href") if n< len(investor_crunch_base) else None,
            youtube = investor_youtube[n].get("href") if n < len(investor_youtube) else None
        )

        investors.append(investor)

    return investors, final_investor_vc



def vc_scraper_reporters() -> list[Reporter]:
    soup = get_html(REPORTERS_URL)

    reporter_name = soup.find_all("h3", class_="list-heading list-pages larger")
    reporter_description = soup.find_all("div", class_="reporter-bio")
    reporter_photo = soup.find_all("a", class_="list-photo investor-cards _65 w-inline-block")
    reporter_website = soup.find_all("a", class_="contact-icon site-link w-inline-block")
    reporter_email = soup.find_all("a", class_="contact-icon site-link dark w-inline-block")
    reporter_twitter = soup.find_all("a", class_="contact-icon x w-inline-block")
    reporter_linkedin = soup.find_all("a", class_="contact-icon linkedin w-inline-block")
    reporter_channel = soup.find_all("a", class_="fund-face-pic sm reporter-version w-inline-block")
    reporter_location = [n.text.strip() for n in soup.find_all("div", class_="list-title medium")]

    reporter_final_location = []
    reporter_final_company = []
    for i in range(0, len(reporter_location), 2):
        if i + 1 < len(reporter_location):
            reporter_final_location.append(reporter_location[i + 1])
            reporter_final_company.append(reporter_location[i])

    reporters: list[Reporter] = []
    for n in range(0, len(reporter_name)):
        reporter = Reporter(
            name=reporter_name[n].text.strip() if n < len(reporter_name) else None,
            description=reporter_description[n].text.strip() if n < len(reporter_description) else None,
            photo=str(reporter_photo[n].get("style")).replace("background-image:url(", "")
            .replace(")", "")
            .replace('"', '')
            if n < len(reporter_photo) else None,
            website=str(reporter_website[n].get("href")) if n < len(reporter_website) else None,
            email=reporter_email[n].get("href").replace("mailto:", "").replace("?subject=Pitch", "")
            if n < len(reporter_email) else None,
            twitter=reporter_twitter[n].get("href") if n < len(reporter_twitter) else None,
            linkedin=reporter_linkedin[n].get("href") if n < len(reporter_linkedin) else None,
            channel_url=reporter_channel[n].get("href") if n < len(reporter_channel) else None,
            channel_image=reporter_channel[n].get("style").replace("background-image:url(", "")
            .replace(")", "")
            .replace('"', '')
            if n < len(reporter_channel) else None,
            location=reporter_final_location[n].strip() if n < len(reporter_final_location) else None,
            company=reporter_final_company[n].strip() if n < len(reporter_final_company) else None
        )

        reporters.append(reporter)

    return reporters
"""

    