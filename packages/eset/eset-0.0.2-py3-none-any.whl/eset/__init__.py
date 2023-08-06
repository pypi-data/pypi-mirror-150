import collections
import copy
import itertools


def _decode(s):
    if isinstance(s, eset):
        return s._items.keys(), s._complement
    if isinstance(s, (frozenset, set)):
        return s, False
    if isinstance(s, dict):
        return s.keys(), False
    raise TypeError(f'unsupported operand types(s): {s.__class__}')


def frozen(iterable=(), complement=False):
    if isinstance(iterable, eset) and iterable.frozen:
        return iterable
    return eset(iterable, complement, True)


class eset(collections.Collection):
    """
    Set and complement sets
    >>> 'hello' in ~eset(['hello'])
    False
    >>> 'bye' in ~eset(['hello'])
    True
    >>> ~eset(['hello']) & ~eset(['bye'])
    ~eset(['hello', 'bye'])
    >>> ~eset(['hello']) & set(['bye'])
    eset(['bye'])
    >>> ~eset(['hello']) | ~eset(['bye'])
    ~eset()
    >>> ~eset(['hello']) | set(['bye'])
    ~eset(['hello'])
    >>> ~eset(['hello']) - ~eset(['bye'])
    eset()
    >>> ~eset(['hello']) - {'bye'}
    ~eset(['hello', 'bye'])
    >>> eset(['hello']) == set(['hello'])
    True
    >>> set(['hello']) == eset(['hello'])
    True
    """
    def __init__(self, iterable=(), complement=False, frozen=False):
        self._items = dict.fromkeys(iterable)
        self._complement = complement
        self._frozen = frozen

    def _mutates(self):
        if self._frozen:
            raise TypeError(f'cannot mutate frozen eset')

    @property
    def complement(self):
        return self._complement
    @property
    def frozen(self):
        return self._frozen
    def freeze(self):
        self._frozen = True
        return self
    def thaw(self):
        self._frozen = False
        return self

    def __iter__(self):
        return iter(self._items)
    def __repr__(self):
        items = ', '.join(repr(i) for i in self)
        if items:
            items = '[' + items + ']'
        mode = '~' if self._complement else ''
        out = f'{mode}{self.__class__.__name__}({items})'
        if self._frozen:
            out = f'frozen({out})'
        return out

    def __copy__(self):
        return self.__class__(self._items, self._complement, self._frozen)
    def __deepcopy__(self):
        return copy.deepcopy(self)
    def _fork(self, iterable, complement):
        return self.__class__(iterable, complement, frozen=self._frozen)

    def __len__(self):
        return len(self._items)
    def __abs__(self):
        return self.cardinality()
    def cardinality(self):
        if self._complement:
            import math
            return math.inf # FIXME: this is aleph-1 when really we're aleph-0
        return len(self._items)
    def __bool__(self):
        return True if self.complement else bool(self._items)
    def __invert__(self):
        return self._fork(self._items, not self._complement)
    def __contains__(self, item):
        if self.complement:
            return item not in self._items
        return item in self._items

    def __eq__(self, other):
        items, c = _decode(self)
        oitems, oc = _decode(other)
        return c == oc and items == oitems
    def __le__(self, other):
        items, c = _decode(self)
        oitems, oc = _decode(other)
        if c and oc:        # ~A <= ~B
            return oitems <= items
        if c and not oc:    # ~A <= B
            return False
        if not c and oc:    # A <= ~B
            return not items & oitems
        return items <= oitems
    def __lt__(self, other):
        items, c = _decode(self)
        oitems, oc = _decode(other)
        if c and oc:        # ~A < ~B
            return oitems < items
        if c and not oc:    # ~A < B
            return False
        if not c and oc:    # A < ~B
            return not items & oitems
        return items < oitems
    def __ge__(self, other):
        items, c = _decode(self)
        oitems, oc = _decode(other)
        if c and oc:        # ~A >= ~B
            return oitems >= items
        if c and not oc:    # ~A >= B
            return not items & oitems
        if not c and oc:    # A >= ~B
            return False
        return items >= oitems
    def __gt__(self, other):
        items, c = _decode(self)
        oitems, oc = _decode(other)
        if c and oc:        # ~A > ~B
            return oitems > items
        if c and not oc:    # ~A > B
            return not items & oitems
        if not c and oc:    # A > ~B
            return False
        return items > oitems
    def issubset(self, other):
        return self <= other
    def issuperset(self, other):
        return self >= other

    def __and__(self, other):
        items, c = _decode(self)
        oitems, oc = _decode(other)
        if c and oc:        # ~A & ~B
            return self._fork(itertools.chain(items, oitems), True)
        if c and not oc:    # ~A & B
            return self._fork((i for i in oitems if i not in items), False)
        if not c and oc:    # A & ~B
            return self._fork((i for i in items if i not in oitems), False)
        return self._fork((i for i in items if i in oitems), False)
    def __rand__(self, other):
        return self & other

    def __or__(self, other):
        items, c = _decode(self)
        oitems, oc = _decode(other)
        if c and oc:        # ~A | ~B
            return self._fork((i for i in items if i in oitems), True)
        if c and not oc:    # ~A | B
            return self._fork((i for i in items if i not in oitems), True)
        if not c and oc:    # A | ~B
            return self._fork((i for i in oitems if i not in items), True)
        return self._fork(itertools.chain(items, oitems), False)
    def __ror__(self, other):
        return self | other

    def __sub__(self, other):
        items, c = _decode(self)
        oitems, oc = _decode(other)
        if c and oc:        # ~A - ~B
            return self._fork((i for i in items if i in oitems), False)
        if c and not oc:    # ~A - B
            return self._fork(itertools.chain(items, oitems), True)
        if not c and oc:    # A - ~B
            return self._fork((i for i in oitems if i in items), False)
        return self._fork((i for i in items if i not in oitems), False)
    def __rsub__(self, other):
        if isinstance(other, (frozenset, set)):
            other = self._fork(other, False)
        return other - self

    def __xor__(self, other):
        return (self | other) - (self & other)
    def __rxor__(self, other):
        return self ^ other

    # mutable methods
    def clear(self, restore=True):
        """
        Clears all state
        """
        self._mutates()
        self._items.clear()
        if restore:
            self._complement = False
        return self
    def add(self, item):
        """
        Adds an item
        """
        self._mutates()
        self._items[item] = None
        return self
    def discard(self, item):
        """
        Removes an item
        """
        self._mutates()
        self._items.pop(item, None)
        return self
    def update(self, items):
        """
        Adds items
        """
        self._mutates()
        for k in items:
            self._items[k] = None
        return self
    def __iand__(self, other):
        self._mutates()
        r = self & other
        self._items = r._items
        self._complement = r._complement
        return self
    def __ior__(self, other):
        self._mutates()
        r = self | other
        self._items = r._items
        self._complement = r._complement
        return self
    def __isub__(self, other):
        self._mutates()
        r = self - other
        self._items = r._items
        self._complement = r._complement
        return self
    def __ixor__(self, other):
        self._mutates()
        r = self ^ other
        self._items = r._items
        self._complement = r._complement
        return self
