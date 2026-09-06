import random
from datetime import date 
from decimal import Decimal 

from sqlalchemy import delete 

from app.db.database import SessionLocal 
from app.models import Country, Department, Employee, SalaryHistory 

COUNTRIES = [
    ("India", "IN", "INR"),
    ("United States", "US", "USD"),
    ("United Kingdom", "GB", "GBP"),
    ("Germany", "DE", "EUR"),
    ("Singapore", "SG", "SGD"),
    ("Australia", "AU", "AUD"),
    ("Canada", "CA", "CAD"),
    ("France", "FR", "EUR"),
    ("Japan", "JP", "JPY"),
    ("United Arab Emirates", "AE", "AED"),
]

DEPARTMENTS = [
    "Engineering",
    "Finance",
    "Human Resources",
    "Sales",
    "Marketing",
    "Operations",
    "Legal",
    "Information Technology",
]

JOB_TITLES = [
    "Software Engineer",
    "Senior Software Engineer",
    "Staff Engineer",
    "Engineering Manager",
    "Data Analyst",
    "Data Engineer",
    "Product Manager",
    "Project Manager",
    "HR Manager",
    "HR Specialist",
    "Financial Analyst",
    "Accountant",
    "Sales Manager",
    "Sales Executive",
    "Marketing Manager",
    "Operations Manager",
    "Business Analyst",
    "Legal Counsel",
]

FIRST_NAMES = [
    "Aarav",
    "Vivaan",
    "Aditya",
    "Arjun",
    "Rahul",
    "Akash",
    "Rohan",
    "John",
    "James",
    "Robert",
    "Michael",
    "William",
    "David",
    "Daniel",
    "Emma",
    "Olivia",
    "Sophia",
    "Sarah",
    "Emily",
    "Mia",
]

LAST_NAMES = [
    "Singh",
    "Sharma",
    "Patel",
    "Kumar",
    "Gupta",
    "Mehta",
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Miller",
    "Davis",
    "Wilson",
    "Taylor",
]

SALARY_RANGES = {
    "IN": (600000, 3000000),
    "US": (50000, 200000),
    "GB": (30000, 120000),
    "DE": (40000, 130000),
    "SG": (40000, 160000),
    "AU": (50000, 160000),
    "CA": (50000, 150000),
    "FR": (35000, 120000),
    "JP": (4000000, 15000000),
    "AE": (60000, 200000),
}


def seed_database(employee_count: int = 10_000) -> None:
    random.seed(42)

    db = SessionLocal()

    try:
        db.execute(delete(SalaryHistory))
        db.execute(delete(Employee))
        db.execute(delete(Country))
        db.execute(delete(Department))
        db.commit()

        country_objects = []


        for name, code, currency in COUNTRIES:
            country = Country(
                name = name,
                code = code
            )

            country_objects.append(country)

        db.add_all(country_objects)

        department_objects = [
            Department(name = name)
            for name in DEPARTMENTS
        ]

        db.add_all(department_objects)

        db.commit()

        employees = []

        for index in range(1,employee_count + 1):
            country_name, country_code, currency = random.choice(COUNTRIES)

            country = next(
                country 
                for country in country_objects
                if country.code == country_code
            )

            department = random.choice(department_objects)

            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)

            employee = Employee(
                employee_id = f"EMP{index:05d}",
                first_name = first_name,
                last_name = last_name,
                email=f"employee{index}@acme.com",
                country = country,
                department = department,
                job_title = random.choice(JOB_TITLES),
                employment_status = random.choice(
                    ["ACTIVE", "ON_LEAVE", "INACTIVE"]
                )
            )

            employees.append(employee)

        db.add_all(employees)
        db.commit()

        for employee in employees:
            db.refresh(employee)
        
        salary_records = []

        for employee in employees:
            country_code = employee.country.code
            currency = next(
                item[2]
                for item in COUNTRIES
                if item[1] == country_code
            )

            minimum, maximum = SALARY_RANGES[country_code]

            current_salary = random.randint(minimum, maximum)

            salary_records.append(
                SalaryHistory(
                    employee_id = employee.id,
                    salary=Decimal(current_salary),
                    currency = currency,
                    effective_from = date(2026,1,1)
                )

            )

            if employee.id % 2 ==0:
                previous_salary = int(current_salary * 0.9)

                salary_records.append(
                    SalaryHistory(
                        employee_id = employee.id,
                        salary = Decimal(previous_salary),
                        currency = currency,
                        effective_from = date(2025,1,1)
                    )

                )
        db.add_all(salary_records)
        db.commit()

        print(f"Successfully seeded {employee_count} employees.")


    except Exception:
        db.rollback()
        raise 

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()     


