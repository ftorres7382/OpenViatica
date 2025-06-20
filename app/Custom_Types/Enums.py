import typing as t
import typing_extensions as te


ALLOWED_SQL_ENGINES = t.Literal["sqlite", "postgres"]
ALLOWED_PRINCIPAL_TYPES = t.Literal["user", "group"]

def get_enum_values_list(literal_type: t.Any) -> list[t.Any]:
    '''
    This function expectes a t.Literal[] data type definition and returns a list of the values that were defined
    '''
    return list(te.get_args(literal_type))
