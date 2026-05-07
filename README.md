# OpenViatica

OpenViatica is a data analytics platform builder and maintainer.

It is designed to be accessed using any of the following:

- Command Line Interface (CLI)
- Python Code
- Web based Application Programming Interface (API)

It handles data analytics problems with a local, python and SQL centered approach.

It is also bundled with tools & examples to handle common data analytics problems.

## Requirements

1. Windows, MacOS or Linux for some basic features
    - For a server setup, ONLY Linux is supported
2. **Python Version:** >= python 3.12

# Setup

1. Install the ``` uv ``` package: ``` pip install uv ```
2. Open a folder where you want to create the new workspace in VSCode
3. Open a terminal
4. Run: ``` uvx --no-cache --from openviatica ovutils ws init ```

## Contributor Steps

For the developers contributing to the project, there are other steps that need to be followed

1. Install the python package: uv
    - The steps for this differ depending on your OS, python version and other factors
2. Run this command at the root directory: ```uv sync```
3. To run any file use the ```uv run python {filepath}``` standard
4. Build the package using ```uv build```
5. To run automated tests use ```uv run pytest```
6. For manual tests:
    1. Find and save the path where the wheel file was created. Example: ```dist/openviatica-0.1.5-cp38-abi3-linux_x86_64.whl```
    2. Create another directory for testing
    3. Run ```uv init```
    4. Get the path to the wheel distribution file
    5. Run ```uv add <path_to_ditribution_wheel_file>```
    6. Run ```uv lock --upgrade-package openviatica```
    7. Conduct your test
    8. Implement changes in the source code if needed
    9. If any changes were implemented:
        1. Re-build package (Step 4)
        2. Run Automated Tests (Step 5)
        3. Update manual testing environment (Step 4.6)
        4. Re-conduct test and onward (Steps 4.7 onwards)
7. NOTE: A license header will be added to all files using the command:

    ```uv tool run licenseheaders -t ./docs/apache2.tmpl -o ftorres7382 -y 2026 -E py -E rs```

# Documentation

All of the documentation for the project can be found [here](docs/README.md)

# New Idea Submissions

- For any proposals/ideas or arquitecture changes send them to <ftorres7382@gmail.com> (at some point I would like to do the whole mailing list thing and keep track of community discussions that way or in any other way that does not depend on other companies)
  - I will give every idea a fair shot, but taking into account the project's vision while prioritizing a simple-first approach
  - Ideas are a good starting point, but after that, a proposal would have to be made on how that would be implemented, pros, cons and value
  - In general I consider the impact of the idea on the implementationt that are already there, the value of the idea, the complexity and the timeframe.
- If any of the documentation is not correct or contains typos, feel free to open a PR fixing only that.

# Licensing

1. [LICENSE](LICENSE): Apache 2.0
2. [NOTICE](NOTICE): Contains reserved trademarks
