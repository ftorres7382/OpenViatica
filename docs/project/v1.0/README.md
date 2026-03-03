# v1.0 Planning and Documentation
This is the documentation of the features and of the several steps to get to a v1.0

# Definitions
1. Datasets: 
    - NOTE: I know that different groups consider small and medium datasets to be completely different. This is just the definition this documentation provides from the perspective of the user being defined. 
    1. small dataset = < 1GB 
    2. medium dataset = >= 1GB and < 25GB


# User Profile & Requirements (UP&R)
1. This version is aimed at the user that wants to do local data analytics in their local environment for report outs and the like.
2. This user has the following requirements:
    1. Wants a local data analytics platform to help him be able to tackle small to medium datasets with the following tasks in their local work computer:
        1. Data Ingestion
        2. Data Processing 
        3. Data Visualization
        4. Visualization Dashboards
        5. Mapping business concepts with their data
        6. Workflows to refresh things on a schedule
        7. Listeners that can trigger a workflow upon custom requirements
        8. Able to customize the environment to their needs
        9. Must alow the use of python, IPython or Jupyter Notebooks
        10. The use of localhost or local ports must be optional. Since the uesr could be in a very security restricted environment.
        11. Must support Windows & Linux
    2. Has a need for examples on some of the best tools out there for the data they are working with.
    3. Wants a workspace environment that is easy to start and deep enough to support his needs.

# Planned Features (PL)
1. **Python Based Environment:** Since python is one of the leading standards for flexible data analytics platforms, this is what will be used as the base of the environment.
2. **Windows & Linux Support:** Since the user is a normal corporate office worker person trying to do reports and data analysis and since most of the corporate world uses Windows right now, the features listed below should be supported on both Windows and Linux.
    - To accomplish this, python will be used as the main method of execution since it is cross-platform
3. **Workspace Creation:** Allows the user to create a new workspace and define the configuration settings using CLI, config files or Python code
4. **Workspace Python Environment Configuration:** The program has a system to define the python virtual environment of the workspace. 
    1. The program is capable of creating the workspace with no virtual environment setup.
    2. The program has a minimal preset for virtual environment modules.
    3. The program has a complete preset for the virtual environment that allows for working from small to medium datasets.
    4. The program allows the user to choose which preset to start the workspace in.
    5. The program allows the user to add requirements on top of the presets chosen by the user. These should be installed right after workspace initialization
5. **Workspace Lifecycle Methods:** The workspace will have a lifecycle system so that the user can execute the functions they need when starting their work.
    1. It will come with the most basic of lifecycle steps:
        1. **init**: Creates a new workspace
        2. **activate**: Activates the python virtual environment and whatever the workspace needs "activated"
            - Will use the same python activation methods
        3. **start**: A hook for starting up any types of services or actions to do whenever work starts on the workspace
        4. **stop**: A hook for stopping any services or actions to do whenever the workspace stops.
    2. It will let the user add any steps in between the basic lifecycle steps
    3. By default, the lifecycle steps will need to be run manually by the user
    4. The program should let the user define which stages should be run automatically after which stage has been called
    5. The program should let the user add steps to any part of the lifecycle
    6. Extra init steps should be configurable before workspace creation.
    7. Any lifecycle steps should be configurable after workspace initialization
        - NOTE: The user or program can add to the init step to make a defuault workspace configuration of their liking
    8. Workspace should have a way to configure the lifecycle steps using files, CLI, API or python modules/classes/functions
6. **Workflows System:** The program must install a custom workflows system solution, since we need it to be windows and linux compatible and because there are not agreed upon standard solutions for this.
    1. Must contain a way to script events and define programs
    2. Must contain a way to run them on demand
    3. Must contain a way to run them upon a trigger
        1. Trigger can be set using the linux standard way of setting up recurring events (idk what that is called tbh)
        2. Trigger can be a custom user defined checks
        3. Must be callable using CLI, Python or API
7. **Data & Concept Map Integration:** The program must have a concept map that the user can definne that is capable of integrating with the data.
    - Best way to achieve this is to make a translation layer from the concept map to SQL commands.
8. **Workspace Folder Structure:** Must contain a folder structure helping guide the user on how they should structure their own work.
    1. Data: For holding data
    2. Repos: For holding code repositories
    3. Home: For a scratch area to play around in
    4. Code_Flows: For workflows. These would be defined using code
    5. Concept_Map: For defining a data concept map
    6. Services: For defining anything like docker or other services that could need to be tarted up by the user. 
        - Could also be ued for docker files that setup and deploy applications in the Apps folder.
    7. Apps: For creating data applications like APIs, webpages, etc.
    8. The workspace folder structure MUST be configurable on or after initialization
    
# Out of Scope Features
1. **Access/permission Control:** This is because of item 1 in the user profile
    - Since this user is envisioning only themselves using it, we will not support this feature for this version. 
    - We should still think about how we want to make the v1.0 still compatible with whenever we do want permission control
    - I am thinking just leveraging file permissions on linux for all permission controls in the first implementation. But still needs to be determined

# Features Version Plan
In this section, the versioning plan is defined. Only the current development and the next version will be defined.

1. v1.0
    1. v0.1 - Integration version
        - Created a simple fibonacci calculating python that can calculate fibonacci numbers manually.
        - Created a working rust fibonacci calculating python function
        - Posted the ovutils to Pypi
        - Installable using pip as ovutils
        - Useable in Windows and Linux
        - Callable in python code or CLI
    2. v0.2 - Complete workspace initialization feature
        - Workspace name & ID
            - Ability to modify after initialization through CLI or config files
        - venv config
            - Ability to modify after initialization (use hatch, uv or pip with pyproject.toml)
        - Defined folder structure
            - Ability to add the optional folders
        - Testing
    3. v0.3 - Workspace Lifecycle Feature
        - Ability to run things before & after each workspace lifecycle 
            - "init"
            - AFTER Terminal entry to workspace folder
            - AFTER venv activation
            - AFTER running custom "activate" command
            - "start"
            - "stop"
        - uv could be used as the standard for running these things
        - We should assume that there could be multiple .venvs for the same workspace and that each one sets up different things. Thus we can say that different workflows can be run depending on the venv activation and the start and stop can be venv dependent (we can make this mandatory)
    4. v0.4 - v1.0 Workflow tool integration
    5. v0.5 - v1.0 Concept Map tool integration
    6. Validation for v1.0 release

# Requirement Fulfillment
I much prefer diagrams to represent the fulfillment of the requirements, even though this can make it a little harder to track. Right now I want to understand and make sure that the requirements are sound.


PS: Some of these diagrams could look hard to read. To read them, just try to focus on one thing that might be of interest to you and see what connections that box has with others.


![Diagram link](./Interactions_Diagram.drawio)