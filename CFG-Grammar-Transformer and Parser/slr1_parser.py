from tree_node import TreeNode, print_tree
from collections import defaultdict

EPSILON = "ε"

class Item:
    def __init__(self, head, body, dot=0):
        self.head = head
        self.body = body
        self.dot = dot

    def next_symbol(self):
        if self.dot < len(self.body):
            return self.body[self.dot]
        return None

    def __eq__(self, other):
        return self.head == other.head and self.body == other.body and self.dot == other.dot

    def __hash__(self):
        return hash((self.head, tuple(self.body), self.dot))

    def __repr__(self):
        b = list(self.body)
        b.insert(self.dot, "•")
        return f"{self.head} -> {' '.join(b)}"

def closure(items, grammar):
    closure_set = set(items)
    changed = True
    while changed:
        changed = False
        new_items = set()
        for item in closure_set:
            sym = item.next_symbol()
            if sym in grammar:
                for prod in grammar[sym]:
                    prod_body = [] if prod == EPSILON else prod.split()
                    new_item = Item(sym, prod_body)
                    if new_item not in closure_set:
                        new_items.add(new_item)
        if new_items:
            closure_set |= new_items
            changed = True
    return closure_set

def goto(items, symbol, grammar):
    moved = set()
    for item in items:
        if item.next_symbol() == symbol:
            moved.add(Item(item.head, item.body, item.dot + 1))
    return closure(moved, grammar)

def build_canonical_collection(grammar, start_symbol):
    augmented_head = start_symbol + "'"
    start_item = Item(augmented_head, [start_symbol])
    # Don't modify the original grammar directly to avoid side effects
    temp_grammar = grammar.copy()
    temp_grammar[augmented_head] = [start_symbol]
    
    C = [closure({start_item}, temp_grammar)]
    added = True
    while added:
        added = False
        for I in list(C):
            symbols = set(i.next_symbol() for i in I if i.next_symbol())
            for X in symbols:
                J = goto(I, X, temp_grammar)
                if J and J not in C:
                    C.append(J)
                    added = True
    return C

def build_slr_tables(states, grammar, follow):
    ACTION = defaultdict(dict)
    GOTO = defaultdict(dict)
    
    for i, I in enumerate(states):
        for item in I:
            a = item.next_symbol()
            if a is None:
                if item.head.endswith("'"):
                    ACTION[i]["$"] = "acc"
                else:
                    for t in follow.get(item.head, []):
                        ACTION[i][t] = ("r", (item.head, item.body))
            elif a in grammar:
                for j, J in enumerate(states):
                    if goto(I, a, grammar) == J:
                        GOTO[i][a] = j
            else:
                for j, J in enumerate(states):
                    if goto(I, a, grammar) == J:
                        ACTION[i][a] = ("s", j)
    return ACTION, GOTO

def slr1_parse(input_string, grammar):
    from first_follow import compute_first, compute_follow
    
    first = compute_first(grammar)
    follow = compute_follow(grammar, first)
    start_symbol = list(grammar.keys())[0]
    
    states = build_canonical_collection(grammar, start_symbol)
    ACTION, GOTO = build_slr_tables(states, grammar, follow)

    stack = [0]
    display_stack = ["$"] # Matches the format of your PPT image [cite: 10, 22]
    node_stack = []

    tokens = input_string.split() + ["$"]
    index = 0

    print("\n--- SLR(1) PARSING ---")
    print(f"{'Stack':<25} | {'Input':<25} | Action")
    print("-" * 75)

    while True:
        state = stack[-1]
        token = tokens[index]
        action = ACTION.get(state, {}).get(token)

        stack_str = ' '.join(display_stack)
        input_str = ' '.join(tokens[index:])
        
        # Formatting action for human-readable output as per PPT [cite: 41, 64]
        action_desc = "None"
        if action == "acc":
            action_desc = "accept"
        elif action:
            if action[0] == "s":
                action_desc = "shift"
            else:
                action_desc = f"reduce {action[1][0]} -> {' '.join(action[1][1])}"

        print(f"{stack_str:<25} | {input_str:<25} | {action_desc}")

        if not action:
            print("❌ ERROR: String rejected. No transition for current state/token.")
            return

        if action == "acc":
            print("\n✔ Success — input accepted! [cite: 75]")
            print("\n--- PARSE TREE ---")
            if node_stack:
                print_tree(node_stack[0])
            return

        if action[0] == "s":
            stack.append(action[1])
            display_stack.append(token)
            node_stack.append(TreeNode(token))
            index += 1
            
        elif action[0] == "r":
            head, body = action[1]
            new_node = TreeNode(head)
            
            num_to_pop = len(body)
            if num_to_pop > 0:
                # Handle popping for both state and display stacks
                stack = stack[:-num_to_pop]
                display_stack = display_stack[:-num_to_pop]
                
                # Handle parse tree children
                children = node_stack[-num_to_pop:]
                node_stack = node_stack[:-num_to_pop]
                new_node.children.extend(children)
            else:
                new_node.children.append(TreeNode(EPSILON))

            node_stack.append(new_node)
            display_stack.append(head) # Push reduced non-terminal
            
            # GOTO logic
            top_state = stack[-1]
            goto_state = GOTO.get(top_state, {}).get(head)
            if goto_state is None:
                print("❌ ERROR: GOTO state not found.")
                return
            stack.append(goto_state)