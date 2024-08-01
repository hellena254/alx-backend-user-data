#!/usr/bin/env python3
"""
Module for filtering and displaying user data from the database.
"""

import os
import mysql.connector
from mysql.connector import Error
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='[HOLBERTON] user_data INFO %(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S,%f')

def get_db():
    """
    Establishes and returns a connection to the database.
    
    Returns:
        mysql.connector.connection.MySQLConnection: The database connection.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
            user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
            password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
            database=os.getenv('PERSONAL_DATA_DB_NAME', 'my_db')
        )
        return connection
    except Error as e:
        logging.error(f"Error: {e}")
        raise

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.
    
    Args:
        fields (List[str]): The fields to obfuscate.
        redaction (str): The string to replace the field values with.
        message (str): The log message.
        separator (str): The character that separates fields in the log message.
    
    Returns:
        str: The obfuscated log message.
    """
    pattern = '|'.join(f"{field}=[^{separator}]+" for field in fields)
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}", message)

def main():
    """
    Retrieves data from the users table and displays each row with specified fields obfuscated.
    """
    fields_to_obfuscate = ["name", "email", "phone", "ssn", "password"]
    
    try:
        connection = get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users;")
        rows = cursor.fetchall()
        
        for row in rows:
            message = "; ".join(f"{key}={value}" for key, value in row.items()) + ";"
            filtered_message = filter_datum(fields_to_obfuscate, '***', message, ';')
            logging.info(filtered_message)
            
    except Error as e:
        logging.error(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()
