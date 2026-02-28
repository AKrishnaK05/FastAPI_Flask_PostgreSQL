from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import auth, crud, schemas
from app.database import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=schemas.LoginResponse, status_code=status.HTTP_200_OK)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token."""

    user = crud.authenticate_user(db=db, email=credentials.email, password=credentials.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    access_token = auth.create_access_token(subject=str(user.id))
    return schemas.LoginResponse(access_token=access_token, token_type="bearer", user=user)
