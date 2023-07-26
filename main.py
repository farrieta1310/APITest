import csv
from flask import Flask, request, jsonify
from FileVerifier import FileVerifier
from SQLDB import SQLDB
import re
import pandas as pd

#Flask constructor
app = Flask(__name__)

#The route that the application should call the associated function
@app.route('/upload', methods=['POST'])

#Function to Upload File through API
def upload_file():
  try:
    #read csv file
    file = request.files['file']
    #get file name to know which structure verify to execture
    filename = file.filename
    
    verified_file = FileVerifier(file)
    
    #Check the file name on the POST request to know which verify needs to be executed
    if 'jobs' in filename:
      if verified_file.verify_jobs() == False:
        return jsonify({"error":"File does not have the correct structure"}),400
      
      data = verified_file.get_df()

      for index,row in data.iterrows():
        job = row[0]
        name = row[1]
        db_sql = SQLDB()
        db_sql.connect()        
        db_sql.execute_query(f"EXEC dbo.ADD_JOBS @job_id ={job},@job_name='{name}'") 
        db_sql.disconnect()     

    elif 'departments' in filename:
      if verified_file.verify_departments() == False:
        return jsonify({"error":"File does not have the correct structure"}),400
      
      data = verified_file.get_df()

      for index,row in data.iterrows():
        department_id = row[0]
        department = row[1]
        db_sql = SQLDB()
        db_sql.connect()        
        db_sql.execute_query(f"EXEC dbo.ADD_DEPARTMENTS @department_id ={department_id},@department='{department}'") 
        db_sql.disconnect()        

    elif 'employees' in filename:
      if verified_file.verify_hired_employees() == False:
        return jsonify({"error":"File does not have the correct structure"}),400  

      data = verified_file.get_df()

      for index,row in data.iterrows():
        id = row[0] if not pd.isna(row[0]) else None
        name = row[1] if not pd.isna(row[1]) else None
        hire_date = row[2] if not pd.isna(row[2]) else None
        department_id = row[3] if not pd.isna(row[3]) else None
        job_id = row[4] if not pd.isna(row[4]) else None
        db_sql = SQLDB()
        db_sql.connect()        
        db_sql.execute_query(f"EXEC dbo.ADD_HIRED_EMPLOYEES @id={id},@name='{name}',@hire_date='{hire_date}',@department_id='{department_id}',@job_id='{job_id}'") 
        db_sql.disconnect()     

    else:
      #In this case the file is not loaded as we can't tell the kind of file it's
      return jsonify({"error":"Invalid file"}),400

    return jsonify({"message":'read file'}),201
  except Exception as e:
    return jsonify({"error":str(e)}),500

if __name__ == '__main__':
  app.run()
