# classic problem

## 1631. Path With Minimum Effort

You are a hiker preparing for an upcoming hike. You are given `heights`, a 2D array of size `rows x columns`, where `heights[row][col]` represents the height of cell `(row, col)`. You are situated in the top-left cell, `(0, 0)`, and you hope to travel to the bottom-right cell, `(rows-1, columns-1)` (i.e., **0-indexed**). You can move **up**, **down**, **left**, or **right**, and you wish to find a route that requires the minimum **effort**.

A route's **effort** is the **maximum absolute difference** in heights between two consecutive cells of the route.

Return *the minimum **effort** required to travel from the top-left cell to the bottom-right cell.*

*   这是一道graph中，undirected weighted edge，寻找最佳路径的题。此scenario是在Dijkstra的范畴，虽然不完全一样，但是有个共同点就是route weight只会单调上升。所以通过priority queue的方法来计算是可以的。

```python
class Solution:
    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])
        dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        visited = [[False for _ in range(n)] for _ in range(m)]
        
        visiting = [(0, 0, 0)]
        while visiting:
            effort, x, y = heapq.heappop(visiting)
            if visited[x][y]:
                continue
            if x == m - 1 and y == n - 1:
                return effort
                
            visited[x][y] = True
            for dx, dy in dirs:
                xx, yy = x + dx, y + dy
                if 0 <= xx < m and 0 <= yy < n:
                    new_effort = max(effort, abs(heights[x][y] - heights[xx][yy]))
                    heapq.heappush(visiting, (new_effort, xx, yy))
```

*   Time Complexity : $O(m⋅nlog(m⋅n))$, where *m* is the number of rows and n*n* is the number of columns in matrix heights. It will take $O(m⋅n)$ time to visit every cell in the matrix. The priority queue will contain at most $mn$ cells, so it will take $O(log(m⋅n))$ time to re-sort the queue after every adjacent cell is added to the queue. This given as total time complexiy as $O(m⋅nlog(m⋅n))$. 

*   这道题我们可以用贪心算法，类似于kruskal算法，找最小生成树。我们将所有edge找出，然后从小到大取出来，知道取出的edge使得原点和终点在同一个connected component之内。这种iterative的加入方法，很适合用union-find

    ```python
            m, n = len(heights), len(heights[0])
        	# flatten parent vector
            parent = list(range(m * n))
            edges = []
            for i, j in itertools.product(range(m), range(n)):
                if i + 1 < m:
                    edges.append((abs(heights[i][j] - heights[i + 1][j]), i * n + j, (i + 1)*n + j))
                if j + 1 < n:
                    edges.append((abs(heights[i][j] - heights[i][j + 1]), i * n + j, i*n + j + 1))
            heapq.heapify(edges)
            
            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return parent[x]
            
            def union(x1, x2):
                p1 = find(x1)
                p2 = find(x2)
                parent[p1] = p2
            
            while edges:
                e, node1, node2 = heapq.heappop(edges)
                union(node1, node2)
                if find(0) == find(m * n - 1):
                    return e
            return 0
    ```

    

