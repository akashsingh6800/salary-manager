from .shared_imports import *

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/summary")
def get_summary(db : Session = Depends(get_db)):

    total_employees = db.scalar(
        select(func.count(Employee.id))
    ) or 0 

    active_employees = db.scalar(
        select(func.count(Employee.id)).where(
            Employee.employment_status == "ACTIVE"
        )
    ) or 0 

    total_countries = db.scalar(
        select(func.count(Country.id))
    )

    total_departments = db.scalar(
        select(func.count(Department.id))
    ) or 0 

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "total_countries": total_countries,
        "total_departments": total_departments
    }

@router.get("/by-country")
def salary_by_country(db: Session = Depends(get_db)):


    latest_salary = (
        select(
            SalaryHistory.employee_id,
            func.max(SalaryHistory.effective_from).label("latest_date"),
        )
        .group_by(SalaryHistory.employee_id)
        .subquery()
    )

    query = (
        select(
            Country.name.label("country"),
            SalaryHistory.currency,
            func.avg(SalaryHistory.salary).label("average_salary"),
            func.count(Employee.id).label("employee_count"),
        )
        .join(Employee, Employee.country_id==Country.id)
        .join(
            latest_salary,
            latest_salary.c.employee_id == Employee.id
            )
        .join(
            SalaryHistory,
            (SalaryHistory.employee_id == Employee.id)
            & (SalaryHistory.effective_from == latest_salary.c.latest_date),
        )
        .group_by(
            Country.name,
            SalaryHistory.currency,
        )
        .order_by(Country.name)
    )

    results = db.execute(query).all()

    return [
        {
            "country": row.country,
            "currency": row.currency,
            "average_salary": round(float(row.average_salary),2),
            "employee_count": row.employee_count
        }
        for row in results
    ]


@router.get("/by-department")
def salary_by_department(db: Session = Depends(get_db)):

    latest_salary = (
        select(
            SalaryHistory.employee_id,
            func.max(SalaryHistory.effective_from).label("latest_date"),
        )
        .group_by(SalaryHistory.employee_id)
        .subquery()
    )

    query = (
        select(
            Department.name.label("department"),
            SalaryHistory.currency,
            func.avg(SalaryHistory.salary).label("average_salary"),
            func.count(Employee.id).label("employee_count")
        )
        .join(
            Employee,
            Employee.department_id == Department.id
        )
        .join(
            SalaryHistory,
            SalaryHistory.employee_id == Employee.id,
        )
        .join(
            latest_salary,
            latest_salary.c.employee_id == Employee.id,
        )
        .group_by(
            Department.name,
            SalaryHistory.currency,
        )
        .order_by(Department.name)
    )

    results = db.execute(query).all()

    return [
        {
            "department": row.department,
            "currency": row.currency,
            "average_salary": round(float(row.average_salary),2),
            "employee_count": row.employee_count
        }
        for row in results
    ]
