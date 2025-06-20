from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import CheckConstraint
from .Base import Base
from app import Custom_Types as T

class Principals(Base):
    __tablename__ = "Principals"

    ID: Mapped[str] = mapped_column(primary_key=True, unique=True, nullable=False)
    PRINCIPAL_ID: Mapped[str] = mapped_column(unique=True, nullable=False)
    TYPE: Mapped[str] = mapped_column(nullable=False)

    __table_args__ = (
        CheckConstraint(
            f"TYPE IN {str(tuple(T.Enums.get_enum_values_list(T.Enums.ALLOWED_PRINCIPAL_TYPES)))}",
            name="check_type_valid"
        ),
    )

    def __init__(self, ID: str, PRINCIPAL_ID: str, TYPE: str) -> None:
        self.ID = ID
        self.PRINCIPAL_ID = PRINCIPAL_ID
        self.TYPE = TYPE

