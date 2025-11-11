from fastapi import APIRouter
from  sqlalchemy.orm import Session
from app.database.db import SessionLocal
from typing import List, Optional
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuth
from app.config import soc_auth


social_router = APIRouter(prefix="/social", tags=["Social Auth"])

oauth = OAuth()

oauth.register(
    name="github",
    client_id=soc_auth.GITHUB_CLIENT_ID,
    secret_key=soc_auth.GITHUB_KEY,
    authorize_url="https://github.com/login/oauth/authorize",
)

oauth.register(
    name="google",
    client_id=soc_auth.GOOGLE_CLIENT_ID,
    secret_key=soc_auth.GOOGLE_KEY,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid profile email"},
)

@social_router.get("/login/github/")
async def login_github(request: Request):
    redirect_uri = soc_auth.GITHUB_URL
    return await oauth.github.authorize_redirect(request, redirect_uri)

@social_router.get("/login/google/")
async def login_google(request: Request):
    redirect_uri = soc_auth.GOOGLE_URL
    return await oauth.google.authorize_redirect(request, redirect_uri)
