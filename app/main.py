import os
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.database import engine, Base
from app.routers import blacklist
from app import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blacklist API",
    description="API for managing a global email blacklist as per project requirements.",
    version="1.0.0"
)

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Health Check"])
def health_check():
    """
    Performs a simple health check.
    """
    return {"status": "healthy"}


@app.get("/reset", tags=["Testing"])
def reset_database():
    from sqlalchemy.orm import Session
    from app.database import SessionLocal

    db: Session = SessionLocal()
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
            content={"status": "error", "message": f"Failed to clear database: {str(e)}"}
        )
    finally:
        db.close()


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
