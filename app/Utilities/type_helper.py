'''
This file will contain the functions and variables that can halpe with handling type hinting better
'''
import typing as t
class Type_Helper():
    def __init__(self) -> None:
        pass

    def extract_key_structure(self, typed_dict_class: type) -> dict[str, t.Any]:
        key_structure = {}
        hints = t.get_type_hints(typed_dict_class)

        for key, hint in hints.items():
            # If it's another TypedDict (nested)
            if isinstance(hint, type) and hasattr(hint, '__annotations__'):
                key_structure[key] = self.extract_key_structure(hint)
            else:
                key_structure[key] = None  # Leaf keys set to None

        return key_structure