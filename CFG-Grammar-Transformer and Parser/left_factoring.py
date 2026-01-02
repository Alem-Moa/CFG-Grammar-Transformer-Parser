# left_factoring.py

def detect_left_factoring(grammar):
    """
    Detects non-terminals that need left factoring.
    Returns a list of non-terminals that have common prefixes.
    """
    needs_factoring = []

    for head, prods in grammar.items():
        # Remove duplicates
        prods = list(set(prods))
        prefixes = {}
        for prod in prods:
            symbols = prod.split()
            if not symbols:
                continue
            prefix = symbols[0]
            if prefix in prefixes:
                prefixes[prefix].append(prod)
            else:
                prefixes[prefix] = [prod]

        # If any prefix has more than one production, left factoring is needed
        for pref, group in prefixes.items():
            if len(group) > 1:
                needs_factoring.append(head)
                break

    return needs_factoring
