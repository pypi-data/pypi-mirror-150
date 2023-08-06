# eset
Extended sets - support for set complement

## Overview

An `eset` works like a normal python `set` except that you can invert it to generate its
complement.  For example, let's say you have the following:

```
>>> from eset import eset
>>> s = eset(['hello'. 'there'])
>>> s_invert = ~s
>>> s_invert
~eset(['hello', 'there'])
```

In this example, `s_invert` contains everything _except_ `'hello'` and `'there'`.

## Logic

All the logic operations you'd expect from sets are available in esets, including
intersection, union, difference, and symmetric difference.  Use the `&`, `|`, `-`, and `^`
operators respectively.

Similarly, conditional expressions are available to determine subset relationships.
If `A <= B`, that A is a subset of B.
