__author__ = 'himanshu'




class Node(object):
    """
    If value is not [! & |] then it is a leaf.
    """
    def __init__(self, left, value, right):
        assert isinstance(left, Node) or left is None
        assert isinstance(right, Node) or right is None
        # assert isinstance(value, str) and len(value) is 1

        if value not in ['!', '&', '|']:
            assert left is None
            assert right is None

        if value is '!':
            """
            for !, our convention is to make left the notted value. right is None
            """
            assert left is not None and right is None
        elif value in ['&', '|']:
            assert left is not None and right is not None



        self.left = left
        self.right = right
        self.value = value


        #todo: there are requirements for what characters are allowed. a-z, A-Z, underscores,...


    def __eq__(self, other):
        assert isinstance(other, Node)

        if other is None:
            return False

        # by memory address
        if other is self:
            return True

        return self.left == other.left and \
               self.right == other.right and \
               self.value == other.value


