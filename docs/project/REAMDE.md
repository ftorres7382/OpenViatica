# Project Documentation
The purpose of this area is to contain all the relevant documentation about the project scope and its intended supported features in the future

# Terms & Definitions
1. user-space
    1. Any interface that is documented or presented as stable for user consumption is considered part of user-space and is covered by the project’s compatibility guarantees. 
    2. This term is used a lot in the linux community and this project aims to keep a similar promise.
    3. This would apply to the following:
        1. CLI commands and flags intended for the user(s)
        2. APIs intended for the user(s)
        3. Config files intended for the user(s) to configure any of the underlying tools
        4. Python Modules, classes, functions or files intended for the user(s)
        5. Rust Modules, classes, functions or files intended for the user(s)
        5. User(s) workspace folder structures, names, configurations and established features
    4. This would NOT include:
        1. Internal modules, classes, functions or files
        2. Internal class structure
        3. Private functions
        4. Internal file layout
        5. Implementation language (ie. Python or Rust)

# Version System
1. The project's versions will be denoted by the following template: **v{major_version}.{minor_version}.{patched_version}{optional:"-lts"}**. 
    1. The versions with "-lts" in the version name are considered to be long term support versions
        1. For this project. Long Term Support means no breaking changes to user-space for the duration of the LTS period.
        2. It also means that it will receive patches for the next 2 years for any bugs on it.
    2. Major versions may introduce significant internal architectural changes or large feature additions, while preserving user-space compatibility.
        1. The major versions will always increment by 1 number
    4. Minor versions introduce new, backward-compatible user-facing features within the same major version.
    5. The patched version would indicate that the specific major and minor version needed patching so that is what was released.
    6. Examples: 
        1. v1.0 is released but bugs are found, this would mean that v1.0.1 will be created to fix it.
        2. v1.0 is out, but now we want to add some list of functionalities under the same system it would be v1.1
        3. Any other commits that do not have a tag are just incremental versions of the code
2. Deprecation Policy
    1. User-space features may be deprecated but will not be removed.
    2. Deprecated features will continue to function and may emit warnings indicating preferred alternatives.

# Project Planning Strategy
1. Identifying features to be added
    1. Identify the types of users we want this program to serve to. 
    2. Identify what features they will need to fulfill their Data Analytics requirements
    3. Plan those features around the version system.
2. Features will be added from simplest and impactful to more complex and impactful.
3. Things scoped in a major version can be subject to change based on the version's goals.
4. Minor versions are better defined.

# Planning documentation
1. [v1.0 Plan](./v1.0/README.md)
    