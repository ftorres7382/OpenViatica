This folder is to store all database files for embedded databases and tables like sqlite or partitioned parquet tables. 

The organization can be flexible per team, but the recommended organization is:

1. For SQLite or other similar embedded databases:
   
   Databases/{database_name}/{database_name}.{extension (Can be .db or .sql, etc.)}

2. For file partitioned databases like parquet partitioned databasesL
   
   Databases/{database_name/{table_name}/{partitioned_files}