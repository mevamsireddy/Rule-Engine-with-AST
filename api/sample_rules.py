from backend.ast_engine import Node

def get_sample_rule():
    # (age > 30 AND department == 'Sales')
    condition_1 = Node(type="condition", value="age > 30")
    condition_2 = Node(type="condition", value="department == 'Sales'")
    and_node_1 = Node(type="operator", left=condition_1, right=condition_2, value="AND")

    # (age < 25 AND department == 'Marketing')
    condition_3 = Node(type="condition", value="age < 25")
    condition_4 = Node(type="condition", value="department == 'Marketing'")
    and_node_2 = Node(type="operator", left=condition_3, right=condition_4, value="AND")

    # (salary > 50000 OR experience > 5)
    condition_5 = Node(type="condition", value="salary > 50000")
    condition_6 = Node(type="condition", value="experience > 5")
    or_node_1 = Node(type="operator", left=condition_5, right=condition_6, value="OR")

    # Combine everything with OR and AND
    or_node_2 = Node(type="operator", left=and_node_1, right=and_node_2, value="OR")
    root_node = Node(type="operator", left=or_node_2, right=or_node_1, value="AND")

    return root_node