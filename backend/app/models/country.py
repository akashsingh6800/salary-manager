from sqlalchemy import String 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base 

class Country(Base):
    __tablename__ = "countries"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(100), unique = True, nullable=False)
    code: Mapped[str] = mapped_column(String(2), unique=True, nullable = False)

    employees: Mapped[list["Employee"]] = relationship(
        back_populates="country"
    )
