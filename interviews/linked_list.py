class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None
        
    def append_to_tail(self, data):
        end = Node(data)
        node = self
        while node.next is not None:
            node = node.next
        node.next = end
    
    def __str__(self):
        return '({})'.format(self.data)
        
    @staticmethod
    def delete_node(head, data):
        node = head
        if head.data == data:
            return head.next # moved head
        while node.next is not None:
            if node.next.data == data:
                node.next = node.next.next
                return head # head didn't change
            node = node.next
    
    @staticmethod  
    def remove_duplicates(head):
        node = head
        value_counter = dict()
        while node.next is not None:
            value_counter.setdefault(node.data, 0)
            value_counter[node.data] += 1
            node = node.next
        node = head
        while node.next is not None:
            data = node.next.data
            if value_counter.get(data, 0) > 1:
                node.next = node.next.next
                value_counter[data] -= 1
            node = node.next
            
head = Node(0)
for i in [1,2,3,4,5,5,6,7,7,8,9]:
    head.append_to_tail(i)

def print_list(head):
    node = head
    while node.next is not None:
        print(node)
        node = node.next
    print('------------')
        
print_list(head)
head.remove_duplicates(head)
print_list(head)