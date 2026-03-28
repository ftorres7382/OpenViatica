


import typing as t

TEMPLATES_TOML_TYPE_ALLOWED_VALUES = t.Literal["TEMPLATE"]


class ovutils_types:
    
    class templates_types:
        class TEMPLATE_WORKSPACE_TOML_DICT_TYPE(t.TypedDict):
            type: TEMPLATES_TOML_TYPE_ALLOWED_VALUES
            id: str
            name: str 

    
    ANY_TYPE_DEF_TYPE = t.TypeVar("ANY_TYPE_DEF_TYPE")