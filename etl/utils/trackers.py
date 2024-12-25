import re

def isolate_transformer_logic(text):
    pattern = r"### start(.*?)### end"
    matches = re.findall(pattern, text, re.DOTALL)
    code_lines = []
    for match in matches:
        lines = match.strip().split('\n')
        code_lines.extend([line.strip() for line in lines])
    return code_lines

def split_node_and_label(code_lines: list):
    pattern = r"df\['(\w+)'\]\s*=\s*(.+)"
    for line in code_lines:
        matches = re.findall(pattern, line)
        yield matches[0][0], matches[0][1]

def get_parents(label: str):
    pattern = r"df\['(\w+)'\]"
    matches = re.findall(pattern, label)
    return list(set(matches))

def generate_nodes(code_lines: list):
    nodes = []
    for node, label in split_node_and_label(code_lines):
        nodes.append({
            'node': node,
            'label': label.replace('"', '').replace("'", ''),
            'parents': get_parents(label)
        })
    return nodes