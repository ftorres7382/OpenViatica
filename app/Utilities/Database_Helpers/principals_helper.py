import typing as t
import sqlalchemy.orm as sqla_orm
import uuid
from email_validator import validate_email, EmailNotValidError


from app.Database_Models import Principals
from app.Utilities import Sqla_Helper
from app import Custom_Types as T

class Principals_Helper():
    
    def __init__(self) -> None:
        self.sqla_helper = Sqla_Helper()
        

    def add_principal(self, principal_ID: str, principal_type: T.Enums.ALLOWED_PRINCIPAL_TYPES) -> None:
        '''
        This function adds a new entry to the Principals table
        '''
        # Validate the arguments
        allowed_principal_types = T.Enums.get_enum_values_list(T.Enums.ALLOWED_PRINCIPAL_TYPES)
        if principal_type not in allowed_principal_types:
            raise ValueError(f"ERROR! The allowed types for 'principal_type' are: {allowed_principal_types}")
        
        # user types must be emails
        if principal_type == "user":
            # Then the principal_ID must be an email
            try:
                # This will throw if invalid
                valid = validate_email(principal_ID)
                principal_ID = valid.email  # This is normalized (e.g., lowercased)
            except EmailNotValidError as e:
                raise ValueError(f"Invalid email: {e}")

        
        id = str(uuid.uuid4())

        with sqla_orm.Session(self.sqla_helper.get_engine()) as session:

            # Check if the entry already exists
            new_principal = Principals(
                ID=id,
                PRINCIPAL_ID=principal_ID,
                TYPE=principal_type
            )
            session.add(new_principal)
            session.commit()

        



