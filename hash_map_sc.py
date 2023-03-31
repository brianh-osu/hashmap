# Name: Brian Hsiang
# OSU Email: hsiangb@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: Friday March 17, 11:59pm
# Description: Maps and hash table assignment- using chain implementation


from DS_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates the key/value pair in the hash map. If the given key already exists in the hash map,
        its associated value must be replaced with the new value. If the key is not in the hash map,
        a new key/value pair must be added.
        *The table must be resized to double its current capacity when this method is called and the current
        load factor of the table is >= 1.0
        """
        if self.table_load() >= 1.0:
            self.resize_table(2*self._capacity)
        index = self._hash_function(key) % self._capacity #index for DA

        LL = self._buckets.get_at_index(index) #accesses the LinkedList's within the DA

        found = False #initialize variable for finding the key #v1
        for node in LL:                    #within the node..
            if node.key == key:            #if node's key = user key
                node.value = value         #re-assign node's value to user value
                found = True
        if found is False: #if not found, then insert key to LL and increment size
            LL.insert(key, value)
            self._size += 1



    def empty_buckets(self) -> int:
        """
        Returns the # of empty buckets in the hash table.
        """
        result = 0
        for x in range(self._buckets.length()):
            if self._buckets[x].length() == 0:
                result += 1
        return result
        # return(self.get_capacity() - self.get_size()) #refactored :-) <- doesn't work


    def table_load(self) -> float:
        """
        Method returns the current hash table load factor.
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Method clears the contents of the hash map. Does nto change the underlying hash table capacity.
        """
        for x in range(self.get_capacity()):
            self._buckets[x] = LinkedList()
        self._size = 0


    def resize_table(self, new_capacity: int) -> None:
        """
        **Resize table does not figure out if the table needs to be resized or not. By the fact it is called, it means it
        does need to be resized. We've got our new capacity. Now go ahead and rehash everything w the new table.

        This method changes the capacity of the internal hash table. All existing key/value pairs must remain in the new
        hash map, and all hash table links must be rehashed.

        First check that new_capacity is not less than 1; if so, the method does nothing.
        If new_capacity is >= 1, make sure it is a prime number. If not, change it to the next highes tprime number.
        """
        if new_capacity < 1: #if new_capacity <1, do nothing.
            return

        if self._is_prime(new_capacity) is False: #need to check if new_capacity is a prime# first.
            new_capacity = self._next_prime(new_capacity) #if not, then update it.
        self._capacity = new_capacity

        copy_da = self._buckets #create copy of current buckets
        self._buckets = DynamicArray() #reset buckets to blank
        self._size = 0 #reset size to 0 (using put will increase size as need)

        for x in range(self.get_capacity()): #capacity remains the same,
            self._buckets.append(LinkedList()) # iterate and append empty LL's to self._buckets
        for x in range(copy_da.length()): #We have to rehash all the hash table LL's.
            copy_bucket_LL = copy_da[x] #point to LL
            for y in copy_bucket_LL: #access the LL
                self.put(y.key, y.value) #put copy_da's LL nodes into the blank LL's within self._buckets


    def get(self, key: str):
        """
        This method returns the value associated with the given key. If the key is not in the
        hash map, return None.
        (Hash in, if the value is not there, then return None).
        """
        index = self._hash_function(key) % self._capacity
        for x in self._buckets[index]:
            if x.key == key:
                return x.value
        return None


    def contains_key(self, key: str) -> bool:
        """
        Method returns True if the key is in the hash map, otherwise return False.
        *An empty hash map does not contain any keys.
        """
        index = self._hash_function(key) % self._capacity
        for x in self._buckets[index]:
            if x.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map.
        If the key is not in the hash map, do nothing
        """
        for x in range(self.get_capacity()):
            if self._buckets[x].contains(key): #poitns to DA. If DA contains the given key..
                LL = self._buckets[x] #accesses the LL within the bucket (DA).
                LL.remove(key) #call remove on the LL, passing given key.
                self._size -= 1  #hash map size decrement


    def get_keys_and_values(self) -> DynamicArray:
        """
        Method returns a DA where each index contains a tuple of a (key, value) pair stored in the
        hash map. The order of keys int he DA does not matter.
        """
        result = DynamicArray()
        for x in range(self.get_capacity()):
            if self._buckets[x].length() != 0: #if there's something here, store value to result
                LL = self._buckets[x]
                current = LL._head #current refers to the node within LL
                while current is not None: #iterate using while. Adding (key,value)
                    result.append((current.key, current.value))
                    current = current.next
        return result



def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Function rcvs a DynamicArray (not guaranteed sorted), returns a tuple containing in this order:
    1. A dynamic array comprising the mode (most occuring) value(s) of the array,
    2. an integer representing the highest frequency (how many time the mode value(s) appear)
    If more than 1 mode exists, the values should be captured in the DA returned (order doesn't matter).
    E.g. if mode contains only 1 value, the DA will only have that value.
    *Must be written in O(N) complexity.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    for x in range(da.length()):
        # map.put(da[x], 0) #The below is same as put() except if the key exists then we increment 1 (i/o replace its value)
        if map.table_load() >= 1.0:
            map.resize_table(2*map._capacity)
        index = map._hash_function(da[x]) % map.get_capacity()
        LL = map._buckets.get_at_index(index)
        found = False
        for node in LL:
            if node.key == da[x]:
                node.value += 1
                found = True
        if found is False:
            LL.insert(da[x], 1)
            map._size += 1
    # print(map) #map initialized and ready to iterate + determine mode

    result_da = DynamicArray() #initialize result_da first so you can append max values (strings) during comparison.
    LL_max_freq, LL_max_val = None, None  # max frequency and max value (string) within LL

    #1. iterate through each Hashtable element (Linked lists) and get the maximum.
    #1b if more than 1 element is a maximum, it's added to the resulting DA.
    #** When setting up the while loop, be sure to account for if current.next is None (you're just
    #   comparing the node to itself to get the LL_max).
    for x in range(da.length()):
        index = map._hash_function(da[x]) % map.get_capacity()
        LL = map._buckets.get_at_index(index)
        current = LL._head
        if current is not None: #only traverse LL if head is not None.
            if LL_max_freq is None and LL_max_val is None:
                LL_max_freq = current.value #sets the max as the value of the first key (string)
                LL_max_val = current.key
                result_da.append(LL_max_val)
                current = current.next #for the very first iteration, we can skip comparing current
            while current is not None:
                if current.value > LL_max_freq:
                    LL_max_val = current.key
                    LL_max_freq = current.value
                    result_da = DynamicArray()
                    result_da.append(LL_max_val)
                if current.value == LL_max_freq: #and if result_da does not contain the LL_max_val
                    result_da.append(current.key)
                current = current.next

    #result_da contains duplicates, final_da will contain unique values.
    final_da = DynamicArray() #iterate through result_da and append the first appearance into final_da
    for x in range(result_da.length()):
        current_val = result_da[x]
        duplicate = False #initialize duplicate as false. If current_aal exists in final_da, then we don't need to add it.
        for y in range(final_da.length()):
            if final_da[y] == current_val:
                duplicate = True
        if duplicate is False:
            final_da.append(current_val)

    # print("map's max frequency count: ", map_max_freq, "\ncorresponding key(string): ", map_max_val)
    return (final_da, LL_max_freq)





# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         # print(m.empty_buckets())
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
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
    # #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
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
    # #
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
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value') #after put, the size is not correct
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))
    #
    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # #
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
    # m = HashMap(53, hash_function_1)
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
    # #
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
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    # #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")
    #
    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )
    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
