

import typing_extensions as te
import typing as t

ov_ws_type_t = t.Literal["ov-meta", "ov-templates"]

meta_workspace_toml_type_value, templates_workspace_toml_type_value = t.get_args(ov_ws_type_t)

class ov_ws_types:
    ws_type_t: te.TypeAlias = ov_ws_type_t
    

    class _COMMON_FIELDS_DICT_TYPE(t.TypedDict):
        name: str
        id: str
    
    class BASE_WORKSPACE_TOML_DICT_TYPE(_COMMON_FIELDS_DICT_TYPE):
        type:  ov_ws_type_t
    
    class META_WORKSPACE_TOML_MANAGES_DICT_TYPE(BASE_WORKSPACE_TOML_DICT_TYPE):
        workspace_tomlpath : str

    class META_WORKSPACE_TOML_DICT_TYPE(_COMMON_FIELDS_DICT_TYPE):
        type: t.Literal["ov-meta"]

        # list of the workspaces it manages
        manages: t.List["ov_ws_types.META_WORKSPACE_TOML_MANAGES_DICT_TYPE"]
        

    
    ANY_TYPE_DEF_TYPE = t.TypeVar("ANY_TYPE_DEF_TYPE")