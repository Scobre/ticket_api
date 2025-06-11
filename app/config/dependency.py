from pydantic import BaseModel

from app.config.database import SessionLocal


class Dependency(BaseModel):
    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
