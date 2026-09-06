from .shared_imports import *



router = APIRouter(
    prefix="/employees",
    tags = ["Employees"],
)

@router.get("")
def get_employees(
    page: int = Query(1,ge=1),
    page_size: int = Query(10,ge=1,le=100),
    search: str | None = None,
    db: Session = Depends(get_db),
):
    query = select(Employee)

    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Employee.employee_id.ilike(search_term),
                Employee.first_name.ilike(search_term),
                Employee.last_name.ilike(search_term),
                Employee.email.ilike(search_term),
            )
        
        )
    
    total = db.scalar(
        select(func.count())
        .select_from(query.subquery())
    ) or 0
    
    employees = db.scalars(
        query
        .order_by(Employee.id)
        .offset((page-1)* page_size)
        .limit(page_size)
    ).all()

    return {
        "items": [
            {
                "employee_id": employee.employee_id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email" : employee.email,
                "country": employee.country.name,
                "department": employee.department.name,
                "job_title": employee.job_title,
                "employment_status": employee.employment_status
            }
            for employee in employees
        ],
        "page": page,
        "page_size": page_size,
        "total": total
    }


@router.get("/{employee_id}")
def get_employee(
    employee_id: str,
    db: Session = Depends(get_db),
):
    employee = db.scalar(
        select(Employee).where(Employee.employee_id == employee_id)
    )

    if not employee:
        raise HTTPException(
            status_code = 404,
            detail = "Employee not found"
        )
    
    return {
        "employee_id": employee.employee_id,
        "first_name": employee.first_name,
        "last_name": employee.last_name,
        "email": employee.email,
        "country": employee.country.name,
        "department": employee.department.name,
        "job_title": employee.job_title,
        "employment_status": employee.employment_status
    }

