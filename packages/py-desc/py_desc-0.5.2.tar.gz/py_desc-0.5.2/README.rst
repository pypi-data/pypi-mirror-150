py-desc
=======

Installation
------------
``pip install py-desc``

Usage
-----

Simple built-in types
^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> from py_desc.built_in import *
    >>>
    >>> class YourClass:
    ...     bool_var = Boolean()
    ...     string_var = String()
    ...     positive_int_var = PositiveInteger()
    >>>
    >>> a = YourClass()
    >>> a.positive_int_var = 5
    >>> a.string_var = 'str'
    >>> a.bool_var = True
    >>>
    >>> a.bool_var = 'string'
    ValueError: Must be boolean
    >>> a.string_var = 5
    ValueError: Must be string
    >>> a.positive_int_var = -10
    ValueError: Cannot be negative

Custom Types
^^^^^^^^^^^^

.. code:: python

    >>> from py_desc.built_in import *
    >>>
    >>> class YourCustomClass:
    ...     first = CustomInteger(left=5)
    ...     second = CustomInteger(right=10)
    ...     third = CustomInteger(left=1, right=10)
    >>>
    >>> a = YourClass()
    >>> a.first = 2
    ValueError: Cannot be smaller than 5
    >>> a.second = 50
    ValueError: Cannot be equal or bigger than 10
    >>> a.third = 6  # OK. this value in range 1-10
    >>> a.third = 12
    ValueError: Cannot be not in range [1:10]

.. code:: python

    >>> from py_desc.built_in import *
    >>>
    >>> @dataclass
    >>> class ExampleData:
    ...     name: str
    ...     age: int
    >>>
    >>>
    >>> class YourCustomClass:
    ...     custom_list_int = CustomList(int)
    ...     custom_list_data = CustomList(ExampleData)
    >>>
    >>> a = YourCustomClass()
    >>> a.custom_list_int = [5, 6, 3, 6]  # OK. The same type was given
    >>> a.custom_list_int = [5.6, 2.1, 'str']
    ValueError: Values in list must be int
    >>> a.custom_list_data = [ExampleData(name='Carl', age=23), ExampleData(name='Daniel', age=21)]
    >>> print(a.custom_list_data)
    [ExampleData(name='Carl', age=23), ExampleData(name='Daniel', age=21)]
    >>> a.custom_list_data = (ExampleData(name='Carl', age=23), ExampleData(name='Daniel', age=21))
    ValueError: Must be list
