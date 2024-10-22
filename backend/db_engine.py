import psycopg2
import json

def connect_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="",  # Update with your actual password 
            host="localhost",
            port="5432",
            database="rule_engine"
        )
        return connection
    except Exception as error:
        print("Error connecting to the database:", error)
        return None

def insert_rule(rule_string, ast):
    connection = connect_db()
    if connection is None:
        return False

    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO rules (rule_string, ast)
        VALUES (%s, %s) RETURNING id;
        """

        # If `ast` is already a dictionary, use it directly; otherwise, call `to_dict()`.
        if isinstance(ast, dict):
            ast_dict = ast  # Already a dictionary
        else:
            ast_dict = ast.to_dict()  # Convert Node to dictionary

        cursor.execute(query, (rule_string, json.dumps(ast_dict)))  # Serialize AST as JSON
        rule_id = cursor.fetchone()[0]

        connection.commit()
        cursor.close()
        return rule_id
    except Exception as error:
        print("Error inserting rule:", error)
        return None
    finally:
        if connection:
            connection.close()