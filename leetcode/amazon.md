# Amazon

## 1229. Meeting Scheduler

Given the availability time slots arrays `slots1` and `slots2` of two people and a meeting duration `duration`, return the **earliest time slot** that works for both of them and is of duration `duration`.

If there is no common time slot that satisfies the requirements, return an **empty array**.

**Example 1:**

```
Input: slots1 = [[10,50],[60,120],[140,210]], slots2 = [[0,15],[60,70]], duration = 8
Output: [60,68]
```

**Example 2:**

```
Input: slots1 = [[10,50],[60,120],[140,210]], slots2 = [[0,15],[60,70]], duration = 12
Output: []
```

很容易想到sort之后two pointer的方法。

优化：

	1. 如果我们一开始就找到了，那么对于后续interval的sort就浪费了，我们可以使用更经济的heap
 	2. 所有小于duration的timeslot我们都不需要考虑，可以filter掉
 	3. 如果建立两个heap，我们需要考虑从哪个heap pop的问题，代码比较长。我们可以考虑建立一个heap，将heap中两两相邻元素比对，只要有overlap，那肯定来自不同的人

```python
heap = list(filter(lambda intv: intv[1] - intv[0] >= duration, slots1 + slots2))
heapq.heapify(heap)
while len(heap) > 1:
    s1, e1 = heapq.heappop(heap)
    s2, e2 = heap[0]
    ss, ee = max(s1, s2), min(e1, e2) //不用比较是否有overlap，那种情况下ss会大于ee
    if ee - ss >= duration:
        return [ss, ss + duration]
    return []
```

## 1288. Remove Covered Intervals

Given a list of `intervals`, remove all intervals that are covered by another interval in the list.

Interval `[a,b)` is covered by interval `[c,d)` if and only if `c <= a` and `b <= d`.

After doing so, return *the number of remaining intervals*.

容易想到要sort，然后根据前面interval的end来确定当前的interval是否是covered，为了达到这个目的，我们不仅要sort start，也要反向sort end。 Intervals.sort(key = lambda x: [x[0], -x[1]])