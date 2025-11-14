import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routers import blacklist
from app import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    pass


app = FastAPI(
    title="Blacklist API",
    description="API for managing a global email blacklist as per project requirements.",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health_check():
    """
    Performs a simple health check..
    """
    return {"status": "healthy"}


@app.get("/reset", tags=["Testing"])
def reset_database(db: Session = Depends(get_db)):
    try:
        # Delete all entries from the blacklist table
        deleted_count = db.query(models.BlacklistEntry).delete()
        db.commit()
        return {
            "status": "success",
            "message": f"Database cleared. {deleted_count} entries deleted.",
            "deleted_count": deleted_count
        }
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"status": "error",
                     "message": f"Failed to clear database: {str(e)}"}
        )


@app.get("/all", tags=["Testing"])
def get_all_blacklist_entries(db: Session = Depends(get_db)):
    try:
        entries = db.query(models.BlacklistEntry).all()
        return {
            "status": "success",
            "entries": [{"id": entry.id, "email": entry.email} for entry in entries]
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error",
                     "message": f"Failed to retrieve entries: {str(e)}"}
        )


@app.get("/error", tags=["Testing"])
def generate_error():
    result = 1 / 0
    return {"result": result}


@app.get("/env", tags=["Testing"])
def get_env_variables():
    return {"env": dict(os.environ)}


app.include_router(blacklist.router)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected internal server error occurred."},
    )
