# Concurrency models in Python

threading, multi-processing, and asyncio

## Processes, threads and GIL

*   Each instance of the Python interpreter is a process. You can start additional Python processes using the `multiprocessing` or `concurrent.futures` libraries, Python’s `subprocess` library is designed to launch processes to run external programs, regardless of the languages used to write them.
*   The Python interpreter uses a single thread to run the user’s program and the memory garbage collector. You can start additional Python threads using the `threading` or `concurrent.futures` libraries.
*   To prevent a Python thread from holding the GIL indefinitely, Python’s bytecode interpreter pauses the current Python thread every 5ms by default, releasing the GIL. The thread can then try to reacquire the GIL, but if there are other threads waiting for it, the OS scheduler may pick one of them to proceed.
*   Every Python standard library function that makes a syscall[4](https://learning.oreilly.com/library/view/Fluent+Python,+2nd+Edition/9781492056348/ch19.html#idm46605847881624) releases the GIL. This includes all functons that perform disk I/O, network I/O, and `time.sleep()`. Many CPU-intensive functions in the NumPy/SciPy libraries, as well as the compressing/decompressing functions from the `zlib` and `bz2` modules also release the GIL.[5](https://learning.oreilly.com/library/view/Fluent+Python,+2nd+Edition/9781492056348/ch19.html#idm46605847878440)
*   Extensions that integrate at the Python/C level can also launch other non-Python threads that are not affected by the GIL. Such GIL-free threads generally cannot change Python objects, but they can read from and write to the memory underlying `array.array` or NumPy arrays, which support the [buffer protocol](https://www.python.org/dev/peps/pep-3118/).
*   The effect of the GIL on network programming with Python threads is relatively small, because the I/O functions release the GIL. each individual thread spends a lot of time waiting anyway, so their execution can be interleaved without major impact on the overall throughput
*   To run CPU-intensive Python code on multiple cores, you must use multiple Python processes



## Concurrency Hello world

Suppose we are working on a spinner line. 

```python
import itertools
import time
from threading import Thread, Event


def spin(msg: str, done: Event) -> None:
    for char in itertools.cycle(r"\|/-"):
        status = f"\r{char} {msg}"
        print(status, end="", flush=True)
        if done.wait(0.1):
            break
    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


def slow() -> int:
    time.sleep(3)
    return 42
```

### Spinner with Threading

use `threading.Event` to communicate

```python
def supervisor() -> int:
    done = Event()
    spinner = Thread(target=spin, args=("thinking!", done))
    print(f"spinner object: {spinner}")
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result


def main() -> None:
    result = supervisor()
    print(f"Answer: {result}")
```

### Spinner with Multi-processing

```python
import itertools
import time
from multiprocessing import Process, Event  
from multiprocessing import synchronize     

def spin(msg: str, done: synchronize.Event) -> None:  

# [snip] the rest of spin and slow functions are unchanged from spinner_thread.py

def supervisor() -> int:
    done = Event()
    spinner = Process(target=spin,               
                      args=('thinking!', done))
    print(f'spinner object: {spinner}')          
    spinner.start()
    result = slow()
    done.set()
    spinner.join()
    return result

# [snip] main function is unchanged as well
```

### Spinner with asyncio

It is the job of OS schedulers to allocate CPU time to drive threads and processes. In contrast, coroutines are driven by an application-level event loop that manages a queue of pending coroutines, drives them one by one, monitors events triggered by I/O operations initiated by coroutines, and passes control back to the corresponding coroutine when each event happens. 

```python
import asyncio
import itertools

async def spin(msg: str) -> None:  
    for char in itertools.cycle(r'\|/-'):
        status = f'\r{char} {msg}'
        print(status, flush=True, end='')
        try:
            await asyncio.sleep(.1)  
        except asyncio.CancelledError:  
            break
    blanks = ' ' * len(status)
    print(f'\r{blanks}\r', end='')

async def slow() -> int:
    await asyncio.sleep(3)  
    return 42

def main() -> None:  
    result = asyncio.run(supervisor())  
    print(f'Answer: {result}')

async def supervisor() -> int:  
    spinner = asyncio.create_task(spin('thinking!'))  
    print(f'spinner object: {spinner}')  
    result = await slow()  
    spinner.cancel()  
    return result

if __name__ == '__main__':
    main()
```



#### three ways to run a coroutine

1.  `asyncio.run(coro())`: **Called from a regular function** to drive a coroutine object which usually is the entry point for all the asynchronous code in the program, like the `supervisor` in this example. This call blocks until the body of `coro` returns. The return value of the `run()` call is whatever the body of `coro` returns.
2.  `asyncio.create_task(coro())`: **Called from a coroutine to schedule another coroutine to execute eventually.** This call does not suspend the current coroutine. It returns a `Task` instance, an object that wraps the coroutine object and provides methods to control and query its state.
3.  `await coro()`: **Called from a coroutine** to transfer control to the coroutine object returned by `coro()`. This suspends the current coroutine until the body of `coro` returns. The value of the await expression is whatever body of `coro` returns.

#### Other operations

1.  Use `await asyncio.sleep(.1)` instead of `time.sleep(.1)`, to pause **without blocking other coroutines**. 

    >   `asyncio.sleep`  is actually a mechanism to yields control back to the event loop, which can drive other pending coroutines

2.  `asyncio.CancelledError` is raised when the `cancel` method is called on the `Task` controlling this coroutine. Time to exit the loop.

### comparison of coroutine and threading

*   They are roughly equivalent
*   An `asyncio.Task` drives a coroutine object, and a `Thread` invokes a callable.
*   A Coroutine yields control explicitly with the `await` keyword
*   You don’t instantiate `Task` objects yourself, you get them by passing a coroutine to `asyncio.create_task(…)`.
*   There’s no API to terminate a thread from the outside; instead, you must send a signal—like setting the `done` `Event` object. For tasks, there is the `Task.cancel()` instance method, which raises `CancelledError` at the `await` expression where the coroutine body is currently suspended.

#### Pros of Coroutine:

*   In thread programming, it is challenging to reason about the program because the scheduler can interrupt a thread at any time.You must remember to hold locks to protect the critical sections of your program, to avoid getting interrupted in the middle of a multistep operation—which could leave data in an invalid state
*   With coroutines, your code is protected against interruption by default. You must explicitly `await` to let the rest of the program run. Instead of holding locks to synchronize the operations of multiple threads, coroutines are “synchronized” by definition: only one of them is running at any time.
*   When you want to give up control, you use `await` to yield control back to the scheduler. That’s why it is possible to safely cancel a coroutine: by definition, a coroutine can only be cancelled when it’s suspended at an `await` expression, so you can perform cleanup by handling the `CancelledError` exception.

## A homegrown process pool

Suppose we want to check the primality of 20 integers between 2 and 2^35

```python
import sys
from time import perf_counter
from typing import NamedTuple
from multiprocessing import Process, SimpleQueue, cpu_count  
from multiprocessing import queues  

from primes import is_prime, NUMBERS

class PrimeResult(NamedTuple):  
    n: int
    prime: bool
    elapsed: float

JobQueue = queues.SimpleQueue[int]  
ResultQueue = queues.SimpleQueue[PrimeResult]  

def check(n: int) -> PrimeResult:  
    t0 = perf_counter()
    res = is_prime(n)
    return PrimeResult(n, res, perf_counter() - t0)

def worker(jobs: JobQueue, results: ResultQueue) -> None:  
    while n := jobs.get():  
        results.put(check(n))  
```

>   **Poison pill** design pattern:  in the worker function, it loops indefinitely while taking items from a queue and processing them. The loop ends when the queue produces a sentinel.(poison pill)

```python
def main() -> None:
    if len(sys.argv) < 2:  
        workers = cpu_count()
    else:
        workers = int(sys.argv[1])

    print(f'Checking {len(NUMBERS)} numbers with {workers} processes:')

    jobs: JobQueue = SimpleQueue() 
    results: ResultQueue = SimpleQueue()
    t0 = perf_counter()

    for n in NUMBERS:  
        jobs.put(n)

    for _ in range(workers):
        proc = Process(target=worker, args=(jobs, results))  
        proc.start()  
        jobs.put(0)  # Put one sentinel for each worker

    while True:
        n, prime, elapsed = results.get()  
        label = 'P' if prime else ' '
        print(f'{n:16}  {label} {elapsed:9.6f}s')  
        if jobs.empty():  # Ok to do so, because the last job in the queue is sentinel
            break

    elapsed = perf_counter() - t0
    print(f'Total time: {elapsed:.2f}s')

if __name__ == '__main__':
    main()
```

>   The sentinel is very important, if not, it is possible that the jobs is empty but a worker is still running.

## The Big picture

*   The free lunch is over: the trend of software getting faster with no additional developer effort because CPUs were executing sequential code faster, year after year. Since 2004, that is no longer true: clock speeds and execution optimizations reached a plateau, and now any significant increase in performance must come from leveraging multiple cores or hyper-threading, advances that only benefit code that is written for concurrent execution.
*   Python’s story started in the early 1990’s, when CPUs were still getting exponentially faster at sequential code execution.The GIL makes the interpreter faster when running on a single core, and its implementation simpler.The GIL also makes it easier to write simple extensions through the Python/C API.

### System Administration

*   Python is widely used to manage large fleets of servers, routers, load balancers, network-attached storage (NAS). It’s also a leading option in software-defined networking (SDN) and ethical hacking. 
*   There is also a growing number of libraries for system administration supporting coroutines and asyncio. In 2016, Facebook’s Production Engineering team reported: “We are increasingly relying on AsyncIO, which was introduced in Python 3.4, and seeing huge performance gains as we move codebases away from Python 2.”

### Data science

*   Jupiter: integrated vis ZeroMQ, Julia, Python, R, Tool [Bokeh](https://docs.bokeh.org/en/latest/index.html)
*   Dask: A parallel computing library that can farm out work to local processes or clusters of machines
*   15-minute [demo](https://www.youtube.com/watch?v=ods97a5Pzw0&ab_channel=MatthewRocklin) which Matthew Rocklin—a maintainer of the project—shows Dask crunching data on 64 cores distributed in 8 EC2 machines on AWS

### Server-side development

*   Application caches: memcached, Varnish, Redis
*   Relational DB: PostgreSQL, mySQL
*   document databases: Apache CouchDB, MongoDB
*   Full-test indexes: Elasticsearch, Apache Solr
*   Messaage Queues: RabibitMQ, Redis

### WSGI Application Servers

The Web Server Gateway Interface: is a standard API for a Python framework or application to receive requests from a HTTP server and send responses to it.

The best known application servers in Python Web projects are:

-   [mod_wsgi](https://modwsgi.readthedocs.io/en/master/);
-   [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/);[21](https://learning.oreilly.com/library/view/Fluent+Python,+2nd+Edition/9781492056348/ch19.html#idm46605845273272)
-   [gunicorn](https://gunicorn.org/);
-   [NGINX Unit](https://unit.nginx.org/).

### Distributed task queues

[Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html) and [RQ](https://python-rq.org/) are the best known Open Source task queues with Python APIs. Cloud providers also offer their own proprietary task queues.

These products wrap a message queue and offer a high-level API for delegating tasks to workers, possibly running on different machines.

|      Feature       | Threads | Async | Multiprocessing | PEP 554  | Ideal CSP |
| :----------------: | :-----: | :---: | :-------------: | :------: | :-------: |
| Parallel execution |   No    |  No   |       Yes       |    ?     |    Yes    |
| Shared raw memory  |   Yes   |  Yes  |     Limited     | Limited? |    No     |
|   Shared objects   |   Yes   |  Yes  |       No        |   No?    |    No     |
|      Overhead      | Medium  |  Low  |      High       |    ?     |     —     |

### Further reading

*    [An Intro to Threading in Python](https://realpython.com/intro-to-python-threading/) by Jim Anderson is a good first read. Doug Hellmann has a chapter titled *Concurrency with Processes, Threads, and Coroutines* in his [site](https://pymotw.com/3/concurrency.html) and book: [Python 3 Standard Library by Example](https://www.pearson.com/us/higher-education/program/Hellmann-Python-3-Standard-Library-by-Example-The/PGM328871.html) (Addison-Wesley, 2017).
*   Brett Slatkin’s [*Effective Python, Second Edition*](http://www.effectivepython.com/) (Addison-Wesley, 2019), David Beazley’s *Python Essential Reference, 4th Edition* (Addison-Wesley Professional, 2009), and Martelli, Ravenscroft & Holden’s *Python in a Nutshell*, 3E (O’Reilly) are other general Python references with significant coverage of `threading` and `multiprocessing`. The vast `multiprocessing` official documention includes useful advice in its [Programming guidelines](https://docs.python.org/3/library/multiprocessing.html#programming-guidelines) section.
*   In [*Advanced Python Development*](https://www.apress.com/gp/book/9781484257920) (Apress, 2020), author Matthew Wilkes is a rare book that includes short examples to explain concepts, while also showing how to build a realistc application ready for production: a data agregator, similar to DevOps monitoring systems or IoT data collectors for distributed sensors.
*   If you want to learn the hard way how difficult it is to reason about threads and locks—without risking your job—try the exercises in Alen Downey’s workbook [*The Little Book of Semaphores*](https://greenteapress.com/wp/semaphores/). 
*    [*High Performance Python, 2nd Edition*](https://learning.oreilly.com/library/view/high-performance-python/9781492055013/) and [*Parallel Programming with Python*](https://www.packtpub.com/product/parallel-programming-with-python/9781783288397).
*   “Instagram currently features the world’s largest deployment of the Django web framework, which is written entirely in Python.” That’s the opening sentence of the blog post [Web Service Efficiency at Instagram with Python](https://instagram-engineering.com/web-service-efficiency-at-instagram-with-python-4976d078e366) written by Min Ni—a software engineer at Instagram.
*   [*Architecture Patterns with Python: Enabling Test-Driven Development, Domain-Driven Design, and Event-Driven Microservices*](https://www.oreilly.com/library/view/architecture-patterns-with/9781492052197/) by Harry Percival & Bob Gregory (O’Reilly, 2020) presents architectural patterns for Python server-side applications. The authors also made the book freely available online at [cosmicpython.com](https://www.cosmicpython.com/).
*   Two elegant and easy to use libraries for parallelizing tasks over processes are [*lelo*](https://pypi.python.org/pypi/lelo) by João S. O. Bueno and [*python-parallelize*](http://bit.ly/1HGtF6Q) by Nat Pryce.
*   The actor model of concurrent programming underlies the highly scalable Erlang and Elixir languages,as well as the Akka framework for Scala and Java.If you want to try out the actor model in Python, check out thethe Thespian and Pykka libraries.