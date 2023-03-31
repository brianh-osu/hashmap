# Name: Brian Hsiang
# OSU Email: hsiangb@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: Fri March 17, 11:59pm
# Description: Maps and hash table assignment - using open addressing

from DS_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    _hash_function: object

    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution *quadratic probing can be done w/o exponents, or even multiplication
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Method updates the key/value pair for the hash map.
        If the given key already exists in the hash map, the value should replace
        the existing one.
        If the given key doesn't exist in the hash map, a new key/value pair is added.
        *If table factor is >= 0.5, the table is to be resized to 2x current capacity.
        """
        if self.table_load() >= 0.5:
            self.resize_table(2*self.get_capacity())
        index = self._hash_function(key)

        #3 scenarios
        #1. If it is none, just insert the value
        #2. If the given key already exists in the hash map, replace the key's value with the new value.
        #3. If the given key doesn't exist, add the key/value pair (probe as needed).

        #Revised v2: to incorporate tombstone verbiage
        #1. if it's been removed before (tombstone = True), replace it with new HashEntry, and increment size.
        #2. if the key existing key = your key, just update the value. Replace with HashEntry(same key, new value).
        #   No need to increment size.
        #3. If nothing is there (None), just set the HashEntry and increment size.

        j = 0
        while True:
            probe = (index + j**2) % self._capacity #quad probe formula
            if self._buckets[probe] is not None:
                if self._buckets[probe].is_tombstone is True: #'pseudo'-None since a bucket was 'removed'
                    self._buckets.set_at_index(probe, HashEntry(key, value))
                    self._size += 1
                    break
                if self._buckets[probe].key == key and self._buckets[probe].is_tombstone is False:
                    self._buckets.set_at_index(probe, HashEntry(key,value))
                    break
            elif self._buckets[probe] is None: #'actual'-None, since bucket was never initialized w/a HashEntry
                self._buckets.set_at_index(probe, HashEntry(key, value))
                self._size += 1
                break
            #At this point we can re-probe as we've exhausted all options:
            # bucket was 'removed' at some point, has matching key, or bucket has None.
            j += 1


    def table_load(self) -> float:
        """
        Method returns the table factor
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        Method returns the # of empty buckets in the Hashtable
        """
        result = 0
        for x in range(self._buckets.length()):
            if self._buckets[x] is None:
                result += 1
        return result

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity. All existing key/value pairs must remain in the new hash map, and
        all the hash table links must be rehashed.
        First, check the new_capacity is not less than the current # of elements in the hash map.
        If so, do nothing.
        Second, if new_capacity is valid then make sure its prime. If not, change it to the next prime.
        """
        if new_capacity < self._size:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity

        copy_da = self._buckets
        self._buckets = DynamicArray()
        self._size = 0

        for x in range(self.get_capacity()):
            self._buckets.append(None)


        for x in range(copy_da.length()):
            if copy_da[x] is not None:
                if copy_da[x].is_tombstone is False:
                    self.put(copy_da[x].key, copy_da[x].value)

        # print('resized', self._buckets)

    def get(self, key: str) -> object:
        """
        Method returns the value associated with the given key.
        If key is not in the hash map, return None.
        """
        for x in range(self._buckets.length()):
            if self._buckets[x] is not None:
                if self._buckets[x].is_tombstone is True: #if it's 'Removed', it's technically non-existent (None)
                    return None
                if self._buckets[x].key == key:
                    return self._buckets[x].value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if the given key is in the hash map. Otherwise return False.
        *An empty hash map does not contain any keys.
        """
        for x in range(self._buckets.length()):
            if self._buckets[x] is not None:
                if self._buckets[x].key == key:
                    return True
        return False


    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.
        """
        for x in range(self._buckets.length()):
            if self._buckets[x] is not None:
                if self._buckets[x].key == key:
                    if self._buckets[x].is_tombstone is True: #if the bucket is a tombstone, skip decrementing size.
                        continue
                    self._buckets[x].is_tombstone = True #if it wasn't a tombstone, it now is. Decrement size
                    self._size -= 1

    def clear(self) -> None:
        """
        Method clears the contents of the hash map. does not change the underlying hash table capacity.
        """
        for x in range(self._buckets.length()):
            self._buckets[x] = None
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a DA where each index contains a tuple of a key/value pair stored in the hash map.
        Order of the keys in the DA does not matter.
        """
        result = DynamicArray()
        for x in range(self._buckets.length()):
            if self._buckets[x] is not None:
                if self._buckets[x].is_tombstone is False:
                    result.append((self._buckets[x].key, self._buckets[x].value))
        return result

    def __iter__(self):
        """
        Method enables the hash map to iterate across itself. Implemented in a similar way to the example
        in 'Exploration: Encapsulation and Iterators'. Can either build the iterator functionality inside the
        HashMap class or create a separate iterator class.
        """
        # if key is None:
        #     key = 0
        # key += 1
        self._key = 0
        return self

    def __next__(self):
        """
        Method returns the next item in the hash map, based on the current location of the iterator (__iter__)
        It will need to only iterate over active items.
        """
        try:
            value = self._buckets[self._key]

            # The only time we should return is if it is not None, and if it is not a TS
            # if it is None, then key += 1 and check again.
            while value is None:
                self._key += 1
                value = self._buckets[self._key]
                if value is not None:
                    if value.is_tombstone is True:
                        value = None
        except DynamicArrayException:
            raise StopIteration

        self._key += 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    # # for i in range(10):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #         # print(m._buckets)
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    # #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # # print('buckets :', m._buckets)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(11, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1')) #after put, check the value
    # m.remove('key1')
    # print(m.get('key1')) #after remove, check the value
    # m.remove('key4')
    # #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())
    #
    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
    #
    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
