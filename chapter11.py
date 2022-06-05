class TreeNode:

    def __init__(self, key):
        self.key = key

        # initialize size of subtree starting at node to 1 (since the subtree
        # just contains one node)
        self.size = 1
        self.parent = None
        self.left_child = None
        self.right_child = None

    def __str__(self):
        return str(self.key)


class BST:

    def __init__(self):
        self.root = None
        self.len = 0

    def search(self, key):
        """Given a key returns an object containing that key"""
        return self._recursive_search(key, self.root)

    def _recursive_search(self, key, current_node):

        if current_node is None or key == current_node.key:
            return current_node

        elif key < current_node.key:
            return self._recursive_search(key, current_node.left_child)

        else:
            return self._recursive_search(key, current_node.right_child)

    def min(self):
        """Returns object in tree with minimum key"""
        return self._recursive_min(self.root)

    def _recursive_min(self, current_node):
        # as long as the node has a left child keep on going through
        # left child nodes
        if current_node.left_child is None:
            return current_node
        else:
            return self._recursive_min(current_node.left_child)

    def max(self):
        """Returns object in tree with maximum key"""
        return self._recursive_max(self.root)

    def _recursive_max(self, current_node):
        # as long as the node has a right child keep on going through
        # right child nodes
        if current_node.right_child is None:
            return current_node
        else:
            return self._recursive_max(current_node.right_child)

    def output_sorted(self):
        """Returns a sorted array representing the tree"""
        return self._recursive_output(self.root, [])

    def _recursive_output(self, current_node, node_list):

        if current_node is None:
            return

        self._recursive_output(current_node.left_child, node_list)
        node_list.append(current_node)
        self._recursive_output(current_node.right_child, node_list)

        return node_list

    def insert_key(self, key):
        """Insert a new key into the tree"""
        self.len += 1

        # initialize a node with that key
        key_obj = TreeNode(key)

        # if the root node hasn't yet been set, set it
        if self.root is None:
            self.root = key_obj
        else:
            self.insert(key_obj, self.root)

    def insert(self, obj_to_insert, current_node):

        # increment size of each node we traverse
        current_node.size += 1

        # search for null pointer where obj should go,
        # and insert it once none is found
        if obj_to_insert.key < current_node.key:
            if current_node.left_child is None:
                obj_to_insert.parent = current_node
                current_node.left_child = obj_to_insert
            else:
                self.insert(obj_to_insert, current_node.left_child)

        else:
            if current_node.right_child is None:
                obj_to_insert.parent = current_node
                current_node.right_child = obj_to_insert
            else:
                self.insert(obj_to_insert, current_node.right_child)

    def select(self, i, current_node=None):
        """Returns the ith smallest element in the tree"""
        if current_node is None:
            current_node = self.root

        # set j to be the size of the current node's left subtree
        if current_node.left_child is not None:
            j = current_node.left_child.size
        else:
            j = 0

        # if i is 1 more than j, then we are at the ith smallest node
        if i == j + 1:
            return current_node
        # if i is less than j + 1, recurse on left subtree
        elif i < j + 1:
            return self.select(i, current_node.left_child)
        # if i is greater than j + 1, recurse on right subtree
        else:  # i > j + 1
            return self.select(i-j-1, current_node.right_child)

    def delete(self, key_to_delete):
        """INCOMPLETE. I was spending too much time fiddling with pointers and edge cases
        without gaining any deeper understanding, so I decided to stop wasting my time.
        As of not BST does not support a delete operation."""
        node_to_delete = self.search(key_to_delete)
        if node_to_delete is None:
            raise AttributeError("Node not in tree")

        self.delete_node(node_to_delete)

    def delete_node(self, node_to_delete):
        # if node has no children we can simply delete it by making its parent's
        # appropriate child pointer None

        if node_to_delete.right_child is None and node_to_delete.left_child is None:
            # special case if root node is only node in tree
            if node_to_delete == self.root:
                self.root = None
                return

            # set parent pointer based on whether node to delete is
            # itself a left or right child
            if node_to_delete.key < node_to_delete.parent.key:
                node_to_delete.parent_node.left_child = None
            else:
                node_to_delete.parent_node.right_child = None

        # if node only has a left child we can splice it out
        elif node_to_delete.right_child is None:
            # special case if we are deleting root node
            if node_to_delete == self.root:
                self.root = node_to_delete.left_child
                return

            # if node_to_delete is itself a left child
            if node_to_delete.key < node_to_delete.parent.key:
                node_to_delete.parent.left_child = node_to_delete.left_child
            else:  # node_to_delete is itself a right child
                node_to_delete.parent.right_child = node_to_delete.left_child

        # similar if node only has a right child
        elif node_to_delete.left_child is None:
            # special case if we are deleting root node
            if node_to_delete == self.root:
                self.root = node_to_delete.right_child
                return

            # if node_to_delete is itself a left child
            if node_to_delete.key < node_to_delete.parent.key:
                node_to_delete.parent.left_child = node_to_delete.right_child
            else:   # node_to_delete is itself a right child
                node_to_delete.parent.right_child = node_to_delete.right_child

        # else node has two children
        else:
            # find the predecessor of node to delete which must be the
            # max node in its left subtree (which must exist)
            predecessor_node = self._recursive_max(node_to_delete.left_child)

            # swap parent_nodes
            if node_to_delete == self.root:
                pass
            elif node_to_delete.key < node_to_delete.parent.key:
                node_to_delete.parent.left_child = predecessor_node
            else:
                node_to_delete.parent.right_child = predecessor_node

            # swap left children
            predecessor_node.left_child, node_to_delete.left_child = \
                node_to_delete.left_child, predecessor_node.left_child

            # swap right children
            predecessor_node.right_child = node_to_delete.right_child
            node_to_delete.right_child = None

            # node to delete now either has no left child or no children,
            # so we call delete again, and it will get caught by the no
            # child or one child case
            self.delete_node(node_to_delete)


def bst_median_maintenance_sum(array):
    """Returns the sum of the kth medians of an array O(log n) runtime"""
    total = 0
    tree = BST()
    # insert each value into the tree and call select on k//2+1 (0 indexed)
    # element, note that this will return the (k/2)th smallest (1 indexed) if k
    # is even or the ((k+1)/2)th smallest (1 indexed) if k is odd
    for k, value in enumerate(array):
        tree.insert_key(value)
        median = tree.select(k // 2 + 1).key
        total += median
    return total
