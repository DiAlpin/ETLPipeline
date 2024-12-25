import pytest
import re
from etl.utils.trackers import (
    isolate_transformer_logic,
    split_node_and_label,
    get_parents,
    generate_nodes
)

class TestTextParsingFunctions:
    def test_isolate_transformer_logic(self):
        """
        Test the isolate_transformer_logic function
        """
        # Test case with multiple code blocks
        text = """
        Some random text
        ### start
        df['col1'] = some_function()
        df['col2'] = another_function()
        ### end
        More random text
        ### start
        df['col3'] = third_function()
        ### end
        """
        
        # Expected result
        expected_lines = [
            "df['col1'] = some_function()",
            "df['col2'] = another_function()",
            "df['col3'] = third_function()"
        ]
        
        # Run the function
        result = isolate_transformer_logic(text)
        
        # Assertions
        assert len(result) == 3, "Should extract all code lines"
        assert set(result) == set(expected_lines), "Should match expected lines"
    
    def test_isolate_transformer_logic_no_matches(self):
        """
        Test isolate_transformer_logic with no matches
        """
        text = "No code blocks here"
        result = isolate_transformer_logic(text)
        assert result == [], "Should return empty list when no matches found"
    
    def test_split_node_and_label(self):
        """
        Test the split_node_and_label function
        """
        # Test inputs
        code_lines = [
            "df['age'] = df['age'] * 2",
            "df['income'] = df['salary'] + df['bonus']"
        ]
        
        # Convert generator to list for easier assertion
        result = list(split_node_and_label(code_lines))
        
        # Expected results
        expected = [
            ('age', "df['age'] * 2"),
            ('income', "df['salary'] + df['bonus']")
        ]
        
        assert result == expected, "Should correctly split nodes and labels"
    
    def test_get_parents(self):
        """
        Test the get_parents function
        """
        # Test cases
        test_cases = [
            ("df['age'] * 2", ['age']),
            ("df['salary'] + df['bonus']", ['salary', 'bonus']),
            ("some_function(df['col1'], df['col2'])", ['col1', 'col2']),
            ("42", [])
        ]
        
        for label, expected_parents in test_cases:
            result = get_parents(label)
            assert set(result) == set(expected_parents), f"Failed for label: {label}"
    
    def test_generate_nodes(self):
        """
        Test the generate_nodes function
        """
        # Test input
        code_lines = [
            "df['age'] = df['age'] * 2",
            "df['income'] = df['salary'] + df['bonus']"
        ]
        
        # Expected result
        expected_nodes = [
            {
                'node': 'age',
                'label': 'df[age] * 2',
                'parents': ['age']
            },
            {
                'node': 'income',
                'label': 'df[salary] + df[bonus]',
                'parents': ['salary', 'bonus']
            }
        ]
        
        # Run the function
        result = generate_nodes(code_lines)
        
        # Compare results
        assert len(result) == len(expected_nodes), "Should generate correct number of nodes"
        
        # Compare each node
        for res, exp in zip(result, expected_nodes):
            assert res['node'] == exp['node'], "Node names should match"
            assert res['label'] == exp['label'], "Labels should match"
            assert set(res['parents']) == set(exp['parents']), "Parents should match"
    
    def test_generate_nodes_complex_scenario(self):
        """
        Test generate_nodes with a more complex scenario
        """
        # Test input with multiple column references and quotes
        code_lines = [
            "df['total_income'] = df['salary'] + df['bonus'] + df['other_income']",
            "df['tax'] = df['total_income'] * 0.2"
        ]
        
        # Expected result
        expected_nodes = [
            {
                'node': 'total_income',
                'label': 'df[salary] + df[bonus] + df[other_income]',
                'parents': ['salary', 'bonus', 'other_income']
            },
            {
                'node': 'tax',
                'label': 'df[total_income] * 0.2',
                'parents': ['total_income']
            }
        ]
        
        # Run the function
        result = generate_nodes(code_lines)
        
        # Compare results
        assert len(result) == len(expected_nodes), "Should generate correct number of nodes"
        
        # Compare each node
        for res, exp in zip(result, expected_nodes):
            assert res['node'] == exp['node'], "Node names should match"
            assert res['label'] == exp['label'], "Labels should match"
            assert set(res['parents']) == set(exp['parents']), "Parents should match"