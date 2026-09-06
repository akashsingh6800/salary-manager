from .shared_imports import *
router = APIRouter(
    prefix = "/employees",
    tags = ["Salary"]
)



@router.get("/{employee_id}/salary-history",response_model=list[SalaryHistoryItem])
def get_salary_history(employee_id: str, db: Session = Depends(get_db)):
    
    employee = db.scalar(
        select(Employee).where(
            Employee.employee_id == employee_id
        )
    )

    if not employee:
        raise HTTPException(
            status_code = 404,
            detail = "Employee not found"
        )
    
    records = db.scalars(
        select(SalaryHistory)
        .where(SalaryHistory.employee_id==employee.id)
        .order_by(SalaryHistory.effective_from.desc())
    )

    return records

@router.put("/{employee_id}/salary",response_model=SalaryHistoryItem)
def update_salary(employee_id: str,payload: SalaryUpdateRequest,db:Session = Depends(get_db)):

    employee = db.scalar(
        select(Employee).where(
            Employee.employee_id == employee_id
        )
    )

    if not employee:
        raise HTTPException(
            status_code = 404,
            detail = "Employee not found"
        )
    
    salary = SalaryHistory(
        employee_id = employee.id,
        salary = payload.salary,
        currency = payload.currency.upper(),
        effective_from = payload.effective_from,
    )

    db.add(salary)
    db.commit()
    db.refresh(salary)


    return salary 




