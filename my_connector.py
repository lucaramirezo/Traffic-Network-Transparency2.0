import mysql.connector
import pandas as pd

class MySQLConnector:
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to MySQL database.")
        except mysql.connector.Error as err:
            print("Error: ", err)

    def execute_query(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully.")
        except mysql.connector.Error as err:
            print("Error: ", err)

    def fetch_data(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_data_as_df(self, query):
        # Ejecutar la consulta
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        # Obtener los nombres de las columnas de los resultados
        column_names = [desc[0] for desc in self.cursor.description]

        # Convertir los resultados en un DataFrame de Pandas
        df = pd.DataFrame(result, columns=column_names)
        return df

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Connection closed.")
