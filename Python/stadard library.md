# Python Standard Library

## Strings

### textwrap

## `heapq`

*   `.heappush(heap, item), .heappop, heappushpop, heapreplace`
    *   heappushpop = push + pop
    *   heapreplace = pop + push
*   `heapq.heapify`
*   `heapq.merge(*iterables, key=None, reverse=False)`:
    *   Merge multiple sorted inputs into a single sorted output (for example, merge timestamped entries from multiple log files). Returns an [iterator](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/glossary.html#term-iterator) over the sorted values.
*   `heapq.nsmallest/largest(n, iterable, key=None)`: