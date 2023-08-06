# litecollections

Python collections and common container types, except its all backed by SQLite.

This library can be useful for:

- large scale data operations that can utilize your disk capacity instead of needing to squeeze everything in ram
- zero learning curve if you know how to use stdlib data types
- data crunching in extremely low RAM environments

### To Install

```
pip install litecollections
```

If you want test utilities included, set the environment variable `$TEST_TOOLS` to `1` like the following.

```
TEST_TOOLS=1 pip install litecollections
```

### The Data Types

| stdlib equivalent | `litecollections` alternative |
|:---|:---|
|`dict` | `LiteDict` |
|`list` | _Coming Soon_ |
|`set` | _Coming Soon_ |
|`collections.namedtuple` | _Coming Soon_ |
|`collections.deque` | _Coming Soon_ |
|`collections.Counter` | _Coming Soon_ |
|`collections.OrderedDict` | _Coming Soon_ |
|`collections.defaultdict` | _Coming Soon_ |
|`queue.Queue` | _Coming Soon_ |
|`queue.LifoQueue` | _Coming Soon_ |
|`queue.PriorityQueue` | _Coming Soon_ |
|`queue.SimpleQueue` | _Coming Soon_ |
|`array.ArrayType` | _Coming Soon_ |
|`graphlib.TopologicalSorter` | _Coming Soon_ |
