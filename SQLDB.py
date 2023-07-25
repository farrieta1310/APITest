import pyodbc
from GoogleSecretManager import GoogleSecretsManager
import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
import json

class SQLDB:
    def __init__(self):
        self.__db_name = GoogleSecretsManager('1000257097927').get_secret_value('db_name')
        self.__user = GoogleSecretsManager('1000257097927').get_secret_value('db_user')
        self.__password = GoogleSecretsManager('1000257097927').get_secret_value('db_password')
        self.__host = GoogleSecretsManager('1000257097927').get_secret_value('db_host')
        self.__port = GoogleSecretsManager('1000257097927').get_secret_value('db_port')
        self.connection = None

    def connect(self):
        try:
            connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={self.__host},{self.__port};DATABASE={self.__db_name};UID={self.__user};PWD={self.__password}"
            self.connection = pyodbc.connect(connection_string)
            print("Connected to the database.")
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            print("Disconnected from the database.")

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            print(f'Query executed: {query}')
            cursor.execute(query)
            cursor.commit()
            cursor.close()
            return 'Query executed succesfully'
        except pyodbc.Error as e:
            print(f"Error executing the query: {e}")
            return None
            
    def export_table_to_avro(self, table_name, avro_format ,output_file):
        try:
            #Parse the schema so we can use it to write the data            
            avro_schema = avro.schema.parse(open(avro_format).read())
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            table_data = cursor.fetchall()   
            print(table_data)      

            # Create Avro data file and write data to it
            with open(output_file, 'wb') as avro_file:
                writer = DataFileWriter(avro_file, DatumWriter(), avro_schema)
                for row in table_data:
                    department_id, department_name = row
                    writer.append({"Department_id": department_id, "Department_Name": department_name})
                writer.close()

            return 'Table exported succesfully'
        except pyodbc.Error as e:
            print(f"Error exporting table: {e}")
            return None        
        
# Example Export:
if __name__ == "__main__":
    db_sql = SQLDB()
    db_sql.connect()
    db_sql.export_table_to_avro(table_name='DEPARTMENTS', avro_format='avro_department_format.avsc' ,output_file='department_output.avro')        
    db_sql.disconnect()
