# '''
# Linked List hash table key/value pair
# '''
class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add_to_head(self, key, value):
        # adds key, value pair to head of linked list
        placeholder = self.head
        self.head = LinkedPair(key, value)
        self.head.next = placeholder

    def contains(self, key):
        # takes key and returns value if available
        if self.head == None:
            return None
        current = self.head
        while current != None:
            if current.key == key:
                return current.value
            else:
                current = current.next

    def remove(self, key):
        if self.head.key == key:
            self.head = self.head.next
            return key
        current = self.head
        while current.next != None:
            if current.next.key == key:
                current.next = current.next.next
                return key
        return "(key, value) pair not found!"

class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.count = 0

    
    def __len__(self):
        return self.capacity


    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.

        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)


    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash

        OPTIONAL STRETCH: Research and implement DJB2
        '''
        hash_djb2 = 5381
        for c in key:
            hash_djb2 = ((hash_djb2 << 5) + hash_djb2) + ord(c)
        return hash_djb2


    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash_djb2(key) % self.capacity


    def insert(self, key, value):
        '''
        Store the value with the given key.

        # Part 1: Hash collisions should be handled with an error warning. (Think about and
        # investigate the impact this will have on the tests)

        # Part 2: Change this so that hash collisions are handled with Linked List Chaining.

        Fill this in.
        '''
        hashed_key = self._hash_mod(key)

        # store value if hashed index is None
        if self.storage[hashed_key] == None:
            self.storage[hashed_key] = (key, value)
            self.count += 1
        # store value in linked list if collision
        elif type(self.storage[hashed_key]) == tuple:
            placeholder = self.storage[hashed_key]
            self.storage[hashed_key] = LinkedList()
            self.storage[hashed_key].head = LinkedPair(placeholder[0], placeholder[1])
            self.storage[hashed_key].add_to_head(key, value)
        # store value in linked list when there's already a collision here
        else:
            self.storage[hashed_key].add_to_head(key, value)


    def remove(self, key):
        '''
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Fill this in.
        '''
        hashed_key = self._hash_mod(key)

        # print warning statement if nothing at hashed index
        if self.storage[hashed_key] == None:
            print("(key, value) pair not found!")
        # remove if key, value pair at hashed index and is not linked list
        elif type(self.storage[hashed_key]) == tuple:
            self.storage[hashed_key] = None
            self.count -= 1
        # remove if key, value pair at hashed index and is linked list
        else:
            self.storage[hashed_key].remove(key)


    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Fill this in.
        '''
        hashed_key = self._hash_mod(key)

        # returns value at hashed index, should automatically return None
        # if nothing stored at hashed index
        if self.storage[hashed_key] == None:
            return None
        elif type(self.storage[hashed_key]) == tuple:
            return self.storage[hashed_key][1]
        else:
            return self.storage[hashed_key].contains(key)


    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.

        Fill this in.
        '''
        # store old self.storage into old_storage to iterate over later
        old_storage = self.storage
        # create new HashTable with double capacity
        self.capacity += self.capacity
        self.storage = [None] * self.capacity
        # iterate over old_storage to populate new self.storage
        for item in old_storage:
            # handle if storage item is None
            if item == None:
                pass
            # if storage item is tuple, re-insert
            elif type(item) == tuple:
                self.insert(item[0], item[1])
            # if storage item is linked list, iterate over linked list while re-inserting
            else:
                current = item.head
                while current != None:
                    self.insert(current.key, current.value)
                    current = current.next


if __name__ == "__main__":
    ht = HashTable(2)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")

    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    old_capacity = len(ht.storage)
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
