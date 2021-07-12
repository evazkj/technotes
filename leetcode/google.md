# Google

##  1610. Maximum Number of Visible Points

You are given an array `points`, an integer `angle`, and your `location`, where `location = [posx, posy]` and `points[i] = [xi, yi]` both denote **integral coordinates** on the X-Y plane.

Initially, you are facing directly east from your position. You **cannot move** from your position, but you can **rotate**. In other words, `posx` and `posy` cannot be changed. Your field of view in **degrees** is represented by `angle`, determining how wide you can see from any given view direction. Let `d` be the amount in degrees that you rotate counterclockwise. Then, your field of view is the **inclusive** range of angles `[d - angle/2, d + angle/2]`.

```python
class Solution:
    def visiblePoints(self, points: List[List[int]], angle: int, location: List[int]) -> int:
        angles = [ ]
        always_visible = 0
        x1, y1 = location
        for x2, y2 in points:
            # we always need to include this point, irrespective of the angle
            if x1== x2 and y2 == y1:
                always_visible +=1
            else:
                ang_rad = math.atan2((y2-y1),(x2-x1))  
                angles.append(math.degrees(ang_rad))
        angles.sort()
        
        maxcount = 0
        l, r = 0, 0
        n = len(angles)
        
        while l < len(angles):
            while r != l + n and (angles[r % n] - angles[l]) % 360 <= angle:
                r += 1
            maxcount = max(maxcount, (r - l))
            l += 1
        return maxcount + always_visible
```

这题注意corner case的处理。

1.  原点always visible
2.  angle为0时，在同一条直线上的点都得算

另外，这题启发了circular 2pointer的思路。移动l,r的时候，我们保持r单调increase，在取值的时候再做mod，用 r  != l + n来表示不能套圈。

## 295. Find Median from Data Stream

这道题很容易想到用2 heap的方法

Follow-up: 

1.  If the number are all from [0-100]? use buckets
2.  What if the number of data points is extremely large? 可以用reservoir sampling来维持一个representative set，然后在这个set里找median
3.  还可以使用BST，node保存左右树的node数量。但是要写一个self balanced tree。

## 519. Random Flip Matrix

You are given the number of rows `n_rows` and number of columns `n_cols` of a 2D binary matrix where all values are initially 0. Write a function `flip` which chooses a 0 value [uniformly at random](https://en.wikipedia.org/wiki/Discrete_uniform_distribution), changes it to 1, and then returns the position `[row.id, col.id]` of that value. Also, write a function `reset` which sets all values back to 0. **Try to minimize the number of calls to system's Math.random()** and optimize the time and space complexity.

这道题一种思路是用vector维持一个blacklist，然后用findTheKthMissingElement的方法来random access，这样的time是O(log(BlacklistSize)), 不够快

另一种思路是建设一个whitelist，因为我们知道剩下的元素数量，所以我们可以将剩下的元素建立一个mapping。

  ```python
from random import randint
class Solution(object):

    def __init__(self, n_rows, n_cols):
        """
        :type n_rows: int
        :type n_cols: int
        """
        self.remain = n_rows * n_cols
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.mapping = dict()

    def flip(self):
        """
        :rtype: List[int]
        """
        rn = randint(0, self.remain - 1)
        if rn not in self.mapping: # 这个数字没有被选中过
            res = rn
        else:
            res = self.mapping[rn] 
        # 将后面的数字来填补之前的数字
        self.mapping[rn] = self.mapping.get(self.remain - 1, self.remain - 1)
        self.remain -= 1

        return (res // self.n_cols, res % self.n_cols)
        
     def reset(self):
        """
        :rtype: None
        """
        self.mapping = dict()
        self.remain = self.n_rows * self.n_cols
  ```

