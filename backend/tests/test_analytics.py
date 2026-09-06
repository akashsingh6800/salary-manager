
from sqlalchemy import text 

from fastapi.testclient import TestClient 
from app.main import app 

client = TestClient(app)



def test_analytics_summary():
    response = client.get("/api/v1/analytics/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_employees"] == 10000
    assert data["active_employees"] >=0 
    assert data["total_countries"] > 0 
    assert data["total_departments"] > 0 
