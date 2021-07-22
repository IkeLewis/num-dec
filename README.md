Overview
========

This library may be used to convert numerals to decimals; it is
intended to be used to process the dictation produced by a
speech-recognition engine such as the one in Dragon.

Public API
----------

The API consists of just one function 'toDecimal' which takes a single
string argument.

Chunking
--------

The purpose of chunking is to make numbers easier to enter.  For
example, saying 'ten ten ten' is easier than saying 'one hundred one
thousand ten' to enter the number 101010.  In the first case, the
chunk size is 2, but in the second case, the chunk size is 6.

```python
>>> num_dec.toDecimal("ten ten ten")
'101010'

>>> num_dec.toDecimal("one hundred one thousand ten")
'101010'
```

Converting decimals to numerals by chunking is not always invertible;
970053->9700,53->ninety seven hundred fifty three->9753!=970053.  This
issue can be addressed by simply pronouncing zeros;
970053->97,0,0,53->ninety seven zero zero fifty three->970053.

```python
>>> num_dec.toDecimal("ninety seven hundred fifty three")
'9753'

>>> num_dec.toDecimal("ninety seven zero zero fifty three")
'970053'
```

Usage Examples
--------------

The function 'toDecimal'

 1) supports chunking:

    ```python
    >>> num_dec.toDecimal("four five nine two")
    '4592'
    ```

 2) does not alter non-numerals:

    ```python
    >>> num_dec.toDecimal("I'll have thirteen eggs for breakfast.")
    "I'll have 13 eggs for breakfast."
    ```

 3) can handle long dictations:

    ```python
    >>> num_dec.toDecimal("one two three four five six seven eight nine ten")
    '12345678910'
    ```

Installation
------------

On most Linux machines, the following command may be used:

```
$ sudo install -D num_dec.py /usr/share/python/num_dec/num_dec.py
```

Testing
-------

The API methods were tested for the first 1 billion integers with the
chunk size ranging between -4 and 1, where a negative chunk size means
that digits were grouped from right to left.  The tests may be rerun
for all natural numbers from 0 to 10000 with the following command:

```python
>>> num_dec.testPackage(10000)
```

Removal
-------

On most Linux machines, the following may be used to remove num_dec:

```
$ sudo rm -rf /usr/share/python/num_dec
```
