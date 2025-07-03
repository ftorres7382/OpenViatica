This folder is where the workspace users will interact and connect to.

This workspace comes pre-installed with the following python modules, through the .venv folder:

1. Data Analysis:
   
   1. pandas: Small to medium size Dataframes
   
   2. polars: Medium to large DataFrames
   
   3. duckDB: Large to XL DataFrames
   
   4. ibis: For a single API to handle pandas, polars or duckDB

2. Data Visualization
   
   1. matplotlib: Static visualization plots
   
   2. plotly: Interactive visualization plots
   
   3. seaborn: For easy and fast visualizations
   
   4. dash: For serving Data Visualizations

3. Applications (NOT YET INTEGRATED)
   
   1. fastAPI: Quick apis to make data accessible to other users
   
   2. flask: To create a webpage or server using the data 

4. Extras:
   
   1. openpyxl
      
      1. For working with excel files
   
   2. notebook
      
      1. For jupyter notebooks
   
   3. sqlalchemy
      
      1. For interacting with databases
   
   4. ipython

5. Custom Utilities:
   
   1. via_utils
6. **<u>Future</u>** Integrations:
   1. pyspark

The recommended Tech Stack is the following:

1. For Data Processing:
   
   1. Pandas
   
   2. Polars
   
   3. duck_db
   
   4. ibis: To standardize all the codes API through ibis. Instead of coding directly in the  package itself, all codes can be made using ibis, thu standardizing the codes. This is less confusing for developers and therefore the resulting code is easier to read and mantain.

2. For visualizations:
   
   1. 