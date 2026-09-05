from fastapi import FastAPI 

app = FastAPI(
    title = "ACME Salary Management API",
    description="API for managing employee salary information and compensation analytics.",
    version = "1.0.0",
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}