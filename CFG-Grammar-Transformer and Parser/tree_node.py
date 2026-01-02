class TreeNode:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []

def print_tree(node, indent=0, is_last=True, prefix=""):
    # This version adds visual connectors like └── and ├──
    marker = "└── " if is_last else "├── "
    print(prefix + marker + node.symbol)
    
    new_prefix = prefix + ("    " if is_last else "│   ")
    child_count = len(node.children)
    for i, child in enumerate(node.children):
        print_tree(child, indent + 1, i == child_count - 1, new_prefix)