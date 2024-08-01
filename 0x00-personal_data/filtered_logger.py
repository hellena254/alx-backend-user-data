#!/usr/bin/env python3
"""
REGEX-ING of logs
"""

import re
import logging
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Use a regex to replace occurrences of certain field values.
    Args:
        fields: The fields to obfuscate
        redaction: The string to replace the field values with.
        message: The log message
        separator: The character that separates fields in the logs

    Return:
        The log message obfuscated
    """
    p = '|'.join(f"{field}=[^{separator}]+" for field in fields)
    return re.sub(p, lambda m: f"{m.group().split('=')[0]}={redaction}", message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter
        Args:
            fields: field to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, filtering specified fields.

        Args:
            record: The log record to format.

        Return:
            str: The formatted and obfuscated log record
        """
        initial_mess = super().format(record)
        return filter_datum(self.fields, self.REDACTION, initial_mess, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Creates and returns a logger with a specific configuration.
    Return:
        logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger
