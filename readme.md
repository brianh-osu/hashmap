**HashMap Implementation**

This is my HashMap implementation from my data structures class. 

HashMap uses a Dynamic Array (DA) and each DA contains either a Linked List or a HashEntry object.

For the chain implementation, we use DA containing Linked List nodes. The table is resized any time the current load factor is greater than or equal to 1.0. 

For the open addressing implementation, 
we use DA containing HashEntry objects.
Each HashEntry object contains a key, value, and tombstone. 
Quadratic Probing is used to address collision.
