'''
This file will contain the functions and variables that can halpe with handling type hinting better
'''
import typing as t

class Type_Helper():
    def __init__(self) -> None:
        pass
    
    

    # def get_type_structure(self, typed_dict_class: type) -> dict[str, t.Any]:
    #     '''
    #     Returns a dictionary with the same key structure as the typed dict, 
    #     but with specific class of the type it should be.

    #     This should help validate by using the isinstance on the structure
    #     '''
    #     type_structure = {}
    #     type_hints = t.get_type_hints(typed_dict_class)

    #     for key, type_hint in type_hints.items():
    #         # If it's another TypedDict (nested)
    #         if isinstance(type_hint, type) and hasattr(type_hint, '__annotations__'):
    #             type_structure[key] = self.get_type_structure(type_hint)
    #         else:
    #             type_structure[key] = type_hint

    #     return type_structure
    # #                                                               Should this be changed to check for a class type?
    # def check_type(self, value: t.Any, expectation: t.Union[type, dict[str, t.Any]]) -> None:
    #     '''
    #     This will compare all the values to the defined type.
    #     If the types or the dictionary structure are not the same, it will raise an error

    #     expectation can be a 
    #         1. python vanilla value vs type class: The basic python type, that will be checked with isinstance
            
    #         2. dictionary vs a type structure dictionary:
    #             - The type structure dictionary would have the same key structure as the value, 
    #                 but has a list of acceptable type classes in the value for each key

    #         3. list vs a list type structure:
    #             - Has the same structure as the list, but contains a list of the acceptable types for each  value
            
    #         4. dictionary value vs Typed Dict type: 
    #             - Checks the value against the typed dict structure and python types. 
    #             - Uses recursion to go up the ladder
            
    #         5. List value vs typing options
    #     '''
    #     #                           Annotations is a safer way to check for something like a typed dict
    #     if isinstance(expectation, type) and hasattr(expectation, "__annotations__"):
    #         # If we are in here, then the value must be a dictionary, otherwise something went wrong
    #         if not isinstance(value, dict):
    #             raise ValueError("ERROR! A Typed Dict like value has been sent to 'expectation', but 'value' is not a dict type. Recevied '{type(value)}' type for 'value' ") 
    #         expected_type_structure = self.get_type_structure(expectation)
    #     # else the thing that was sent was a type structure
    #     else:
    #         expected_type_structure = expectation
        
    #     # If the the expectaion is a dict, we need to recurse
'''
def check_dict(self, 
               value: t.Any, 
               expectation: t.Union[type, dict[str, t.Any]]) -> None:
    \'\'\'
    Recursively checks a value against either:
    - a TypedDict class
    - or a dictionary of expected types (already extracted)
    \'\'\'

    # If expectation is a TypedDict class, get its structure
    if isinstance(expectation, type) and hasattr(expectation, '__annotations__'):
        expected_structure = self.get_type_structure(expectation)
        if not isinstance(value, dict):
            raise TypeError(f"Expected dict for {expectation.__name__}, got {type(value).__name__}")
    else:
        expected_structure = expectation

    if isinstance(expected_structure, dict):
        if not isinstance(value, dict):
            raise TypeError(f"Expected dict, got {type(value).__name__}")

        for key, expected_type in expected_structure.items():
            if key not in value:
                raise KeyError(f"Missing key: '{key}'")
            self.check_dict(value[key], expected_type)

    elif hasattr(expected_structure, '__origin__'):
        origin = expected_structure.__origin__

        if origin is list:
            if not isinstance(value, list):
                raise TypeError(f"Expected list, got {type(value).__name__}")
            item_type = expected_structure.__args__[0]
            for item in value:
                self.check_dict(item, item_type)

        elif origin is dict:
            if not isinstance(value, dict):
                raise TypeError(f"Expected dict, got {type(value).__name__}")
            key_type, val_type = expected_structure.__args__
            for k, v in value.items():
                self.check_dict(k, key_type)
                self.check_dict(v, val_type)

        elif origin is t.Union:
            if not any(self._safe_check_type(value, opt) for opt in expected_structure.__args__):
                raise TypeError(f"Value '{value}' does not match any allowed types {expected_structure.__args__}")

        else:
            raise NotImplementedError(f"Unsupported generic: {origin}")

    else:
        if not isinstance(value, expected_structure):
            raise TypeError(f"Expected {expected_structure}, got {type(value).__name__}")

'''

        

    # def check__dict_against_expected_type_structure(self, 
    #                                        value: t.Any, 
    #                                        expected_type: t.Any
    #                                        ):
    #     '''
    #     This class checks the value dict against another dictionary that has the same key structure, 
    #     but a class of what type it should be 
    #     '''
    #     # If the value is not a dictionary, check its type
    #     if not isinstance(value, dict):
    #         if not isinstance(value, expected_type):
    #             raise TypeError(f"ERROR! Expected '{expected_type}', but got '{type(value)}' instead!")
    #     else:
    #         # If it is a dictionary, we need to recurse
    #         # What about lists tho?

        