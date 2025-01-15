from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.routes.__init import get_db
from loguru import logger
from src.db.model import EmployeeInfo, SalaryInfo
from typing import Optional

router = APIRouter()

class EmployeeCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class SalaryCreate(BaseModel):
    s_id: int
    dept_name: Optional[str] = None
    sal: float

@router.get("/get_all_employees", tags=["View Employees"])
def get_all_employees(
        db: Session = Depends(get_db)
):
    try:
        res = db.query(EmployeeInfo).all()
        return {
            "status_code": 200,
            "detail": res
        }
    except Exception as e:
        logger.debug(f"Error occurred in get_all_employees - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
    


@router.get("/get_employee_by_id", tags=["View Employees"])
def get_employee_by_id(
        id: int,
        db: Session = Depends(get_db)
):
    try:
        res = db.query(EmployeeInfo).filter_by(s_id=id).all()
        return {
            "status_code": 200,
            "detail": res
        }
    except Exception as e:
        logger.debug(f"Error occurred in get_employee_by_id - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
    


@router.post("/add_new_employee", tags=["Manage Employee Information"])
def add_employee_info(
        info: EmployeeCreate,
        db: Session = Depends(get_db)
):
    try:
        employee_email = info.email
        employee_exists = db.query(EmployeeInfo).filter_by(email=employee_email).first()
        if employee_exists:
            logger.debug(f"Employee information already exists - {employee_email}")
            raise HTTPException(status_code=400, detail=f"Employee Email - {employee_email} information already exists")
        else:
            employee_add_info = EmployeeInfo(
                name=info.name,
                email=employee_email,
                address=info.address
            )
            db.add(employee_add_info)
            db.commit()
            return {
                "status_code": 200,
                "detail": (f"Employee Email - {employee_email} Information Added Successfully")
            }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database integrity error: {e}")
    except Exception as e:
        logger.debug(f"Error occurred in add_employee_info - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
    


@router.post("/add_salary_info", tags=["Manage Salary Information"])
def add_salary_info(
        info: SalaryCreate,
        db: Session = Depends(get_db)
):
    try:
        salary_add_info = SalaryInfo(
            s_id=info.s_id,
            dept_name=info.dept_name,
            sal=info.sal
        )
        db.add(salary_add_info)
        db.commit()
        return {
            "status_code": 200,
            "detail": f"Salary information for Employee ID - {info.s_id} Added Successfully"
        }
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database integrity error: {e}")
    except Exception as e:
        logger.debug(f"Error occurred in add_salary_info - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
    



@router.put("/update_employee_info", tags=["Manage Employee Information"])
def modify_employee_info(
        id: int,
        info: EmployeeCreate,
        db: Session = Depends(get_db)
):
    try:
        employee_name = info.name
        update_employee_info = db.query(EmployeeInfo).filter_by(s_id=id).update(info.dict(exclude_unset=True))
        if update_employee_info:
            db.commit()
            return {
                "status_code": 200,
                "detail": f"Employee Name - {employee_name} Information Modified Successfully"
            }
        else:
            logger.debug(f"Employee information not exists for ID - {id}")
            raise HTTPException(status_code=400, detail=f"Employee ID - {id} information does not exist")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.debug(f"Error occurred in modify_employee_info - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
    



@router.delete("/delete_employee", tags=["Manage Employee Information"])
def delete_employee_info(
        id: int,
        db: Session = Depends(get_db)
):
    try:
        res = db.query(EmployeeInfo).filter_by(s_id=id).first()
        if res:
            db.delete(res)
            db.commit()
            return {
                "status_code": 200,
                "detail": f"Employee ID - {id} Information Deleted Successfully"
            }
        else:
            logger.debug(f"Employee information not exists for ID - {id}")
            raise HTTPException(status_code=400, detail=f"Employee ID - {id} information does not exist")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.debug(f"Error occurred in delete_employee_info - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")




@router.get("/get_salary_info", tags=["View Salary Information"])
def get_salary_info(
        id: int,
        db: Session = Depends(get_db)
):
    try:
        res = db.query(SalaryInfo).filter_by(s_id=id).all()
        return {
            "status_code": 200,
            "detail": res
        }
    except Exception as e:
        logger.debug(f"Error occurred in get_salary_info - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
