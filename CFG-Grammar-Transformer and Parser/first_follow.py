EPSILON = "ε"

def compute_first(grammar):
    first = {nt: set() for nt in grammar}
    changed = True
    while changed:
        changed = False
        for head, productions in grammar.items():
            for prod in productions:
                symbols = prod.split()
                if not symbols or symbols[0] == EPSILON:
                    if EPSILON not in first[head]:
                        first[head].add(EPSILON)
                        changed = True
                    continue
                for sym in symbols:
                    if sym not in grammar: # Terminal
                        if sym not in first[head]:
                            first[head].add(sym)
                            changed = True
                        break
                    before = len(first[head])
                    first[head] |= (first[sym] - {EPSILON})
                    if (len(first[head]) > before): changed = True
                    if EPSILON not in first[sym]: break
                else:
                    if EPSILON not in first[head]:
                        first[head].add(EPSILON)
                        changed = True
    return first

def compute_follow(grammar, first):
    follow = {nt: set() for nt in grammar}
    start = list(grammar.keys())[0]
    follow[start].add("$")
    changed = True
    while changed:
        changed = False
        for head, productions in grammar.items():
            for prod in productions:
                symbols = prod.split()
                for i, B in enumerate(symbols):
                    if B in grammar:
                        if i + 1 < len(symbols):
                            beta = symbols[i+1]
                            if beta not in grammar: # terminal
                                if beta not in follow[B]:
                                    follow[B].add(beta)
                                    changed = True
                            else: # non-terminal
                                before = len(follow[B])
                                follow[B] |= (first[beta] - {EPSILON})
                                if len(follow[B]) > before: changed = True
                                if EPSILON in first[beta]:
                                    before = len(follow[B])
                                    follow[B] |= follow[head]
                                    if len(follow[B]) > before: changed = True
                        else:
                            before = len(follow[B])
                            follow[B] |= follow[head]
                            if len(follow[B]) > before: changed = True
    return follow

def display_sets(first, follow):
    print("\n--- FIRST AND FOLLOW SETS ---")
    print(f"{'Non-Terminal':<15} {'FIRST':<20} {'FOLLOW':<20}")
    for nt in first:
        f_str = "{" + ", ".join(first[nt]) + "}"
        fl_str = "{" + ", ".join(follow[nt]) + "}"
        print(f"{nt:<15} {f_str:<20} {fl_str:<20}")