import pyodbc

class SQLDB:
    def __init__(self, db_name, user, password, host, port=1433):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None

    def connect(self):
        try:
            connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={self.host},{self.port};DATABASE={self.db_name};UID={self.user};PWD={self.password}"
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
            if self.connection is None:
                self.connect()

            cursor = self.connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except pyodbc.Error as e:
            print(f"Error executing the query: {e}")
            return None
