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

    def execute(self, query, data=None):
        try:
            if data:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully.")
        except mysql.connector.Error as err:
            print("Error executing query: ", err)

    def fetch_data(self, query, data=None):
        try:
            if data is not None:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("Error fetching data: ", err)
            return None


    def fetch_data_as_df(self, query, data=None):
        try:
            if data is not None:
                self.cursor.execute(query, data)
            else:
                self.cursor.execute(query)
            result = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            df = pd.DataFrame(result, columns=column_names)
            return df
        except mysql.connector.Error as err:
            print("Error fetching data as DataFrame: ", err)
            return None

    def commit(self):
        try:
            self.connection.commit()
            print("Changes committed successfully.")
        except mysql.connector.Error as err:
            print("Error committing changes: ", err)

    def lastrowid(self):
        try:
            return self.cursor.lastrowid
        except mysql.connector.Error as err:
            print("Error fetching last row id: ", err)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Connection closed.")