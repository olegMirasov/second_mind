class Node:
    def __init__(self, parent, prev=None, next=None):
        self.parent = parent
        self.prev = prev
        self.next = next


class MyList:
    def __init__(self):
        self.first_node = None
        self.last_node = None

    def add_node(self, node: Node):
        if not self.last_node:
            self.first_node = self.last_node = node
            return

        node.prev = self.last_node
        self.last_node.next = node
        self.last_node = node

    def r_pop(self):
        result = self.last_node
        if self.last_node and self.last_node.prev:
            self.last_node.prev.next = None
        else:
            self.last_node = self.first_node = None
        return result

