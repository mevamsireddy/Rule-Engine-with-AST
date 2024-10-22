# Rule-Engine-with-AST

## Project Overview
The Rule Engine AST is an application that allows users to create, evaluate, and modify rules based on an Abstract Syntax Tree (AST) structure. The project is designed to handle rule logic processing and store the rules in a PostgreSQL database. The backend logic for parsing rules and evaluating conditions is implemented in Python, while PostgreSQL is used for persistent storage.

## Project Structure
```bash
rule-engine-ast/
├── .venv                       # Virtual environment (optional)
├── api/
│   └── sample_rules.py         # API layer to expose rule engine operations 
├── backend/
│   ├── ast_engine.py           # Backend logic for building and evaluating AST
│   └── db_engine.py            # Database operations for inserting rules
├── tests/
│   └── test_ast_engine.py      # Unit tests for the AST and rules
├── app.py                      # Entry point for the application
├── venv/                       # Python virtual environment
└── requirements.txt            # Dependencies file
```

## Prerequisites
### System Requirements
- **Operating System:** Windows 11 (Used for development)
- **Python:** Version 3.10 (or compatible)
- **PostgreSQL:** Version 17.0-1 (or compatible)

### Python Dependencies
All Python dependencies are listed in the requirements.txt file. You can install them using pip.
```bash
pip install -r requirements.txt
```
- psycopg2: PostgreSQL database adapter
- unittest: Python's built-in testing framework (used for testing)
- re: Regular expression library (used for rule parsing)

## Setting Up the Project
### Step 1: Clone the Repository
```bash
git clone <your-github-repository-url>
cd rule-engine-ast
```

### Step 2: Setting Up Virtual Environment
Create a virtual environment to manage project dependencies:
```bash
# Create virtual environment
python -m venv .venv

# Activate the virtual environment On Windows
.\.venv\Scripts\activate

# Install the project dependencies
pip install -r requirements.txt
```

### Step 3: Install PostgreSQL

Install PostgreSQL version 17.0-1 or compatible version for Windows:
1. Download PostgreSQL for Windows
2. Follow the installation guide and set up a PostgreSQL server.
3. Once PostgreSQL is installed:
```bash
# Start the PostgreSQL service (you can do this via the Windows Services manager)
```

### Step 4: Set Up PostgreSQL Database
Create a database and schema for the project.
#### Create Database
Open pgAdmin or use the PostgreSQL CLI to create a database.
``` bash
CREATE DATABASE rule_engine_db;
```

#### Create Tables
Once the database is created, create the required tables using the schema provided below:
```bash
-- Create rules table
CREATE TABLE rules (
    id SERIAL PRIMARY KEY,
    rule_string TEXT NOT NULL,
    ast JSONB NOT NULL
);

-- Create metadata table
CREATE TABLE metadata (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) NOT NULL,
    value TEXT NOT NULL
);
```

## Configuration
### Step 1: Update Database Configuration
Ensure that the application can connect to your PostgreSQL instance. The default configuration for the database connection is set in the backend/db_engine.py file. Adjust the connection parameters as per your PostgreSQL setup:
```bash
DATABASE = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',  # Change if using a different user
    'password': 'yourpassword',  # Change to the PostgreSQL password you set
    'dbname': 'rule_engine_db'
}
```

## Running the Application
Once the database and environment are set up, you can run the application.
```bash
# Run the app
python app.py
```
### Sample Output
```bash
PS \rule-engine-ast> python app.py
Rule inserted with ID: 14
Rule evaluation result: True
```

## Running Tests
Unit tests are provided in the tests/ folder. To run the tests:
```bash
# Run the tests
python -m unittest discover -s tests
```
### Sample Output
``` bash
PS \rule-engine-ast> python -m unittest discover -s tests

----------------------------------------------------------------------
Ran 4 tests in 0.002s

OK
```

## Design Choices
1. Abstract Syntax Tree (AST)
- The rule engine is built using an AST, where each rule is parsed into a tree structure with operators (AND, OR) acting as internal nodes, and conditions (e.g., age > 30) as leaf nodes. This structure allows the flexible combination of rules and easy evaluation against user data.
- Parsing Rules: The input rule string is tokenized, and the precedence of operators (AND, OR) is respected.
- AST Nodes: Each node in the AST represents either a condition or an operator.

2. Error Handling
- The create_rule function has been extended to handle invalid rule strings, such as missing operators or improper syntax. It logs errors if the rule string is invalid and prevents malformed rules from being inserted into the AST or database.

3. Database Integration
- The rules and their AST representations are stored in a PostgreSQL database. The use of JSONB for the AST storage allows for efficient storage and retrieval of tree-structured data.

4. Tests
- Unit tests were written using Python's unittest module. These cover:
-- Rule creation and validation.
-- Rule evaluation against user data.
-- Database insertion and retrieval.

## API (Optional)
The api/sample_rules.py script provides a basic Flask API to expose some rule engine operations. You can extend this for integration into a larger system.
```bash
# Run the Flask API
python api/sample_rules.py
```

## Dependencies
- Python: Version 3.10
- PostgreSQL: Version 17.0-1
- psycopg2: PostgreSQL database adapter
- unittest: For running unit tests
- re: Regular expression library (for rule parsing)

## Future Improvements
1. Rule Modification: Additional functionalities to modify existing rules dynamically.
2. User-Defined Functions: Future versions may support custom functions to handle advanced conditions.
3. Containerization: Docker or Podman containers could be used to improve portability and ease of deployment.


This README ensures the user can set up the project and run it locally, and it provides a comprehensive guide to the design decisions made during development.