# General Dev Standards

This document will contain all general dev standards

1. NEVER use t.cast to resolve typed dicts transformation
   
   1. Take the time to set it down manually, this will let mypy actually raise an error if a value is not 

2. For any variable that is can get its value from an external source at runtime use pydantic to type check them.
   
   1. This would exclude static config files since they can be checked at the start of the program
   
   2. This would include user input, receiving values from an API, etc.

3. ALWAYS use mypy --strict to check that the code passes type checking.

4. Ignore checks are only permitted under the following circumstances:
   
   1. A type library needs to be imported but none exists. The ignore needs to be added to each import called in that area.
