from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from sqlalchemy import func

from .database import Base, engine, get_db
from .deps import verify_api_key
from . import models, schemas

app = FastAPI(
    title="IIQ Web Service App",
    dependencies=[Depends(verify_api_key)]
)

# ---- Create tables ----
Base.metadata.create_all(bind=engine)

# ---- Consistent error responses ----
@app.exception_handler(HTTPException)
def http_exception_handler(request, exc: HTTPException):
    # If we raised detail as {"error":..., "message":...}, return it as-is
    if isinstance(exc.detail, dict) and "error" in exc.detail and "message" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP_ERROR", "message": str(exc.detail)}
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "INVALID_REQUEST", "message": "Request validation failed"}
    )

def raise_error(code: str, message: str, http_status: int):
    raise HTTPException(status_code=http_status, detail={"error": code, "message": message})

# ---- Seed default groups on startup ----
DEFAULT_GROUPS = [
    ("SUPER ADMIN", "Super administrators"),
    ("ADMIN", "Administrators"),
    ("EDITOR", "Editors"),
    ("USER", "Standard users"),
]

@app.on_event("startup")
def seed_groups():
    db = next(get_db())
    try:
        for name, desc in DEFAULT_GROUPS:
            existing = db.query(models.Group).filter(models.Group.name == name).first()
            if not existing:
                db.add(models.Group(name=name, description=desc))
        db.commit()
    finally:
        db.close()

# ---- Health ----
@app.get("/api/health")
def health():
    return {"status": "ok"}

# ---- Groups (Entitlements) ----
@app.get("/api/groups", response_model=list[schemas.GroupOut])
def get_groups(db: Session = Depends(get_db)):
    groups = db.query(models.Group).order_by(models.Group.name.asc()).all()
    return groups

# ---- Users (Accounts) ----
@app.post("/api/users", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):

    # Unique username constraint
    existing = db.query(models.User).filter(models.User.username == payload.username).first()
    if existing:
        raise_error("USERNAME_EXISTS", "Username already exists", status.HTTP_409_CONFLICT)

    user = models.User(
        username=payload.username,
        email=payload.email,
        display_name=payload.display_name,
        is_active=True
    )

    # Optional group assignments at create time (expanded IIQ plan)
    if payload.groups:
        group_ids = [g.id for g in payload.groups]
        groups = db.query(models.Group).filter(models.Group.id.in_(group_ids)).all()

        if len(groups) != len(set(group_ids)):
            raise_error("GROUP_NOT_FOUND", "One or more group IDs not found", status.HTTP_404_NOT_FOUND)

        user.groups = groups

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/api/users", response_model=schemas.PagedUsers)
def list_users(
    page: int = Query(0, ge=0),
    size: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    total = db.query(func.count(models.User.id)).scalar() or 0

    users = (
        db.query(models.User)
        .order_by(models.User.username.asc())
        .offset(page * size)
        .limit(size)
        .all()
    )

    is_last_page = ((page + 1) * size) >= total

    return {
        "content": users,
        "page": page,
        "size": size,
        "totalElements": total,
        "isLastPage": is_last_page
    }

@app.get("/api/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise_error("USER_NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)
    return user

@app.patch("/api/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: str, payload: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise_error("USER_NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)

    user.is_active = payload.is_active
    db.commit()
    db.refresh(user)
    return user

# ---- Entitlement assignment ----
@app.post("/api/users/{user_id}/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def add_group_to_user(user_id: str, group_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise_error("USER_NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)

    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise_error("GROUP_NOT_FOUND", "Group not found", status.HTTP_404_NOT_FOUND)

    # Idempotent add
    if group not in user.groups:
        user.groups.append(group)
        db.commit()

    return None

@app.delete("/api/users/{user_id}/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_group_from_user(user_id: str, group_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise_error("USER_NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)

    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise_error("GROUP_NOT_FOUND", "Group not found", status.HTTP_404_NOT_FOUND)

    # Idempotent remove
    if group in user.groups:
        user.groups.remove(group)
        db.commit()

    return None

# ---- Delete account entirely ----
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise_error("USER_NOT_FOUND", "User not found", status.HTTP_404_NOT_FOUND)

    db.delete(user)
    db.commit()
    return None

