# Contribution_Documentation
This is the directory for all the documentation on how someone can contribute to this project. 


If it is a little empty it is because I am the only one contributing right now.


# Coding Standards 
## (WARNING! Other standards could be added as the project matures!)

1. This project is python first and Rust whenever it is needed for performance or other reasons. 
    - To choosing rust for an implementation of a function or a feature needs to be justified by performance or other reasons. 
    - It needs also be integrated with the larger python codebase
    - As it stands right now, for any rust code, we would also need an integration strategy and testing before integrating out first rust code into the project.
2. lower_case_snake style by default for variables and functions
3. CamelCase for class names
4. Upper_Case_Snake for modules
5. Upper_Case_Snake for folder names
6. Type Check Standards: To mainatin the project correctly, we will need to enforce certain type safety standards even in python.
    1. Project MUST pass "mypy --strict" check
    2. ALL dynamic variables MUST use ```typeguard.check_type``` to validate their expected schema
        - This way, when the data mutates to a value we do not expect, the program just blows up and we know where to fix things.
    3. ALL functions MUST have the  ```typeguard.typechecked``` decorator to validate arguments on runtime
    4. Exceptions:
        - Scripts that require the minimum amount of packages installed for user experience.
    5. Notes:
        - This could be used to enforce type safety on the project as a whole but would still need some testing
        ```python
        from typeguard import install_import_hook

        # Call this at the very top of your entry point (e.g., main.py)
        install_import_hook('my_project_package')
        ```
9. AI is allowed, but: **YOU ARE RESPONSIBLE FOR THE CODE BEING SUBMITTED**.
    - The code submitted MUST conform to the coding standard and the scope of the project.
    - Using AI is allowed, but YOU will always be responsible for the code submitted.

# Steps for contribution

- Bugfixes and documentation typo fixes are always a foor icebreaker
- How to do contributions on new functionalities
    1. Read the documentation on the code [here](../Code_Documentation/README.md)
    2. Decide on an issue for a module/function/section in the that you want to work on
        - Maybe a section does not have all the functionality that it should have
        - Maybe there is an in progress section that no one is working on.
        - Maybe there could be an improvement to the current arquitecture.
            - In that case I´d accept proposals through email with a proposal or if its something more casual, use the github discussions. (I could add a proposal section to the GitHub discussions, but idk)
    3. Fork this repo
    4. You can work on it as you see in your own fork, but I would recommend following the process that the main repo will do so that there is better parity
    5. When you are done with the changes, these are the steps to start incorporating the work into the main branch.
        1. A branch_name will be determined based on what the scope of your work was supposed to address
        2. A new branch will be made in the main repo
            - Format: incoming/{branch_name}/{MM/dd/YYYY}
            - For contributions from the owner of the repo, the development/{branch_name}/{MM/dd/YYYY} will also be created.
        3. You will need to create a pull request towards that incoming branch
        4. In that branch a preliminary review will take place checking the following:
            1. Coding standards
            2. Running the code to check for the functionalities/fixes
            3. Running validations/tests
            4. Checking impacts to other modules
        5. Any changes would mean the developer would make the changes in their own fork and branch
            - I think the changes would show up on the pull request automatically after committing, but I am not sure (we can delete this once this is tested to be true)
        6. Once the review is done, the reviewer will do a pull request from incoming/{branch_name}{MM/dd/YYYY} to final_review/{branch_name}{MM/dd/YYYY}
        7. In there the final review will take place which should check similar things but with more rigor.
        8. If it fails, then the the final reviewer must make an itemized list of all the things wrong and send it back to step 4.
        9. If they pass, we should be able to merge the changes

# Coding/Standards Suggestions
I want to reserve this area for any coding standard suggestions I am considering but have not 100% decided on yet.


# Coding Standards Justifications
1. **ONLY RUST allowed for performance compiled programming needs**
    - The idea here is that I recognize that python might not be the only language we implement and that we might need the speed of another language
    - I am not a primarily Rust developer, but the strict enforcements of type and memory management standards makes sense to me
    - I kind of think of rust as the python for compiled languages
    - Of course all of the rust code created would add complexity to the project, so it would have to be justified.
    - I really like the defaults of the way that Rust does things. It keeps things clean by default. My biggest attraction is explicit behaviour represented in the code by default
    - It also supports packages and the like so that's also a super plus
    - Idea for another time though