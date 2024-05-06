from fastapi import FastAPI
from.users.router import user


app = FastAPI()

app.title = "Fundraising School API"

app.include_router(user)



