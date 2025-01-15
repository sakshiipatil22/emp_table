from fastapi import APIRouter, FastAPI
from src.routes.employee import router as emp_router

router=APIRouter()

router.include_router(emp_router)