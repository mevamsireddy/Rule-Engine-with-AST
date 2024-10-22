import unittest
from backend.ast_engine import create_rule, evaluate_rule, modify_rule


class TestRuleEngine(unittest.TestCase):

    def test_create_rule(self):
        rule_string = "age > 30 AND department == 'Sales'"
        ast = create_rule(rule_string)

        self.assertIsNotNone(ast)
        self.assertEqual(ast.value, "AND")
        self.assertEqual(ast.left.value, "age > 30")
        self.assertEqual(ast.right.value, "department == 'Sales'")

    def test_evaluate_rule(self):
        rule_string = "age > 30 AND department == 'Sales'"
        ast = create_rule(rule_string)

        data = {
            'age': 31,
            'department': 'Sales'
        }
        result = evaluate_rule(ast, data)
        self.assertTrue(result)

        data['age'] = 30
        result = evaluate_rule(ast, data)
        self.assertFalse(result)

        data['department'] = 'HR'
        result = evaluate_rule(ast, data)
        self.assertFalse(result)

        data['age'] = 35
        result = evaluate_rule(ast, data)
        self.assertFalse(result)

        data['department'] = 'Sales'
        result = evaluate_rule(ast, data)
        self.assertTrue(result)

    def test_invalid_rule(self):
        rule_string = "age > 30 AND department == Sales"
        ast = create_rule(rule_string)
        self.assertIsNone(ast)

    def test_modify_rule(self):
        rule_string = "age > 30 AND department == 'Sales'"
        ast = create_rule(rule_string)
        modified_ast = modify_rule(ast, new_operator='OR')

        self.assertIsNotNone(modified_ast)
        self.assertEqual(modified_ast.value, 'OR')


if __name__ == '__main__':
    unittest.main()