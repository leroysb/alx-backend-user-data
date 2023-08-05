#!/usr/bin/env python3
""" Regex-ing """
import os
import re
from typing import List
import logging
import mysql.connector


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(field + "=.*?" + separator,
                         field + "=" + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum
        Args:
            record (logging.LogRecord): Record to be formatted
        Returns:
            str: Formatted log record.
        """
        message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            message,
            self.SEPARATOR
        )


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """ returns a logging.Logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a connector to the database
    """
    config = {
        'username': os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        'password': os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        'host': os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        'database': os.getenv('PERSONAL_DATA_DB_NAME'),
    }

    cnx = mysql.connector.connect(**config)
    return cnx


def main():
    """ obtains a database connection using get_db and retrieves all rows
        in the users table and display each row under a filtered format
    """
    conn = get_db()
    if not conn:
        print("Error: Unable to connect to the database.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    logger = get_logger()
    for user in users:
        log_message = "; ".join(f"{field}={value}" for field, value in zip(cursor.column_names, user))
        logger.info(log_message)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
