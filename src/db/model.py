import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from os import getcwd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger

engine = None
Base = declarative_base()
DBSession: sessionmaker = None


def init_db():
    try:
        global DBSession
        engine = create_engine(f"sqlite:///{getcwd()}/config/employee.db")
        conn = engine.connect()
        conn.close()
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        return True
    except Exception as e:
        logger.error(f"Error Occurred in init_db - {e}")
        return False


def get_session():
    if DBSession is not None:
        session = DBSession()
        return session
    else:
        return None

class EmployeeInfo(Base):
    __tablename__ = "Employee"

    s_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(String, nullable=True)

class SalaryInfo(Base):
    __tablename__ = "Salary"

    id = Column(Integer, primary_key=True, autoincrement=True)
    s_id = Column(Integer, ForeignKey('Employee.s_id'), nullable=False)
    dept_name = Column(String, nullable=True)
    sal = Column(Float, nullable=False)
