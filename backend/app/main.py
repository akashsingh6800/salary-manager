from fastapi import FastAPI 

from app.api.v1.salaries import router as salary_router
from app.api.v1.analytics import router as analytics_router

from app.api.v1.employees import router as employee_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title = "ACME Salary Management API",
    description="API for managing employee salary information and compensation analytics.",
    version = "1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers = ["*"]
)


app.include_router(
    salary_router,
    prefix="/api/v1"
)

app.include_router(
    analytics_router,
    prefix = "/api/v1"
)

app.include_router(
    employee_router, 
    prefix = "/api/v1"
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}