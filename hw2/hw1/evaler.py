def evaluate(root, facts):
    assert root is not None


    if root.value == '!':
        return not evaluate(root.left, facts)

    if root.value in ['|', '&']:
        if root.value == '|':
            return evaluate(root.left, facts) or evaluate(root.right, facts)
        elif root.value == '&':
            return evaluate(root.left, facts) and evaluate(root.right, facts)

    return facts[root.value]




