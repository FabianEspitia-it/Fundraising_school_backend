from fastapi import APIRouter, status, Depends, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse

from src.database import get_db
from src.users.linkedin_scraper import user_scraper

from src.users.schemas import NewUserReq
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
<<<<<<< HEAD
    
=======
>>>>>>> e9755fee1d32a39fdada08c77f5afe7a5f10c5e7

    background_tasks.add_task(user_scraper, db=db, req=new_user)

    return JSONResponse(content={"response": "created"}, status_code=status.HTTP_201_CREATED)

