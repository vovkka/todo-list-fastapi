from fastapi import APIRouter, status, HTTPException, Response, Depends

from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Users"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserAuth):
    # check if user already exist
    existing_user = await UsersDAO.get_one_or_none(login=user_data.login)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Login is already taken"
        )

    # insert user in db
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.insert_data(
        login=user_data.login,
        hashed_password=hashed_password
    )

    return {"status": status.HTTP_201_CREATED}


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user_or_none = await UsersDAO.get_one_or_none(login=user_data.login)
    user = authenticate_user(user_or_none, user_data.password)
    # check if user exist and password correct
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong login or password"
        )

    # create access token and add it to cookies
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.get("/check")
async def check_auth(user: Users = Depends(get_current_user)):
    return {"login": user.login}
