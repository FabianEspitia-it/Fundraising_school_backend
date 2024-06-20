from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse

import pandas as pd
import os

from src.database import get_db
from src.users.linkedin_scraper import user_scraper

from src.users.schemas import ContactUserReq, ImageUserReq, NewUserReq, RoundUserReq
from src.users.crud import *

from src.utils.validations import check_email

user = APIRouter()


@user.get("/user/{email}", tags=["users"])
def get_user(email: str, db: Session = Depends(get_db)) -> JSONResponse:
    """
    Retrieve a user record by email.

    Args:
        email (str): The email address of the user to retrieve.
        db (Session): The database session dependency.

    Returns:
        JSONResponse: The user record if found.

    Raises:
        HTTPException: If the email is invalid (status code 400).
        HTTPException: If the user is not found (status code 404).
    """
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    user_record = get_user_by_email(db, email=email)
    if not user_record:
        raise HTTPException(status_code=404, detail="Not Found")

    return user_record


@user.get("/user/education/{email}", tags=["users"])
def get_user_education(email: str, db: Session = Depends(get_db)):
    """
    Retrieves education information for a user with the specified email from the database.

    Args:
        email (str): The email address of the user whose education information is to be retrieved.
        db (Session): The database session to use for interacting with the database.

    Returns:
        UserEducation: The education information associated with the user with the specified email.

    Raises: HTTPException: If the email is invalid or if no education information is found for the user, appropriate
    HTTP status codes are raised.
    """
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    user_education = get_education_by_user_email(db, email=email)
    if not user_education:
        raise HTTPException(status_code=404, detail="Not Found")

    return user_education


@user.get("/user/experience/{email}", tags=["users"])
def get_user_experience(email: str, db: Session = Depends(get_db)):
    """
    Retrieves experience information for a user with the specified email from the database.

    Args:
        email (str): The email address of the user whose experience information is to be retrieved.
        db (Session): The database session to use for interacting with the database.

    Returns:
        UserExperience: The experience information associated with the user with the specified email.

    Raises: HTTPException: If the email is invalid or if no experience information is found for the user, appropriate
    HTTP status codes are raised.
    """
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    user_experience = get_experience_by_user_email(db, email=email)
    if not user_experience:
        raise HTTPException(status_code=404, detail="Not Found")

    return user_experience


@user.post("/user/contact", tags=["users"])
def update_contact_user_info(contact_user: ContactUserReq, db: Session = Depends(get_db)):
    """
    Update contact info of an user.

    Args:
        contact_user (ContactUserReq): The user contact info request containing user details.
        db (Session): The database session dependency.

    Returns:
        JSONResponse: A JSON response indicating that the user was updated.

    Raises:
        HTTPException: If the email is invalid (status code 400).
        HTTPException: If the contact email is invalid (status code 400).
    """
    if not check_email(contact_user.contact_email):
        raise HTTPException(status_code=400, detail="Invalid Contact Email")

    if not check_email(contact_user.email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    amount_rows = update_contact_info_user_by_email(db, contact_user.email, contact_user.contact_email, contact_user.nickname)

    if amount_rows == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return JSONResponse(content={"response": "updated"}, status_code=status.HTTP_200_OK)


@user.post("/user/image", tags=["users"])
def update_contact_user_info(image_user: ImageUserReq, db: Session = Depends(get_db)):
    """
    Update image url of an user.

    Args:
        image_user (ImageUserReq): The user info request containing user details.
        db (Session): The database session dependency.

    Returns:
        JSONResponse: A JSON response indicating that the user was updated.

    Raises:
        HTTPException: If the email is invalid (status code 400).
    """
    if not check_email(image_user.email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    amount_rows = update_image_url_by_email(db, image_user.email, image_user.image)

    if amount_rows == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return JSONResponse(content={"response": "updated"}, status_code=status.HTTP_200_OK)


@user.post("/user/round", tags=["users"])
def update_round_user_info(round_user: RoundUserReq, db: Session = Depends(get_db)):
    """
    Update round info of an user.

    Args:
        round_user (NewUserReq): The user round info request containing user details.
        db (Session): The database session dependency.

    Returns:
        JSONResponse: A JSON response indicating that the user was updated.

    Raises:
        HTTPException: If the email is invalid (status code 400).
        HTTPException: If the email is not found (status code 404).
    """
    if not check_email(round_user.email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    amount_rows = update_round_info_user_by_email(db, round_user.email, round_user.seeking_capital, round_user.accept_terms_and_condition, round_user.round_name)

    if amount_rows == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return JSONResponse(content={"response": "updated"}, status_code=status.HTTP_200_OK)


@user.post("/user/new", tags=["users"])
def user_new(new_user: NewUserReq, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        new_user (NewUserReq): The new user request containing user details.
        background_tasks (BackgroundTasks): Background tasks manager for handling asynchronous tasks.
        db (Session): The database session dependency.

    Returns:
        JSONResponse: A JSON response indicating that the user was created.

    Raises:
        HTTPException: If the email is invalid (status code 400).
        HTTPException: If the email is already registered (status code 400).
    """
    if not check_email(new_user.email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    if get_user_by_email(db=db, email=new_user.email):
        raise HTTPException(status_code=400, detail="Email registered")
    

    background_tasks.add_task(user_scraper, db=db, req=new_user)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@user.post("/user/favorite_fund" , tags=["users"])
def add_favorite_fund(email: str, fund_id: int, db: Session = Depends(get_db)):
    """
    Add a favorite fund to a user's profile.

    Args:
        email (str): The email address of the user.
        fund_id (int): The unique identifier of the fund to add to the user's profile.
        db (Session): The database session dependency.

    Returns:
        JSONResponse: A JSON response indicating that the favorite fund was added.

    """

    add_favorite_fund_to_user(db, email, fund_id)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)


@user.get("/user/favorite_fund/csv/{email}", tags=["users"])
def get_favorite_fund_csv(email: str, db: Session = Depends(get_db)):
    """
    Retrieve a CSV file containing the favorite funds of a user.

    Args:
        email (str): The email address of the user.
        db (Session): The database session dependency.

    Returns:
        FileResponse: A CSV file containing the favorite funds of the user.

    Raises:
        HTTPException: If the email is invalid (status code 400).
        HTTPException: If the user is not found (status code 404).
        HTTPException: If no favorite funds are found for the user (status code 404).
    """
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    user_record = get_user_by_email(db, email=email)
    if not user_record:
        raise HTTPException(status_code=404, detail="User not found")
    
    favorite_funds = get_favorite_funds_by_user_id(db, email=email)
    
    if not favorite_funds:
        raise HTTPException(status_code=404, detail="No favorite funds found for this user.")
    
    df = pd.DataFrame([fund.__dict__ for fund in favorite_funds])
    df = df.drop(columns=['_sa_instance_state'])  
    
    
    download_folder = os.path.join(os.path.expanduser("~"), "Descargas")
    os.makedirs(download_folder, exist_ok=True)
    file_path = os.path.join(download_folder, "favorite_funds.csv")
    
    df.to_csv(file_path, index=False)
    
    return FileResponse(path=file_path, filename="favorite_funds.csv", media_type="text/csv")


@user.delete("/user/favorite_fund/{email}/{fund_id}", tags=["users"])
def delete_favorite_fund(email: str, fund_id: int, db: Session = Depends(get_db)):
    """
    Delete a favorite fund from a user's profile.

    Args:
        email (str): The email address of the user.
        fund_id (int): The unique identifier of the fund to delete from the user's profile.
        db (Session): The database session dependency.

    Returns:
        JSONResponse: A JSON response indicating that the favorite fund was deleted.

    Raises:
        HTTPException: If the email is invalid (status code 400).
    """
    if not check_email(email):
        raise HTTPException(status_code=400, detail="Invalid Email")

    delete_favorite_fund_by_user_id(db, email, fund_id)

    return JSONResponse(content={"response": "deleted"}, status_code=status.HTTP_200_OK)
