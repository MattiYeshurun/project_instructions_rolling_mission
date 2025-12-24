import os
import mysql.connector
from mysql.connector import Error

class DatabaseService:

    def __init__(self):
        self.connect_db = None
        self.cursor = self.connect_to_db()

    def connect_to_db(self):
        try:
            self.connect_db = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME")
                )
            cursor = self.connect_db.cursor()
            return cursor
        except Error as e:
            print("Error from connection: ", e)

    def get_connection(self):
        return mysql.connector.connect(self.connect_db)


cur = DatabaseService()
cur.connect_db
cur.cursor

class Contact:
    def __init__(self, first_name, last_name, phone_number):
        self.id = None
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def contact_to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number
        }

    def create_contact(self, contact_data: dict, cursor, connection):
        connection = self.get_connection()
        cursor = self.connection.cursor()
        query = "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)"
        values = (contact_data['first_name'], contact_data['last_name'], contact_data['phone_number'])
        cursor.execute(query, values)
        connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return new_id 

    def get_all_contacts(self, cursor, connection):
        connection = self.get_connection()
        cursor = self.connection.cursor()
        query = "SELECT * FROM contacts"
        cursor.execute(query)
        connection.commit()
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return [Contact(**row) for row in rows]


    def update_contact(self, contact_id: int, contact_data: dict):
        connection = self.get_connection()
        cursor = self.connection.cursor()
        query = "UPDATE contacts SET first_name=%s, last_name=%s, phone_number=%s WHERE id=%s"
        values = (contact_data['first_name'], contact_data['last_name'], contact_data['phone_number'], contact_id)
        cursor.execute(query, values)
        connection.commit()
        success = cursor.rowcount > 0
        cursor.close()
        connection.close()
        return success


    def delete_contact(self, contact_id: int):
        connection = self.get_connection()
        cursor = self.connection.cursor()
        query = "DELETE FROM contacts WHERE id = %s"
        cursor.execute(query, (contact_id,))
        connection.commit()
        success = cursor.rowcount > 0
        cursor.close()
        connection.close()
        return success




