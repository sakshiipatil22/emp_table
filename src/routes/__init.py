from src.db.model import get_session
from src.db.model import engine  

def get_db():
    db=get_session()
    try:
        yield db
    finally:
        db.close()