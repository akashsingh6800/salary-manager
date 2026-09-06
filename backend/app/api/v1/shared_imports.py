from sqlalchemy import func, select, or_
from sqlalchemy.orm import Session 
from app.db.dependencies import get_db
from app.models import Country, Department, Employee, SalaryHistory
from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.salary import SalaryHistoryItem, SalaryUpdateRequest



