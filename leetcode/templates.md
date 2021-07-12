# Templates



## Sliding window:

1.  sliding window with non-decreasing size (e.g. longest substring such that ...)

```python
def slidingWindow(s):
    left = 0
    # initiate monitoring variable
    for right in range(len(s)):
        # update monitoring variable by including right
    	if not constraint.isVald():
            # update monitoring variable by excluding left
            left += 1
    return right - left + 1
     
```

## DFS

1.  DFS inorder traverse

```python
stack = []
node = root
while node or stack:
    while node:
        stack.append(node)
        node = node.left
    node = stack.pop()
    read(node)
    node = node.right
```

## Union Find

1.  Unionfind with path compression and union by rank 

    ```python
    parent = {x for x in all_x}
    rank = {0 for x in all_x}
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            # assume px has higher rank
            if rank[px] < rank[py]:
                px, py = py, px
            parent[py] = px
            # update px's rank if their ranks are equal before the union
            rank[px] += (rank[px] == rank[py])
            return 1 # indicates a union happend
        return 0
    ```

## DP

1.  We want to get `dp(1, n)` before getting that, we need all subproblems with span < n

    ```python
    mem = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    for span in range(1, n + 1):
        for j in range(span, n + 1):
            i = j - span + 1
            if span == 0:
                # base case
            elif span == 1:
                # base case
            else:
                mem[i][j] = #...
                `
    ```

    