from src.utils.scraper import get_html, move_down

"""
soup = move_down("https://signal.nfx.com/investors/andres-humberto-bilbao", 1)


web_sites = soup.find_all("a", class_="iconlink")            
web_sites_final = [web_site.get("href") for web_site in web_sites]
sector_and_stage = soup.find_all("a", class_="vc-list-chip")

print( {
                "name": soup.find("h1", class_="f3 f1-ns mv1").text,
                "location": soup.find("span", class_="ml1").text,
                "role": soup.find("div", class_="subheader lower-subheader pb2").text,
                "vc_link": soup.find("a", class_="ml1 subheader lower-subheader").get("href") if soup.find("a", class_="ml1 subheader lower-subheader") else None,
                "photo": soup.find("img", style="object-fit: cover; height: auto; width: auto;")["src"],
                "investor_linkedin": next((url for url in web_sites_final if 'https://www.linkedin.com/' in url), None),
                "invest_range_final": [span.get_text() for div in soup.find_all("div", class_="col-xs-7") for span in div.find_all("span", class_="lh-solid")][1],
                "sector_and_stage": [item.text for item in sector_and_stage]
            })

"""

def fund_additional_data(url:str) -> dict:

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


    soup = get_html(url)

    all_sections = soup.find_all("div", class_="quick-view-row")
    fund_contact = soup.find("div", class_="quick-deal-response right")
    fund_location = soup.find_all("div", class_="quick-deal-response")
    final_fund_location = "".join([div.text.strip() for div in fund_location if "right" not in div.get("class", [])])
    check_size_range = []
    lead_in = []
    sector_focus= []
    countries_invest_in = []


    partner_names = []
    partner_links = soup.find_all("a", class_="mini-profile-overlay fund-p w-inline-block")




    partners_headings = soup.find_all("div", class_="list-heading")
    partners_titles = soup.find_all("div", class_="list-title")


    for heading, _ in zip(partners_headings, partners_titles):
            partner_names.append(heading.text.strip())

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


print(fund_additional_data("https://www.vcsheet.com/fund/supply-change-capital"))