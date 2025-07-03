# OpenViatica

This repository contains the  code for the OpenViatica software. It is intended to be a fully local hosting of a data analysis environment.

# OS Level Rquirements

1. Windows is supported for simple personal use or moderate collaborative use
2. Linux is supported for more complex or server implementations
3. python 3.12 is recommended

# Generic setup instructions

1. Clone repo
2. Create & activate .venv
   1. python -m venv .vev
   2. or:
   3. python3 -m venv .venv
3. Activate .venv environment
   1. pip install poetry
4. Install requirements.txt
   1. poetry install
5. python OpenViatica.py
   - This will set all the settings for the local use of the tool. Enterprise configurations to come later...
     5- Enterprise recommendations:
     1- Use linux...
     2- Create a OpenViatica App Admin group
     3- Add the accounts necessary to the group
     4- Change the permissions to 700 but only to the OpenViatica App Admin group
     5- Make sure to limit and monitor these access, access to the app files compromises everything in the app itself