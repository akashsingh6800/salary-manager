from datetime import datetime 

from sqlalchemy import ForeignKey, String, Index 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base 

class Employee(Base):

    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index= True 
    )
    first_name: Mapped[str]= mapped_column(
        String(100),
        nullable=False 
    )
    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    email: Mapped[int] = mapped_column(
        String(255),
        unique = True,
        nullable= False,
        index = True 
    )

    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.id"),
        nullable = False,
        index = True 
    )

    department_id: Mapped[list["Employee"]] = mapped_column(
        ForeignKey("departments.id"),
        nullable = False,
        index = True
    )
    
    job_title:Mapped[str] = mapped_column(
        String(150),
        nullable = False 
    )

    employment_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False ,
        index =True 
    )

    created_at: Mapped[datetime] = mapped_column(
        default = datetime.utcnow,
        nullable = False 
    )

    updated_at: Mapped[datetime] = mapped_column(
        default = datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    country: Mapped["Country"] = relationship(
        back_populates="employees"
    )

    department: Mapped["Department"] = relationship(
        back_populates="employees"
    )

    salary_history : Mapped[list["SalaryHistory"]] = relationship(
        back_populates="employee",
        cascade = "all,delete-orphan"
    )

