import re

class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type  # "operator" or "condition"
        self.value = value  # Value for operator or condition
        self.left = left  # Left child Node
        self.right = right  # Right child Node

    def to_dict(self):
        """Converts the Node to a dictionary that can be serialized to JSON."""
        node_dict = {
            "type": self.type,
            "value": self.value,
        }

        if self.left:
            node_dict["left"] = self.left.to_dict()

        if self.right:
            node_dict["right"] = self.right.to_dict()

        return node_dict


VALID_ATTRIBUTES = {"age", "department"}
VALID_OPERATORS = {"AND", "OR", ">", "<", ">=", "<=", "==", "!="}

def validate_rule(rule_string):
    """Check if the rule string is valid."""
    if not rule_string:
        return False

    tokens = re.findall(r"(\w+|[><!=]+|'[^']+'|\bAND\b|\bOR\b)", rule_string)

    for token in tokens:
        if not (token.isdigit() or token in VALID_ATTRIBUTES or token in VALID_OPERATORS or token.startswith("'")):
            print(f"Invalid attribute or operator: {token}")
            return False
    return True


def create_rule(rule_string):
    """
    Create an AST from the given rule string.
    Example: "age > 30 AND department == 'Sales'"
    """
    rule_string = rule_string.strip()

    if not validate_rule(rule_string):
        print(f"Invalid rule string: {rule_string}")
        return None

    rule_string = re.sub(r"\s*([()<>!=]+)\s*", r" \1 ", rule_string)

    tokens = re.split(r'\s+(AND|OR)\s+', rule_string)

    def parse_tokens(tokens):
        """Parse a list of tokens (operands and operators) into an AST."""
        if not tokens:
            return None

        tokens = [token.strip() for token in tokens if token.strip()]

        precedence = {'AND': 1, 'OR': 0}
        min_precedence = float("inf")
        main_operator_index = -1

        for i, token in enumerate(tokens):
            if token in precedence:
                if precedence[token] < min_precedence:
                    min_precedence = precedence[token]
                    main_operator_index = i

        if main_operator_index == -1:
            return Node(type="condition", value=tokens[0].strip())

        left_tokens = tokens[:main_operator_index]
        right_tokens = tokens[main_operator_index + 1:]

        left = parse_tokens(left_tokens)
        operator = tokens[main_operator_index].strip()
        right = parse_tokens(right_tokens)

        return Node(type="operator", value=operator, left=left, right=right)

    return parse_tokens(tokens)


def evaluate_rule(ast, data):
    """
    Evaluate the given AST against user data.
    :param ast: The root node of the AST.
    :param data: Dictionary containing user attributes (e.g., age, department, etc.).
    :return: True if the rule is satisfied, False otherwise.
    """

    def evaluate(node, context):
        if node is None:
            return False

        if node.type == "condition":
            match = re.match(r"(\w+)\s*([!=<>]+)\s*(.+)", node.value)
            if match:
                key, operator, value = match.groups()
                value = value.strip().strip("'")

                context_value = context.get(key)
                if context_value is None:
                    return False

                # Type conversion for comparison
                if value.isdigit():
                    value = int(value)
                elif value.replace('.', '', 1).isdigit():
                    value = float(value)

                # Perform comparison
                if operator == '>':
                    return context_value > value
                elif operator == '<':
                    return context_value < value
                elif operator == '==':
                    return context_value == value
                elif operator == '!=':
                    return context_value != value

        elif node.type == "operator":
            left_result = evaluate(node.left, context)
            right_result = evaluate(node.right, context)

            if node.value.strip() == 'AND':
                return left_result and right_result
            elif node.value.strip() == 'OR':
                return left_result or right_result

        return False

    return evaluate(ast, data)


def modify_rule(ast, new_operator=None, new_value=None):
    """
    Modify an existing rule in the AST.
    :param ast: The root node of the AST.
    :param new_operator: The new operator to set.
    :param new_value: The new value to set.
    :return: The modified AST.
    """
    if ast is None:
        print("AST is None, cannot modify.")
        return None

    if ast.type == "condition":
        if new_value is not None:
            ast.value = f"{ast.value.split()[0]} {new_operator} {new_value}" if new_operator else ast.value
        else:
            ast.value = f"{ast.value.split()[0]} {new_operator} {ast.value.split()[2]}"
    else:
        if new_operator:
            ast.value = new_operator
        ast.left = modify_rule(ast.left, new_operator, new_value)
        ast.right = modify_rule(ast.right, new_operator, new_value)

    return ast