import sqlalchemy as sqla
from .Base import Base

class Principals(Base):
    __tablename__ = "Principals"

    ID = sqla.Column(sqla.String, primary_key=True)
    TYPE = sqla.Column(sqla.String, nullable=False)

    __table_args__ = (
        sqla.CheckConstraint("TYPE IN ('user', 'service', 'group')", name="check_type_valid"),
    )