from backend.ast_engine import create_rule, evaluate_rule
from backend.db_engine import insert_rule
from api.sample_rules import get_sample_rule

def main():
    # Example usage
    rule_string = "age > 30 AND department == 'Sales'"
    
    # Create an AST from the rule string
    ast = create_rule(rule_string)
    if ast is None:
        print("Failed to create AST.")
        return

    # Insert the rule into the database
    rule_id = insert_rule(rule_string, ast)
    if rule_id is None:
        print("Failed to insert rule into the database.")
        return
    print(f"Rule inserted with ID: {rule_id}")

    # Evaluate the rule with some sample data
    sample_data = {
        'age': 35,
        'department': 'Sales'
    }
    result = evaluate_rule(ast, sample_data)
    print(f"Rule evaluation result: {result}")

if __name__ == "__main__":
    main()