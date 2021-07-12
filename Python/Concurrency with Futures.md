# Concurrency with futures

The main features of the `concurrent.futures` package are the `ThreadPoolExecutor` and `ProcessPoolExecutor` classes, which implement an API for to submitting callables for execution in different threads or processes, respectively.



*   Using `ThreadPoolExecutor`

```python
from concurrent import futures

from flags import save_flag, get_flag, main  

def download_one(cc: str):  
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc

def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor:         
        res = executor.map(download_one, sorted(cc_list))  

    return len(list(res))                                  

if __name__ == '__main__':
    main(download_many)  
```

*   Since Python 3.4, there are two classes named `Future` in the standard library: `concurrent.futures.Future` and `asyncio.Future`. They serve the same purpose: an instance of either `Future` class represents a deferred computation that may or may not have completed. This is similar to the `Deferred` class in Twisted, the `Future` class in Tornado, and `Promise` in modern JavaScript.

*   `Future.done()`: nonblocking
*   `.add_done_callback()`: callback will be invoked with the future as the single argument when the future is done
*   `.result()`: if the future is not done, `f.result()` will block.