from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from src.utils.scraper import internet_search, get_time_period, authenticate_linkedin
from src.models import User, Education, Experience

from src.users.schemas import NewUserReq
from src.users.crud import create_bulk_education, create_bulk_experience, create_user_principal_data


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


def scraper_linkedin_profile(db: Session, public_identifier: str, user_id: int) -> None:
    """
    Scrapes LinkedIn profile data and saves it to the database for the given user.

    Args:
        db (Session): The database session to use for interacting with the database.
        public_identifier (str): The public identifier of the LinkedIn profile to scrape.
        user (User): The user object to which the scraped LinkedIn profile data will be associated.
    """
    linkedin_connect = authenticate_linkedin()
    if not linkedin_connect:
        print("[ERROR] Not possible scraper linkedin data: ", user_id)
        return 


    profile_data: dict = linkedin_connect.get_profile(public_identifier)

    followers_amount: int = len(linkedin_connect.get_profile_connections(public_identifier))

    user = db.query(User).filter(User.id == user_id).first()

    user.last_name = profile_data.get("lastName")
    user.location = profile_data.get("locationName")
    user.headline = profile_data.get("headline")
    user.industry = profile_data.get("industryName")
    user.summary = profile_data.get("summary")
    user.followers_amount = followers_amount

    db.commit()
    db.refresh(user)


    education: list[Education] = []
    for education_item in profile_data.get("education"):
        linkedin_url = search_linkedin_url(education_item.get("schoolName"))

        start_date, end_date = get_time_period(education_item)

        education_to_save = Education(
            school_name=education_item.get("schoolName"),
            degree_name=education_item.get("degreeName"),
            grade=education_item.get("grade"),
            description=education_item.get("description"),
            linkedin_url=linkedin_url,
            start_date=start_date,
            end_date=end_date,
            user_id=user_id,
        )

        education.append(education_to_save)

    create_bulk_education(db, education)

    experiences: list[Experience] = []
    for experience in profile_data["experience"]:
        linkedin_url = search_linkedin_url(experience.get("companyName"))

        start_date, end_date = get_time_period(experience)

        experiences.append(
            Experience(
                linkedin_url=linkedin_url,
                role=experience.get("title"),
                company=experience.get("companyName"),
                location=experience.get("locationName"),
                description=experience.get("description"),
                start_date=start_date,
                end_date=end_date,
                user_id=user_id
            )
        )

    create_bulk_experience(db, experiences)


def user_scraper(db: Session, req: NewUserReq) -> None:
    """
    Scrapes LinkedIn profile data for a new user and saves it to the database.

    Args:
        db (Session): The database session to use for interacting with the database.
        req (NewUserReq): The request object containing information about the new user.
    """
    user: User = User(
        email=req.email,
        first_name=req.name
    )

    if req.linkedin_picture is None:
        user.photo_url = req.linkedin_picture

    linkedin_url = search_linkedin_url(req.name)
    if not linkedin_url:
        print("Aqwui")
        create_user_principal_data(db, user)
        return None

    user.linkedin_url = linkedin_url

    user_public_identifier = linkedin_public_identifier(linkedin_url)
    if not user_public_identifier:
        print("Aqwui")
        create_user_principal_data(db, user)
        return None
    
    user_id = create_user_principal_data(db, req)

    scraper_linkedin_profile(db, user_public_identifier, user_id)
