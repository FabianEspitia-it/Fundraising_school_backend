from fastapi import FastAPI
from.users.router import user


app = FastAPI()

app.include_router(user)



