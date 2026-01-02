from first_follow import compute_first, compute_follow, EPSILON
from tree_node import TreeNode, print_tree

def ll1_parse(grammar, input_string):
    start_symbol = list(grammar.keys())[0]
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)
    follow[start_symbol].add("$")

    table = {}
    for head, prods in grammar.items():
        table[head] = {}
        for prod in prods:
            symbols = prod.split()
            if symbols[0] == EPSILON:
                targets = follow[head]
            elif symbols[0] in grammar:
                targets = first[symbols[0]]
                if EPSILON in targets:
                    targets = (targets - {EPSILON}) | follow[head]
            else:
                targets = {symbols[0]}
            for t in targets:
                table[head][t] = symbols

    stack = [(start_symbol, TreeNode(start_symbol))]
    root = stack[0][1]
    tokens = input_string.split() + ["$"]
    index = 0

    print("\n--- LL(1) PARSING ---")
    print(f"{'Stack':<25} {'Input':<25} Action")
    print("-"*65)

    while stack:
        symbol, node = stack.pop()
        token = tokens[index]

        if symbol not in grammar and symbol != EPSILON:
            if symbol == token:
                print(f"{symbol:<25} {token:<25} Match")
                index += 1
                continue
            else:
                print(f"{symbol:<25} {token:<25} ERROR")
                return

        if symbol == EPSILON:
            print(f"{symbol:<25} {token:<25} ε-production")
            continue

        prod = table.get(symbol, {}).get(token)
        if not prod:
            print(f"{symbol:<25} {token:<25} ERROR (no table entry)")
            return

        print(f"{symbol:<25} {token:<25} Expand -> {' '.join(prod)}")
        children = [TreeNode(s) for s in prod]
        node.children.extend(children)
        for s, c in reversed(list(zip(prod, children))):
            stack.append((s, c))

    print("\n--- PARSE TREE ---")
    print_tree(root)
    print("\n✔ Success — input accepted!")
