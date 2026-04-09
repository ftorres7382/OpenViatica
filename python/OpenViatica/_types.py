

import typing_extensions as te
import typing as t

ov_ws_type_t = t.Literal["ov-meta-ws"]

class openviatica_workspace_types:
    ws_type_t: te.TypeAlias = ov_ws_type_t
    
    class TEMPLATE_WORKSPACE_TOML_DICT_TYPE(t.TypedDict):
        name: str
        id: str
        type:  ov_ws_type_t

    
    ANY_TYPE_DEF_TYPE = t.TypeVar("ANY_TYPE_DEF_TYPE")