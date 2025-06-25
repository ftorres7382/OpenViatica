This folder is where the workspace users will interact and connect to.

This workspace comes pre-installed with the following python modules, through the .venv folder:

1. Data Analysis:
   
   1. pandas
   
   2. polars
   
   3. duckdb
   
   4. ibis

2. Data Visualization
   
   1. matplotlib
   
   2. plotly
   
   3. seaborn

3. Extras:
   
   1. Jupyter
      
      1. NOTE: Jupiter notebooks are NOT recommended, the **jupitext** VS code module is preferred if you want a jupyter notebook style interface for your programming
      
      2. Drawbacks of jupiter notebooks:
         
         1. If not set up correctly in github, they can commit actual data to the repo, making the repo hast to manage and causing possible data leaks.
         
         2. The workspace does not support jupyter notebooks by default, some features will be mising as a result