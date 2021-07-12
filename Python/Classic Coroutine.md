# Coroutine

*   3 Types of coroutine
    *   classic coroutine: 
        *   via `my_coro.send(data)`
        *   using `yield`
        *   Delegate to other classic coroutine using `yield from`
    *   Generator-based coroutines
        *   A generator function decorated with `@types.coroutine`
        *   compatible with `await` keyword, intoroduced in Python3.5
    *   Native coroutines
        *   defined with `async def`
        *   using `await` to delegate to another native coroutine or generator-based coroutine

## Coroutine via enhanced generator

An example:

```python
def simple_coroutine():
    print('-> coroutine started')
    x = yield
    print('-> coroutine received', x)
>>> my_coro = simple_coroutine()
>>> next(my_coro)
>>> my_coro.send(42)
```

* States of coroutine:

    * 'GEN_CREATED'
    * 'GEN_RUNNING'
    * 'GEN_SUSPENDED'
    * 'GEN_CLOSED'

* Something to notice

    >   1.   .send can only be invoked when in 'GEN_SUSPENDED' state
    >   2.  in the `yield` sentense: `b = yield a`, the code on the right of `=` happens before the valuation of `b`

## Decorator to prime coroutine

```python
from funtctools import wraps

def coroutine(func):
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer
```

## End coroutine and exception handling

*   `coroutine.throw(type[, value[, traceback]])`: manually throw an specific exception in coroutine, if it's not handled, it will throw.
*   `coroutine.close()`: throw an GeneratorExit exception

## Let Coroutine return value



```python
def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return (count, average)
```

*   When we send None to the coroutine, it will raise `StopIteration`, and its value will be the return value.

## Use `yield from` to channel generators

```python
def delegate_gen():
    x = yield from subgen()
```

### Behavior of `yield from`

-   Any values that the subgenerator yields are passed directly to the caller of the delegating generator (i.e., the client code).
-   Any values sent to the delegating generator using `send()` are passed directly to the subgenerator. If the sent value is `None`, the subgenerator’s `__next__()` method is called. If the sent value is not `None`, the subgenerator’s `send()` method is called. If the call raises `StopIteration`, the delegating generator is resumed. Any other exception is propagated to the delegating generator.
-   `return expr` in a generator (or subgenerator) causes `StopIteration(expr)` to be raised upon exit from the generator.
-   The value of the `yield from` expression is the first argument to the `StopIteration` exception raised by the subgenerator when it terminates.

*   **the value that's sent-in will be passed along `yield from` and stops at `yield` sentence**

>   e.g. 
>
>   ```python
>   def grouper(results, key):
>      while True:
>       results[key] = yield from averager()
>   
>   def main(data):
>       results = {}
>       for key, values in data.items():
>           group = grouper(results, key)
>           next(group)
>           for value in values:
>               grouper.send(value)
>           grouper.send(None)0 
>   ```



## Use case: Discrete Event Simulation

```python
Event = collections.namedtuple('Event', 'time proc action')

def taxi_process(ident, trips, start_time=0):  
    """Yield to simulator issuing event at each state change"""
    time = yield Event(start_time, ident, 'leave garage')  
    for i in range(trips):  
        time = yield Event(time, ident, 'pick up passenger')  
        time = yield Event(time, ident, 'drop off passenger')  

    yield Event(time, ident, 'going home')

class Simulator:    
    def __init__(self, procs_map):        
        self.events = queue.PriorityQueue()        
        self.procs = dict(procs_map)    
    def run(self, end_time):          
        """Schedule and display events until time is up"""        
        # schedule the first event for each cab        
        for _, proc in sorted(self.procs.items()):              
            first_event = next(proc)              
            self.events.put(first_event)          
            # main loop of the simulation        
            sim_time = 0         
            while sim_time < end_time:              
                if self.events.empty():                  
                    print('*** end of events ***')                
                    break            
                current_event = self.events.get()              
                sim_time, proc_id, previous_action = current_event              
                print('taxi:', proc_id, proc_id * '   ', current_event)             
                active_proc = self.procs[proc_id]             
                next_time = sim_time + compute_duration(previous_action)              
                try:               
                    next_event = active_proc.send(next_time)            
                except StopIteration:               
                    del self.procs[proc_id]             
                else:                
                    self.events.put(next_event)         
            else:              
                msg = '*** end of simulation time: {} events pending ***'
        
taxis = {0: taxi_process(ident=0, trips=2, start_time=0),             
         1: taxi_process(ident=1, trips=4, start_time=5),             
         2: taxi_process(ident=2, trips=6, start_time=10)}    
sim = Simulator(taxis)
```

