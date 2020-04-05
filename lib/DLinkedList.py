##!/usr/bin/python3


# define class for each linked list node
class _Node:
    def __init__(self, data):
        self.prev = self.next = None
        self.data = data


# define the class for the doubly linked list
class DLinkedList:
    def __init__(self):
        self.head = self.tail = None

    # iterate through the list and return each node
    def __iter__(self):
        cursor = self.head
        while cursor is not None:
            node = cursor
            cursor = cursor.next
            yield node

    # adds a new node to the end of the list
    def _add_node(self, data):
        node = _Node(data)
        # if head is None, list is empty and node should be both head and tail
        if self.head is None:
            self.head = self.tail = node
            return
        # otherwise, set current tail's next to the new node, the new node's previous to current tail
        # then update tail to the new node
        self.tail.next = node
        node.prev = self.tail
        self.tail = node

    # adds a node to the front of the list
    def _add_node_head(self, data):
        node = _Node(data)
        # if head is none, list is empty and node should be both head and tail
        if self.head is None:
            self.head = self.tail = node
            return
        # otherwise, set current head's prev to the new node, the new node's next to current head
        # then update head to the new node
        self.head.prev = node
        node.next = self.head
        self.head = node

    # removes a node
    # argument is the data to match to
    def _remove_node(self, data):
        for cursor in DLinkedList.__iter__(self):
            if cursor.data == data:
                # only 1 item in list, make it empty
                if self.head == self.tail:
                    self.head = None
                    self.tail = None
                # more than 1, currently head
                elif self.head.data == data:
                    self.head = self.head.next
                    self.head.prev = None
                # more than 1, currently tail
                elif self.tail.data == data:
                    self.tail = self.tail.prev
                    self.tail.next = None
                # more than 2, not head or tail
                else:
                    cursor.prev.next = cursor.next
                    cursor.next.prev = cursor.prev

    # swaps position of given node with its next
    def _swap_node(self, node):
        # list is empty or only length 1, nothing to swap
        # if next is none, nothing to swap
        if (self.head == self.tail) or (node.next is None):
            return
        temp_data = node.data
        node.data = node.next.data
        node.next.data = temp_data

    # insert a node after position of existing node
    # first argument is existing node
    # second argument is node to insert after
    def _insert_node(self, index_node, new_data):
        new_node = _Node(new_data)
        # if head is None, list is empty so new_node is head and tail
        if self.head is None:
            self.head = self.tail = new_node
            return

        # make sure if we inserted after tail we update it
        if index_node == self.tail:
            self.tail = new_node

        new_node.next = index_node.next

        if index_node.next is not None:
            new_node.next.prev = new_node

        index_node.next = new_node
        new_node.prev = index_node

    def _clear(self):
        self.head = self.tail = None