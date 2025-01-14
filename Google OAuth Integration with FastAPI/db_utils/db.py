import mysql.connector
from mysql.connector.errors import Error
import os
from datetime import datetime
import logging as logger

host=os.getenv("DB_HOST")
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
database=os.getenv("DB_NAME")
port=os.getenv("DB_PORT")

def log_user(user_id, user_email, user_name, user_pic, first_logged_in, last_accessed):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=user, password=password)

        if connection.is_connected():
            cursor = connection.cursor()
            sql_query = """SELECT COUNT(*) from users WHERE email_id = %s"""
            cursor.execute(sql_query, (user_email,))
            row_count = cursor.fetchone()[0]

            if row_count == 0:
                sql_query = """INSERT INTO users (user_id, email_id,user_name,user_pic,first_logged_in, last_accessed) VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_query, (user_id, user_email, user_name, user_pic, first_logged_in, last_accessed))

            # Commit changes
            connection.commit()
            logger.info("Record inserted successfully")

    except Error as e:
        logger.info("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("MySQL connection is closed")

def log_token(access_token, user_email, session_id):
    try:
        connection = mysql.connector.connect(host=host, database=database, user=user, password=password)

        if connection.is_connected():
            cursor = connection.cursor()

            # SQL query to insert data
            sql_query = """INSERT INTO issued_tokens (token, email_id, session_id) VALUES (%s,%s,%s)"""
            # Execute the SQL query
            cursor.execute(sql_query, (access_token, user_email, session_id))

            # Commit changes
            connection.commit()
            logger.info("Record inserted successfully")

    except Error as e:
        logger.info("Error while connecting to MySQL", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            logger.info("MySQL connection is closed")