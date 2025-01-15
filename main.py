from fastapi import FastAPI
from uvicorn import run
from src.routes.all_routes import router
from src.db.model import init_db

#from src.routes.employee import router as emp_router
#print(emp_router)

app=FastAPI(title="Employee management System")

@app.on_event("startup")
async def init_process():
    init_db()

app.include_router(router)

if __name__=="__main__":
    run("main:app",host="0.0.0.0",port=8000, reload=True)