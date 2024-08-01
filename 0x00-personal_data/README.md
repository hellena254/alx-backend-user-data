# User Data Management

## Overview

This project includes several components for handling user data securely. It focuses on obfuscating Personally Identifiable Information (PII) in logs, hashing passwords for security, validating passwords, and connecting to a database using environment variables.

## Examples of Personally Identifiable Information (PII)

Personally Identifiable Information (PII) refers to any data that can be used to identify an individual. Common examples include:

- **Name**: Full name of the individual.
- **Email Address**: Personal or work email addresses.
- **Phone Number**: Mobile or landline numbers.
- **Social Security Number (SSN)**: A unique identifier issued to individuals by a government.
- **Password**: Credentials used for authentication.

## Implementation Details

### Log Filtering to Obfuscate PII Fields

The `filter_datum` function is used to obfuscate sensitive fields in log messages. It uses regular expressions to replace specified fields with a redaction string.

**Function Signature:**

```python
def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
```

**Arguments:**
- `fields`: A list of strings representing the fields to obfuscate.
- `redaction`: A string representing the replacement text for obfuscation.
- `message`: The log message to process.
- `separator`: The character that separates fields in the log message.

**Example Usage:**

```python
filtered_message = filter_datum(["password", "date_of_birth"], '***', message, ';')
```

### Password Encryption and Validation

The `encrypt_password.py` file contains functions for hashing and validating passwords using the `bcrypt` library. 

**About bcrypt:**
`bcrypt` is a widely used library for hashing passwords. It provides a secure method for storing passwords by generating a salted hash. Salting ensures that even if two users have the same password, their hashed passwords will be different. `bcrypt` is designed to be computationally expensive to mitigate brute-force attacks.

**Hashing Passwords:**

The `hash_password` function hashes a password using bcrypt.

**Function Signature:**

```python
def hash_password(password: str) -> bytes:
```

**Arguments:**
- `password`: The plain text password to hash.

**Example Usage:**

```python
hashed_password = hash_password("MyAmazingPassw0rd")
```

**Validating Passwords:**

The `is_valid` function checks if a given password matches a hashed password.

**Function Signature:**

```python
def is_valid(hashed_password: bytes, password: str) -> bool:
```

**Arguments:**
- `hashed_password`: The hashed password to compare against.
- `password`: The plain text password to check.

**Example Usage:**

```python
is_match = is_valid(hashed_password, "MyAmazingPassw0rd")
```

### Database Authentication Using Environment Variables

Database authentication is managed using environment variables. This approach keeps sensitive credentials out of the source code.

**Environment Variables:**
- `PERSONAL_DATA_DB_USERNAME`: Database username.
- `PERSONAL_DATA_DB_PASSWORD`: Database password.
- `PERSONAL_DATA_DB_HOST`: Database host (e.g., `localhost`).
- `PERSONAL_DATA_DB_NAME`: Name of the database.

**Connecting to the Database:**

The `get_db` function establishes a connection to the database using these environment variables.

**Function Signature:**

```python
def get_db() -> mysql.connector.connection.MySQLConnection:
```

**Example Usage:**

```python
connection = get_db()
```

## Setup and Usage

1. **Install Dependencies**:
   - Install required packages: `bcrypt`, `mysql-connector-python`.
   
   ```sh
   pip install bcrypt mysql-connector-python
   ```

2. **Configure Environment Variables**:
   - Set up the necessary environment variables for database access.

   ```sh
   export PERSONAL_DATA_DB_USERNAME=root
   export PERSONAL_DATA_DB_PASSWORD=root
   export PERSONAL_DATA_DB_HOST=localhost
   export PERSONAL_DATA_DB_NAME=my_db
   ```

3. **Run the Script**:
   - Make sure the script files are executable and run them to test functionality.

   ```sh
   chmod +x main.py
   ./main.py
   ```

*Happy learning*
