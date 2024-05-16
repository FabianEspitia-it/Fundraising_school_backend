from src.models import Reporter
from src.vc_sheet.constants import REPORTERS_URL, URL, FUNDS_URL, INVESTORS_URL
from src.utils.scraper import get_html


def vc_scraper_sheets() -> None:
    soup = get_html(URL)

    vc_images = soup.find_all("div", class_="content-thumb")
    titles = soup.find_all("div", class_="content-label bold")
    descriptions = soup.find_all("div", class_="fund-desc-wrap")
    crunch_base_url = soup.find_all("a", class_="contact-icon crunchbase w-inline-block")
    linkedin_url = soup.find_all("a", class_="contact-icon linkedin w-inline-block")
    twitter_url = soup.find_all("a", class_="contact-icon w-inline-block")
    website_url = soup.find_all("a", class_="contact-icon site-link w-inline-block")

    return vc_images, titles, descriptions, crunch_base_url, linkedin_url, twitter_url, website_url


def vc_scraper_investors() -> None:
    soup = get_html(INVESTORS_URL)

    investor_name = soup.find_all("h3", class_="list-heading list-pages")
    investor_photo = soup.find_all("div", class_="list-photo investor-cards _55")
    investor_role = soup.find_all("div", class_="html-embed w-embed")
    investor_description = soup.find_all("div", class_="shortdesccard more-top w-richtext")
    investor_email = soup.find_all("a", class_="contact-icon email w-inline-block")
    investor_twitter = soup.find_all("a", class_="contact-icon x w-inline-block")
    investor_linkedin = soup.find_all("a", class_="contact-icon linkedin w-inline-block")
    investor_crunch_base = soup.find_all("a", class_="contact-icon crunchbase w-inline-block")
    investor_youtube = soup.find_all("a", class_="contact-icon video w-inline-block")

    return investor_name, investor_photo, investor_role, investor_description, investor_email, investor_twitter, investor_linkedin, investor_crunch_base, investor_youtube


def vc_scraper_funds() -> None:
    soup = get_html(FUNDS_URL)

    fund_name = soup.find_all("h3", class_="list-heading list-pages")
    fund_description = soup.find_all("div", class_="shortdesccard w-richtext")
    fund_photo = soup.find_all("div", class_="list-photo investor-cards _55")
    fund_website = soup.find_all("a", class_="contact-icon site-link w-inline-block")
    fund_twitter = soup.find_all("a", class_="contact-icon x w-inline-block")
    fund_linkedin = soup.find_all("a", class_="contact-icon linkedin w-inline-block")
    fund_crunch_base = soup.find_all("a", class_="contact-icon crunchbase w-inline-block")
    fund_invest = soup.find_all("div", class_="align-row no-sho-mo")

    return fund_name, fund_description, fund_photo, fund_website, fund_twitter, fund_linkedin, fund_crunch_base, fund_invest


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