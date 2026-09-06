from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EmployeeListItem(BaseModel):

    employee_id: str 
    first_name: str 
    last_name: str 
    email: str 
    country: str 
    department_str 
    job_title: str 
    employment_status: str 

    model_config = ConfigDict(from_attributes=True)

class EmployeeDetail(EmployeeListItem):
    id: int 
    created_at: datetime 
    updated_at: datetime 

class EmployeeListResponse(BaseModel):
    items: list(EmployeeListItem)
    total: int 
    page: int 
    page_size: int 
    total_pages: int 


