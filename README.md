[![PyPI version](https://badge.fury.io/py/hashed-list.svg)](https://badge.fury.io/py/hashed-list)
[![Downloads](https://pepy.tech/badge/hashed-list/week)](https://pepy.tech/project/hashed-list)

# HashedList
A List with O(1) time complexity for `.index()` method, instead of O(N).

## Description

`HashedList` is a data structure that is pretty much a Python list, except that:
1. The method `.index(value)` is O(1) (Good)
2. It uses twice more memory due to indexing (Not good but still okay)
3. It takes more time than list during initialization due to hashing of each item
4. Items must be unique. It will raise `DuplicateValueError` if
   duplicate item is provided

### Main use case:
You have a huge list of unique, ordered items that:
1. You may update the list (remove, insert, set value etc) from
   time to time
2. You may get the index of a specific item in the list very often

In this case, using just a regular list definitely works but will cost
you O(N) each time you get the index of a specific item. Or, you can
maintain along the list a dictionary of item => index, but that will cost
you the burden of updating the dictionary everytime the list is updated.

HashedList will make the work easy for you.

## Installation
```bash
pip install hashed-list
```

## Usage

Simply instantiate it from an iterable, and use it as you normally would a Python list
```python
from hashed_list import HashedList

# From list
hashed_list_1 = HashedList(["a", "b", "c"])
# From generator
hashed_list_2 = HashedList(x for x in range(100) if x % 2 == 0)
# From sequence
hashed_list_3 = HashedList(range(1, 100, 2))

# Exceptions
from hashed_list import DuplicateValueError
try:
    hashed_list_4 = HashedList([1, 1, 2])
except DuplicateValueError as e:
    print(e)

# Use it like a normal Python list
hashed_list_1[0]  # => "a"
len(hashed_list_3) == len(list(range(1, 100, 2)))  # => True
hashed_list_1.index("c")  # => 2
# The same for .extend(), .append(), .insert(), etc ...
```

## Simple benchmark
On a large list, `HashedList.index()` should be tens of times faster 
than `list.index()` but you can try it yourself by copy-pasting the code below on 
your Python shell

```python
from random import randint
import time

from hashed_list import HashedList

list_size = 999_999
random_values = [randint(list_size // 2, list_size) for _ in range(1000)]

print("Testing list.index()")
t0 = time.time()
very_huge_list = list(range(list_size))
[very_huge_list.index(random_value) for random_value in random_values]
d1 = time.time() - t0
del very_huge_list  # Clear up unused memory
print(f"list.index() took {d1} seconds for {len(random_values)} calls")
# => list.index took 7.381884813308716 seconds for 1000 calls

print("Testing HashedList.index()")
t0 = time.time()
very_huge_hashed_list = HashedList(range(list_size))
# _ = very_huge_hashed_list.index(random_value)
[very_huge_hashed_list.index(random_value) for random_value in random_values]
d2 = time.time() - t0
del very_huge_hashed_list  # Clear up unused memory
print(f"HashList.index() took {d2} seconds for {len(random_values)} calls")
# HashList.index took 0.17798161506652832 seconds for 1000 calls

# Result
print(f"HashList.index() is {d1 // d2} times faster than list.index()!")
# => HashList.index() is 41.0 times faster than list.index()!
```

## Caveats
1. `HashedList` consumes 2 times more memory than Python list
2. `HashedList` consumes more time during initialization due to hashing

Given these caveats, use `HashedArray` only when you know that `.index` is going to be used a lot.

## Development
To start developing for and contributing to this repository:
```bash
# Start a virtual environment
python -m venv .venv
# Install the package from source
python -m install -e .
# Run all tests
python -m unittest discover tests/
# Now you can start developing. Please see src/ and tests/ 
# folders for source code and tests respectively
```

## Links
* [PYPI](https://pypi.org/project/hashed-list/)
