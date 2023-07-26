# API Data Test
This is an API built in python that supports 3 kinds of files and insert them to a SQL Database

The files supported by the API are:

- Jobs
This file needs to have 2 columns: Id (integer) and Name of the Job (String)

- Departments
This file needs to have 2 columns Id (Integer) and Department (String)
  
- Hired Employees
This file needs to have 5 columns Id (Integer), Name (String), DateTime (String), Department_Id (int) and Jobs_Id (int)

The API will look at the file name to determine which file we're processing. Examples of valid file names: jobs_20230725.csv, new_departments.csv, latest_employees_20230725.csv. As long as the file name has one of the keywords: jobs, departments or employees, the API will process the files.

The API will double check that the files have the correct number of columns and datatypes before attemption to insert into the Database.

This API is connected to SQL Server DB hosted in GCP. The user, password, Database and port are handle using Google's SecretManager Service.

Examples of how to call the API for each file:
curl -X POST -F "file=@C:\Users\ferna\Desktop\PruebaData\jobs.csv"   http://127.0.0.1:5000/upload

curl -X POST -F "file=@C:\Users\ferna\Desktop\PruebaData\departments.csv"   http://127.0.0.1:5000/upload

curl -X POST -F "file=@C:\Users\ferna\Desktop\PruebaData\hired_employees.csv"   http://127.0.0.1:5000/upload

The class called: SQLDB handles the operations related to Database. Apart from the connect, disconnect and execute operations, this calls also provides support to backup the tables into an AVRO file, and also restore the tables using those same AVRO files.

Here's an example of how to use the backup/restore functionality:

if __name__ == "__main__":
    db_sql = SQLDB()
    db_sql.connect()
    db_sql.export_department_table_to_avro(table_name='DEPARTMENTS', avro_format='avro_department_format.avsc' ,output_file='department_output.avro')        
    db_sql.insert_department_from_avro(avro_file='department_output.avro')
    db_sql.export_jobs_table_to_avro(table_name='JOBS', avro_format='avro_jobs_format.avsc' ,output_file='jobs_output.avro')
    db_sql.insert_job_from_avro(avro_file='jobs_output.avro')
    db_sql.export_hired_employees_table_to_avro(table_name='HIRED_EMPLOYEES', avro_format='avro_hired_employees_format.avsc' ,output_file='employees_output.avro')
    db_sql.insert_employees_from_avro(avro_file='employees_output.avro')    
    db_sql.disconnect()
