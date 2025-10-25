import os
from fastapi import APIRouter, Depends, HTTPException, Request, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models, schemas
from app.database import get_db

STATIC_AUTH_TOKEN = os.environ.get(
    'AUTH_TOKEN', 'my-super-secret-static-token')
security_scheme = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Security(security_scheme)):
    """
    Dependency to verify the static Bearer token.
    """
    if credentials.scheme != "Bearer" or credentials.credentials != STATIC_AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing authorization token",
        )
    return credentials.credentials


router = APIRouter(
    prefix="/blacklists",
    tags=["Blacklist Management"],
    dependencies=[Depends(verify_token)]
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.BlacklistAddResponse,
    summary="Add an Email to the Blacklist"
)
def add_to_blacklist(
    blacklist_item: schemas.BlacklistCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Adds a new email to the global blacklist.

    - **email**: The email address to add.
    - **app_uuid**: The client application's unique ID.
    - **blocked_reason**: (Optional) Why the email is being blocked.
    """
    # Get the source IP address from the request
    source_ip = request.client.host

    new_entry = models.BlacklistEntry(
        email=blacklist_item.email,
        app_uuid=str(blacklist_item.app_uuid),
        blocked_reason=blacklist_item.blocked_reason,
        ip_address=source_ip
    )

    try:
        db.add(new_entry)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{blacklist_item.email}' already exists in the blacklist."
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while adding the email."
        )

    return {"message": f"Email '{blacklist_item.email}' was added to the blacklist successfully"}


@router.get(
    "/{email}",
    response_model=schemas.BlacklistCheckResponse,
    summary="Check if an Email is Blacklisted"
)
def check_blacklist(email: str, db: Session = Depends(get_db)):
    """
    Checks if a specific email address exists in the global blacklist.
    """
    entry = db.query(models.BlacklistEntry).filter(
        models.BlacklistEntry.email == email).first()

    if entry:
        return {
            "is_blacklisted": True,
            "reason": entry.blocked_reason,
            "app_uuid": entry.app_uuid,
            "date_added": entry.created_at
        }
    else:
        return {"is_blacklisted": False}
