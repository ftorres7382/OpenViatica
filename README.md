# OpenViatica
OpenViatica is an open source CLI, API and code-based data analytics platform builder and maintainer. It comes with tools & examples to handle common data analytics problems with a local first and python centered approach.  

## Requirements:
1. Windows, macOS or Linux for some basic features
    - For a server setup, ONLY Linux is supported
2. **Python Version:** >=python3.12

# Setup
1. Install the python package called: ```uv```
2. Open a folder where you want to create the new workspace in VSCode
3. Open a terminal
4. Run: ``` uvx --no-cache --from openviatica ovutils ws init ```


## Contributor Steps
For the developers contributing to the project, there are other steps that need to be followed
1. Install the python package: uv
    - The steps for this differ depending on your OS, python version and other factors
2. Run this command at the root directory: ```uv sync```
3. To run any file use the ```uv run python {filepath}``` standard
4. To run tests use ```uv run pytest```
5. NOTE: A license header will be added to all files using the command:

    ```uv tool run licenseheaders -t ./docs/apache2.tmpl -o ftorres7382 -y 2026 -E py -E rs```

# Documentation
All of the documentation for the project can be found [here](docs/README.md)

# New Idea Submissions
- For any proposals/ideas or arquitecture changes send them to ftorres7382@gmail.com (at some point I would like to do the whole mailing list thing and keep track of community discussions that way or in any other way that does not depend on other companies)
    - I will give every idea a fair shot, but taking into account the project's vision while prioritizing a simple-first approach
    - Ideas are a good starting point, but after that, a proposal would have to be made on how that would be implemented, pros, cons and value
    - In general I consider the impact of the idea on the implementationt that are already there, the value of the idea, the complexity and the timeframe.
- If any of the documentation is not correct or contains typos, feel free to open a PR fixing only that.

# Licensing
1. [LICENSE](LICENSE): Apache 2.0
2. [NOTICE](NOTICE): Contains reserved trademarks

