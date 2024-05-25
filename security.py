'''
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from fastapi import HTTPException, status, Depends, Response

from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request, APIRouter
from fastapi.security.utils import get_authorization_scheme_param
from typing import Dict

from models import User
from config import settings


class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    Custom OAuth2 bearer flow for retrieving an access token from a cookie.

    Parameters:
    - tokenUrl (str): The URL where the token can be obtained.
    - scheme_name (str, optional): The name of the authentication scheme.
    - scopes (dict, optional): OAuth2 scopes for authorization.
    - auto_error (bool, optional): If True, raise an HTTPException on authentication error.

    """

    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        """
        Initialize an OAuth2PasswordBearerWithCookie instance.

        Parameters:
        - tokenUrl (str): The URL where the token can be obtained.
        - scheme_name (str, optional): The name of the authentication scheme.
        - scopes (dict, optional): OAuth2 scopes for authorization.
        - auto_error (bool, optional): If True, raise an HTTPException on authentication error.

        """
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        """
        Call method to obtain the access token from a cookie.

        Parameters:
        - request (Request): The incoming HTTP request.

        Returns:
        - str or None: The access token or None if not authenticated.

        """
        authorization: str = request.cookies.get(
            "access_token"
        )  # changed to accept access token from httpOnly Cookie
        print("access_token is", authorization)

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user based on the provided token.

    Parameters:
    - token (str): The access token.

    Returns:
    - dict: The user information.

    """
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
    except Exception:
        raise credential_exception

    user = get_documents_from_id("users", {"username": username}, "one")
    if user is None:
        raise credential_exception
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token with optional expiration.

    Parameters:
    - data (dict): Data to be included in the token payload.
    - expires_delta (timedelta, optional): Expiration time for the token.

    Returns:
    - str: The encoded JWT access token.

    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


router = APIRouter()


@router.post("/login")
async def login(user: User, response: Response):
    """
    Log in a user and generate an access token.

    Parameters:
    - user (User): User credentials.
    - response (Response): HTTP response.

    Returns:
    - dict: Authentication status.
    """
    username = user.username
    password = user.password
    user_from_db = get_documents_from_id("users", {"username": username}, "one")
    if not user_from_db or user_from_db["password"] != password:
        raise HTTPException(status_code=404, detail="Authentication Failed")

    # Authenticate user and generate access token
    access_token = create_access_token(data={"sub": username})

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="None",
        secure=True,  # Required for cross-origin cookies
        expires=1800,
        path="/",  # Set the path to "/"
    )

    return {"detail": "authenticated"}
'''