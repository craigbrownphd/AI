


def eval(root, defined_variables):
    assert root is not None


    if root.value is '!':
        return not eval(root.left, defined_variables)

    if root.value in ['|', '&']:
        if root.value is '|':
            return eval(root.left, defined_variables) or eval(root.right, defined_variables)
        elif root.value is '&':
            return eval(root.left, defined_variables) and eval(root.right, defined_variables)

    return defined_variables[root.value]

