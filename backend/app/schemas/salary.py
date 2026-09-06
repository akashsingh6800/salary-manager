from datetime import date 
from decimal import Decimal 

from pydantic import BaseModel, Field


class SalaryHistoryItem(BaseModel):
    salary: Decimal
    currency: str 
    effective_from: date 
    model_config = {
        "from_attributes": True 
    }


class SalaryUpdateRequest(BaseModel):
    salary: Decimal = Field(gt=0)
    currency: str = Field(min_length=3,max_length=3)
    effective_from : date
