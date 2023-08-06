# goerrpy

Decorator for simulating Go's error handling in Python

A simple example:
```python
from goerrpy import goerr

@goerr()
def hello_world(): 
    raise Exception("WORLD SHALL NOT BE GREETED!")

value, err = hello_world()

if err is not None:
    print(err)
```

Passing variables:
```python
@goerr()
def get_numbers_larger_than_five(list: typing.List):
    result = []
    for num in list:
        if type(num) is not int:
            raise Exception("All values should be integers!")

        if num > 5:
            result.append(num)

    return result


value, err = get_numbers_larger_than_five([4, 5, 6, 7])

if err is not None:
    print(err)

# value is [6, 7]
```

How to unpack multiple values:
```python 
@goerr(unpack=True)
def get_numbers_smaller_than_five_but_unpack(list: typing.List):
    result = []
    for num in list:
        if type(num) is not int:
            raise Exception("All values should be integers!")

        if num < 5:
            result.append(num)

    return result, result  # so that it can be unpacked


first_list, second_list, err = get_numbers_smaller_than_five_but_unpack([3, 4, 5, 7])

if err is not None:
    print(err)

# first_list is [3, 4] and second_list is [3, 4]
```