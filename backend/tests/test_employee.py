
from sqlalchemy import text 

from fastapi.testclient import TestClient 
from app.main import app 

client = TestClient(app)

def test_get_employee():

    response = client.get("/api/v1/employees/EMP00001")

    assert response.status_code == 200 
    data = response.json()

    assert data["employee_id"] == "EMP00001"
    assert "first_name" in data
    assert "last_name" in data 
    assert "email" in data 
    assert "country" in data 
    assert "department" in data



def test_get_salary_history():

    response = client.get(
        "/api/v1/employees/EMP00001/salary-history"
    )

    assert response.status_code == 200
    
    data = response.json()

    assert isinstance(data,list)

    if data:

        assert "salary" in data[0]
        assert "currency" in data[0]
        assert "effective_from" in data[0]



def test_update_salary():

    response = client.put(
        "/api/v1/employees/EMP00001/salary",
        json={
            "salary": 125000,
            "currency": "USD",
            "effective_from": "2026-09-07"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["salary"] == "125000.00"
    assert data["currency"] == "USD"
    assert data["effective_from"] == "2026-09-07"
