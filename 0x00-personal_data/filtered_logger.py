#!/usr/bin/env python3
"""
REGEX-ING of logs
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Use a regex to replace occurrences of certain field values.
    Args:
        fields: The fields to obfuscate
	reduction: The string to replace the field values with.
	message: The log message
	separator: The character that separates fields in the logs
    
    Return:
        The log message obfuscated
    """
    p = '|'.join(f"{field}=[^{separator}]+" for field in fields)
    return re.sub(p, lambda m: f"{m.group().split('=')[0]}={redaction}", message)
