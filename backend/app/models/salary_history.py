from datetime import date, datetime
from decimal import Decimal 

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String 
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from app.db.database import Base 

class SalaryHistory(Base):
    __tablename__ = "salary_history"

    id: Mapped[int] = mapped_column(primary_key=True)

    employee_id : Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
        index = True 
    )

    salary: Mapped[Decimal] = mapped_column(
        Numeric(15,2),
        nullable=False 
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False 
    )

    effective_from: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index = True 
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="salary_history"
    )
