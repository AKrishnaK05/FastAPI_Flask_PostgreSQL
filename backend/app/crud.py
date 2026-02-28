from sqlalchemy.orm import Session

from app import auth, models, schemas


def get_user(db: Session, user_id: int) -> models.User | None:
    """Fetch one user by id."""

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    """Fetch one user by email."""

    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user_data: schemas.UserCreate) -> models.User:
    """Create and persist a new user."""

    db_user = models.User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=auth.hash_password(user_data.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    """Validate login credentials."""

    user = get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user
