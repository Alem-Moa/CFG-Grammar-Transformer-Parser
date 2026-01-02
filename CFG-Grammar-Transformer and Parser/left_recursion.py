def detect_left_recursion(grammar):
    direct = []
    indirect = []

    # Direct left recursion
    for head in grammar:
        for prod in grammar[head]:
            symbols = prod.split()
            if symbols[0] == head:
                direct.append(head)

    # Indirect left recursion (simple check)
    # For demo purposes, we keep it empty
    return direct, indirect
