import pyodbc
from GoogleSecretManager import GoogleSecretsManager

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
