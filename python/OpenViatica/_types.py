import typing_extensions as te
import typing as t

ov_ws_type_t = t.Literal["ov-meta", "ov-templates"]

meta_workspace_toml_type_value, templates_workspace_toml_type_value = t.get_args(
    ov_ws_type_t
)


class ov_ws_types:
    ws_type_t: te.TypeAlias = ov_ws_type_t

    # Common fields that all workspace types share
    class WORKSPACE_IDENTIFICATION_COMMON_FIELDS_DICT_TYPE(t.TypedDict):
        name: str
        id: str

    # What does the link or linked_by entry need to have
    class WORKSPACE_TOML_LINK_DICT_TYPE(
        WORKSPACE_IDENTIFICATION_COMMON_FIELDS_DICT_TYPE
    ):
        type: ov_ws_type_t
        workspace_tomlpath: str

    # Now the common fields for all workspaces
    class WORKSPACE_COMMON_FIELDS_DICT_TYPE(
        WORKSPACE_IDENTIFICATION_COMMON_FIELDS_DICT_TYPE
    ):
        linked_by: t.List["ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE"]

    # What should a workspace of any type contain
    # Made a different one
    #   because overriding after inheritance
    #   was not feasible thanks to strict type checking
    class GENERIC_WORKSPACE_TOML_DICT_TYPE(WORKSPACE_COMMON_FIELDS_DICT_TYPE):
        type: ov_ws_type_t

    class META_WORKSPACE_TOML_DICT_TYPE(WORKSPACE_COMMON_FIELDS_DICT_TYPE):
        type: t.Literal["ov-meta"]

        # list of the workspaces it links_to
        links_to: t.List["ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE"]

    class TEMPLATES_WORKSPACE_TOML_DICT_TYPE(WORKSPACE_COMMON_FIELDS_DICT_TYPE):
        type: t.Literal["ov-templates"]

    ANY_TYPE_DEF_TYPE = t.TypeVar("ANY_TYPE_DEF_TYPE")


# Other types
WORKSPACE_DEFAULT_METADATA_INFO_DICT_TYPE = t.Dict[
    # The key is one of the workspace types
    ov_ws_type_t,
    # The values are string but should be metadata path
    str,
]


#
