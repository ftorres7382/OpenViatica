# Documentation
This is the landing folder for any and all documentation. This would include Code, project, teams and other types of documentation related to the OpenViatica project.

# Steps to Use Documentation
The documentation should be mostly followable using the Github Page using the readmes, except for the embedded drawio diagrams. 

To see those, or to see mkdocs documentation, you would have to clone the repo and follow the steps below:

- Follow [Contributor Setup Steps](../../README.md#contributor-setup-steps) to setup the venv
- Serve using mkdocs:
    - In project root:
        ```bash
        mkdocs serve -f Project_Source/mkdocs/mkdocs.yml
        ```
    - (Optionally) Add the --livereload for automatic reloads after edits
        ```bash
        mkdocs serve -f Project_Source/mkdocs/mkdocs.yml --livereload
        ```