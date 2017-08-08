Motivation
==========

This library may be used to translate numerals to decimals and vice
versa. It is intended to be used with the general dictation produced
by an SR (speech recognition) engine such as the one in
Dragon. Libraries similar to this one already exist; but all of the
ones I have found were either closed source or lacked the features
that I was looking for.

Testing & Quality
-----------------

The API methods were tested for the first 1 billion integers with the
chunk size ranging between -4 and 1. An example should make the
meaning of 'chunk size' clear.

EXAMPLE: Convert the decimal 123456 to numerals using (a) a chunk size
of 4 and (b) a chunk size of -4.

Solution:

(a) Since the chunk size is positive, split the decimal into chunks
    from left to right.

123456 -> 1234,56-> one thousand two hundred thirty four fifty six

(b) Since the chunk size is negative, split the decimal into chunks
    from right to left.

123456 -> 12,3456-> twelve three thousand four hundred fifty six

Why is chunking important? Because it makes manual data entry much
easier.  It is easier to say 'ten ten ten' than 'one million ten
thousand ten' to enter the number 101010.

PIP Installation
----------------

TODO

Manual Installation (Example)
-----------------------------

The following may be used to install num_dec on Debian.

```
$ sudo install -D num_dec.py /usr/share/python/num_dec/num_dec.py
```

Usage (Examples)
----------------

Start python.

```python

>>> import num_dec

# Convert the traditional (long) way

>>> num_dec.toNumerals("123",0)
'one hundred twenty three'

>>> num_dec.toDecimal('one hundred twenty three')
'123'

# Convert digit-by-digit

>>> num_dec.toNumerals("123",1)
'one two three'

>>> num_dec.toDecimal('one two three')
'123'

# Convert with other dictation present

>>> num_dec.toNumerals("12 equals 12")
'twelve equals twelve'

>>> num_dec.toDecimal("twelve equals twelve")
'12 equals 12'

# Test the package for the first 1000 integers

>>> num_dec.testPackage(1000)
``` 

Manual Removal (Example)
------------------------

The following may be used to remove num_dec on Debian.

```
$ rm -rf /usr/share/python/num_dec
```

Invertibility Of Chunking
-------------------------

Converting decimals to numerals by chunking from left to right is not
always invertible, since 970053->9700,53->ninety seven hundred fifty
three->9753. Curiously chunking from right to left works:
970053->97,0053->ninety seven zero zero fifty three->970053. In
general,

 (1) Converting decimals to numerals by chunking from right to left
     is invertible.

The result is not particularly convenient since the reading order in
English is from left to right. However, at least one useful
consequence may gleaned from (1):

 (2) Converting decimals to numerals by chunking is invertible if all
     chunks are of the same size.

Thus chunking digit-by-digit will always work.

Public API
----------

 The API consists of two functions:

 1) toDecimal(str)

 which takes a single argument: <str> -- a string of space separated
                                         English words possibly
                                         including punctuation

 2) toNumerals(str, int)

 which takes two arguments: <str> -- a string of space separated
                                       English words possibly
                                       including punctuation

                            <int> -- an integer indicating the
                                     chunk size

Key Features of 'toDecimal'
---------------------------

 1) Supports chunking:

    toDecimal("four five nine two") = 4592

 2) Does not alter non-numerals:

    toDecimal("I'll have thirteen eggs for breakfast.") =
    "I'll have 13 eggs for breakfast."

 3) Can handle long dictations:

    toDecimal("one two three four five six seven eight nine ten") =
    12345678910

Key Features of 'toNumerals'
----------------------------

 1) Supports chunking:

    toNumerals("4592",2) = "forty five ninety two"

 2) Does not alter non-decimals:

    toNumerals("The number A8 in hexadecimal is 168 in decimal.",0) =
    "The number A8 in hexadecimal is one hundred sixty eight in
    decimal."

 3) Can handle large decimals:

    toNumerals("12345678910",1) =
    "one two three four five six seven eight nine ten"