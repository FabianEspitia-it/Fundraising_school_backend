from src.utils.scraper import move_down


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