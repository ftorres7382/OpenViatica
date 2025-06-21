from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base

class Workspaces(Base):
    __tablename__ = "Workspaces"

    ID: Mapped[str] = mapped_column(primary_key=True, unique=True, nullable=False)
    WORKSPACE_NAME: Mapped[str] = mapped_column(unique=True, nullable=False)
    # This can later be changed to wherever the workspace is being hosted and the like
    WORKSPACE_FOLDER_PATH: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    def __init__(self, ID: str, WORKSPACE_NAME: str, WORKSPACE_FOLDER_PATH: str) -> None:
        self.ID = ID
        self.WORKSPACE_NAME = WORKSPACE_NAME
        self.WORKSPACE_FOLDER_PATH = WORKSPACE_FOLDER_PATH

