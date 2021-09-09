

# Facebook

## 426. Convert Binary Search Tree to Sorted Doubly Linked List

Convert a **Binary Search Tree** to a sorted **Circular Doubly-Linked List** in place.

```python
def treeToDoublyList(self, root: 'Node') -> 'Node':
    	# Stack solution
        stack = []
        node = root
        last, first = None, None
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            if last:
                last.right = node
                node.left = last
            else:
                first = node
            last = node
            node = node.right
        
        if not root:
            return None
        first.left = last
        last.right = first
        return first
        
        # recursion solution
        last, first = None, None
        def helper(node):
            nonlocal last, first
            if node:
                helper(node.left)
                if last:
                    last.right = node
                    node.left = last
                else:
                    first = node
                last = node
                helper(node.right)
        if not root:
            return None
        
        helper(root)
        first.left = last
        last.right = first
        return first
```

关键在于寻找一个编程的pattern：last和first

## 56. Merge Intervals

Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return *an array of the non-overlapping intervals that cover all the intervals in the input*.

**Example 1:**

```
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlaps, merge them into [1,6].
```

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals:
            return []
        
        res = []
        intervals.sort()
        i, j, n = 0, 0, len(intervals)
        
        while i < n:
            start = intervals[i][0]
            end = intervals[i][1]
            while j < n and intervals[j][0] <= end:
                end = max(end, intervals[j][1])
                j += 1
            res.append([start, end])
            i = j 
        return res
```

这题在于熟悉2pointer的书写模板

```python
while i < n:
    # init
    while j < n and (stop_condition):
        # do_something
        j += 1
    # do_somthing
    # update_i
```

## 76. Minimum Window Substring

Given two strings `s` and `t`, return *the minimum window in `s` which will contain all the characters in `t`*. If there is no such window in `s` that covers all characters in `t`, return *the empty string `""`*.

**Note** that If there is such a window, it is guaranteed that there will always be only one unique minimum window in `s`.

**Example 1:**

```
Input: s = "ADOBECODEBANC", t = "ABC"
Output: "BANC"
```

```python
from collections import Counter
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        window = Counter(t)
        num_missed = len(window)
        
        min_len = float(inf)
        res = ""
        queue = deque()
        i, j = 0, 0
        while i < len(s):
            while j < len(s) and num_missed > 0:
                ch = s[j]
                if ch in window:
                    queue.append(j)
                    window[ch] -= 1
                    if window[ch] == 0:
                        num_missed -= 1
                j += 1

            if j == len(s) and num_missed > 0:
                break
            
            while queue and num_missed == 0:
                # 先 update i or 先update res
                i = queue.popleft()
                if j - i < min_len:
                    min_len = j - i
                    res = s[i:j]
                ch = s[i]
                window[ch] += 1
                if window[ch] > 0:
                    num_missed += 1
        return res
```

## 1004 Max Consecutive Ones III

Given a binary array `nums` and an integer `k`, return *the maximum number of consecutive* `1`*'s in the array if you can flip at most* `k` `0`'s.

**Example 1:**

```
Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
Output: 6
Explanation: [1,1,1,0,0,1,1,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
```

**Example 2:**

```
Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
Output: 10
Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
```

*   思路：
    *   如果要flip，肯定是要讲成片的1连起来，否则没有意义，等于说我们flip的0也必须是连续的，所以可以想到用sliding window
    *   于是问题变成了：**找到一个最长的substring使得其中的0的数量不超过k个**
    *   假设我们用left,right来定义substring的两侧，活动的pattern是我们先动right，当constraint被违背了之后，再动left
    *   因为我们要最大的substring，所以这个window的size是只增不减的，也就是说我们发现0过多的时候我们只需要把size减小1，即left向右移动一格，而不用管left是不是在0上

```python

class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        # zero_pos = [i for i, num in enumerate(nums) if num == 0]
        # 
        # if len(zero_pos) <= k:
        #     return len(nums)
        # 
        # zero_pos = [-1] + zero_pos + [len(nums)]
        # 
        # if k == 0:
        #     return max((zero_pos[i] - zero_pos[i - 1] - 1) for i in range(1, len(zero_pos)))
        # 
        # max_len = 0
        # for i in range(1, len(zero_pos) - k):
        #     crt_len = zero_pos[i + k] - zero_pos[i - 1] - 1
        #     max_len = max(max_len, crt_len)
        # return max_len
        
        left = 0
        
        for right in range(len(nums)):
            if nums[right] == 0:
                k -= 1
            if k < 0:
                if nums[left] == 0:
                    k += 1
                left += 1
        return right - left + 1
```

## 1361.  Validate Binary Tree Nodes

You have `n` binary tree nodes numbered from `0` to `n - 1` where node `i` has two children `leftChild[i]` and `rightChild[i]`, return `true` if and only if **all** the given nodes form **exactly one** valid binary tree.

If node `i` has no left child then `leftChild[i]` will equal `-1`, similarly for the right child.

Note that the nodes have no values and that we only use the node numbers in this problem.

 

**Example 1:**

![img](https://assets.leetcode.com/uploads/2019/08/23/1503_ex1.png)

```
Input: n = 4, leftChild = [1,-1,3,-1], rightChild = [2,-1,-1,-1]
Output: true
```

*   此题的corner case很多。最简单的想法是先找到root，然后从root开始bfs，如果有环，返回False。最后检查是否所有节点都已经被遍历过。

    ```python
    from collections import deque
    class Solution:
        def validateBinaryTreeNodes(self, n: int, leftChild: List[int], rightChild: List[int]) -> bool:
            
            children = set(leftChild + rightChild)
            parents = set(range(n)) - children
            if len(parents) != 1:
                return False
            root = next(iter(parents))
            
            visited = [0 for _ in range(n)]
            queue = deque([root])
            
            while queue:
                node = queue.popleft()
                if visited[node]:
                    return False
                visited[node] = 1
                if leftChild[node] != -1:
                    queue.append(leftChild[node])
                if rightChild[node] != -1:
                    queue.append(rightChild[node])
                    
            return all(visited)
    ```

    

