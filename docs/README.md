# Documentation
This is the overview any and all documentation. This would include Code, project, teams and other types of documentation related to the OpenViatica project.

# Steps to Use Documentation
The documentation should be mostly followable using the Github Pages and by using the readmes. Although these would not include the embedded drawio diagrams. 

To see those, you will have to follow the [mkdocs steps](#mkdocs-steps)

# Documenation Links
1. [code](code/README.md): Contains all the documentation on code purpose, overall design, arquitecture, modes and configuration. It basically explains how the current version works.
2. [contributions](contributions/README.md): Contains all the standards for how to contribute to this project.
3. [project](project/README.md): Contains all the documentation for the project like planned features and project timeline


# MkDocs Steps
To see the MkDocs documentation you will have to clone the repo and follow the steps below:

- Follow [Contributor Setup Steps](../README.md#contributor-steps) to setup the venv
- Serve using mkdocs:
    - **In the project root**:
        ```bash
        uv run mkdocs serve
        ```
    - (Optional) Add the --livereload for automatic reloads after edits
        ```bash
        uv run mkdocs serve --livereload
        ```