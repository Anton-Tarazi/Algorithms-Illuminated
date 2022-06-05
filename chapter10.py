class MinHeap:

    def __init__(self, array=None, key=lambda x: x):
        # initialize a function to be used to compare objects in the heap
        self.function = key

        # store a reference to the position of each object as within the queue
        # object: position
        self.positions = {}

        # if no array is provided initialize an empty array
        # otherwise heapify provided array
        if array is None:
            self.data = []
        else:
            self.data = array
            self.heapify()

    @staticmethod
    def left_child_index(index):
        return 2 * index + 1

    @staticmethod
    def right_child_index(index):
        return 2 * index + 2

    @staticmethod
    def parent_node_index(index):
        return (index - 1) // 2

    def add(self, value):
        """Insert an element into the heap- O(log n) runtime"""
        self.data.append(value)
        new_node_index = len(self.data) - 1
        self.positions[value] = len(self.data) - 1
        self._bubble_up(new_node_index)

    def get_min(self):
        """Returns minimum element of heap without deleting it- O(1) runtime"""
        return self.data[0]

    def extract_min(self):
        """Removes and returns minimum element of heap- O(log n) runtime"""
        if len(self.data) == 1:
            return self.data.pop()

        heap_min = self.data[0]
        self.data[0] = self.data.pop()
        self.positions[self.data[0]] = 0
        self._bubble_down(0)

        return heap_min

    def delete_by_index(self, index):
        """Deletes any element of the heap given a pointer to its index in the
        array- O(log n) runtime"""

        # if the array has length 1, or we are deleting the last element
        # no need to bubble up/ down
        if len(self.data) == 1:
            return self.data.pop()
        if index == len(self.data) - 1:
            return self.data.pop()

        object_to_delete = self.data[index]

        # replace object to delete with last element
        self.data[index] = self.data.pop()

        # delete the object from the positions dictionary
        del self.positions[object_to_delete]

        # restore invariant
        self._bubble_up(index)
        self._bubble_down(index)

        return object_to_delete

    def heapify(self):
        """Turn an array into a heap- O(n) runtime"""
        for i in range(len(self.data) - 1, -1, -1):
            self._bubble_down(i)

    def _bubble_up(self, new_node_index):
        """Move node up the tree until invariant is restored"""

        # update positions dict
        self.positions[self.data[new_node_index]] = new_node_index

        parent_index = self.parent_node_index(new_node_index)

        # run if the new node is not at root and parent node is larger
        while new_node_index > 0 and self.function(self.data[new_node_index]) < \
                self.function(self.data[parent_index]):
            # swap node with parent node
            self.data[new_node_index], self.data[parent_index] = \
                self.data[parent_index], self.data[new_node_index]

            # update positions dict
            self.positions[self.data[new_node_index]] = new_node_index
            self.positions[self.data[parent_index]] = parent_index

            # reset node index and recalculate parent index
            new_node_index = parent_index
            parent_index = self.parent_node_index(new_node_index)

    def _bubble_down(self, new_node_index):
        """Move node down tree until invariant is restored"""

        # update positions dict
        self.positions[self.data[new_node_index]] = new_node_index

        # run as long as the new node has a child node with a smaller key
        while self._has_smaller_child(new_node_index):
            # return smaller of the children nodes
            smaller_child_index = self._smaller_child_index(new_node_index)

            # swap node with smaller child
            self.data[new_node_index], self.data[smaller_child_index] = \
                self.data[smaller_child_index], self.data[new_node_index]

            # update positions of these elements in positions dict
            self.positions[self.data[new_node_index]] = new_node_index
            self.positions[self.data[smaller_child_index]] = smaller_child_index

            # reset index of new node to that where it was switched
            new_node_index = smaller_child_index

    def _has_smaller_child(self, index):
        """Helper function to determine whether a node posses a child with a smaller key,
        which violates the heap property"""

        # check if left and right children exist
        left_index = self.left_child_index(index)
        right_index = self.right_child_index(index)
        left_child_exists = left_index <= len(self.data) - 1
        right_child_exists = right_index <= len(self.data) - 1

        # if left child exists check if its smaller
        if left_child_exists:
            left_child_smaller = \
                self.function(self.data[index]) > self.function(self.data[left_index])
        else:
            left_child_smaller = False

        # if right child exists check if its smaller
        if right_child_exists:
            right_child_smaller = \
                self.function(self.data[index]) > self.function(self.data[right_index])
        else:
            right_child_smaller = False

        # return true if one of the children is smaller
        # return false if children don't exist or are larger
        return left_child_smaller or right_child_smaller

    def _smaller_child_index(self, index):
        """Helper function that returns the index of the child node with the smaller key"""
        left_index = self.left_child_index(index)
        right_index = self.right_child_index(index)

        # if right child doesn't exist then return left child
        if right_index >= len(self.data):
            return left_index

        # otherwise, return index of child with smaller index
        if self.function(self.data[right_index]) < self.function(self.data[left_index]):
            return right_index
        else:
            return left_index

    def is_empty(self):
        """Return true if heap is empty (self.data=[]), false otherwise"""
        return len(self.data) == 0

    def size(self):
        """Returns size of heap"""
        return len(self.data)


def heap_median_maintenance_sum(array):
    """Returns sum of kth medians of an array- O(log n) runtime"""

    # initialize max heap and min heap
    smaller_max_heap = MinHeap(key=lambda x: -x)
    larger_min_heap = MinHeap()

    total = 0
    for entry in array:

        # for each incoming entry if it is larger than the smallest element
        # of the min heap, we put it in that heap, otherwise we put it in the
        # smaller max heap
        if larger_min_heap.size() == 0 or entry > larger_min_heap.get_min():
            larger_min_heap.add(entry)
        else:
            smaller_max_heap.add(entry)

        # re-balance heaps if their sizes are more than 1 apart
        if larger_min_heap.size() >= smaller_max_heap.size() + 2:
            smaller_max_heap.add(larger_min_heap.extract_min())
        if smaller_max_heap.size() >= larger_min_heap.size() + 2:
            larger_min_heap.add(smaller_max_heap.extract_min())

        # depending on the sizes of the heaps the median is either
        # the smallest element in the larger heap or the largest
        # element in the smaller heap
        if larger_min_heap.size() > smaller_max_heap.size():
            current_median = larger_min_heap.get_min()
        else:
            current_median = smaller_max_heap.get_min()

        total += current_median
    return total
