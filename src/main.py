import os
import uvicorn

from fastapi import FastAPI

from src.users.router import user
from src.vc_sheet.router import vc_sheet_router

from dotenv import load_dotenv


app = FastAPI()

app.title = "Fundraising School API"

app.include_router(user)
app.include_router(vc_sheet_router)

if __name__ == "__main__":
    load_dotenv()

    port = os.getenv("PORT")

    if not port:
        port = 8080

    uvicorn.run(app, host="0.0.0.0", port=int(port))
