# Native Coroutine

## Awaitable

We say that an object is an **awaitable** object if it can be used in an `await`expression. Many asyncio APIs are designed to accept awaitables.

There are three main types of *awaitable* objects: **coroutines**, **Tasks**, and **Futures**.

### `Coroutine`

Use `async def ` to define coroutine

### `class asyncio.Task(coro, *, loop=None, name=None)`

*   *Tasks* are used to schedule coroutines *concurrently*.

*   When a coroutine is wrapped into a *Task* with functions like [`asyncio.create_task()`](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-task.html#asyncio.create_task) the coroutine is automatically scheduled to run soon:

    ```python
    import asyncio
    
    async def nested():
        return 42
    
    async def main():
        # Schedule nested() to run soon concurrently
        # with "main()".
        task = asyncio.create_task(nested())
    
        # "task" can now be used to cancel "nested()", or
        # can simply be awaited to wait until it is complete:
        await task
    
    asyncio.run(main())
    ```

*   `.cancel(msg=None)`

### `asyncio.Future`: 

*   A [`Future`](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-future.html#asyncio.Future) is a special **low-level** awaitable object that represents an **eventual result** of an asynchronous operation.

*   Super-class: `awaitable`
*   `result()`: return the result of the Future.
    *   If it's done and has a result set by `set_result()`, the result value is returned
    *    If it's done, and has an exception, it raises.
    *   If the future has been cancelled, it raises `CancelledError`
    *   If its result isn't yet available, it raises `InvalidStateError`
*   `exception()`: return the exception
*   `set_result(result)` `set_exception(exception)`: mark the future done and set its result/exception
*   `add_done_callback(callable, *, context=None)`: it is called with the Future object as its only argument
*   `get_loop()`: return the event loop the Future object is bound to

## Important methods

### Running

*   `asyncio.run`(*coro*, ***, debug=False)
*   `asyncio.create_task`(*coro*, ***, *name=None*)

### Sleeping

*   *coroutine* `asyncio.sleep`(*delay*, *result=None*, ***, *loop=None*)
    *   If *result* is provided, it is returned to the caller when the coroutine completes
    *   `sleep()` always suspends the current task, allowing other tasks to run.

### Running tasks concurrently

*   *awaitable* `asyncio.gather`(**aws*, *loop=None*, *return_exceptions=False*)
    *   Run [awaitable objects](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-task.html#asyncio-awaitables) in the *aws* sequence *concurrently*.
    *   If all awaitables are completed successfully, the result is an aggregate list of returned values. The order of result values corresponds to the order of awaitables in *aws*.
    *   If *return_exceptions* is `False` (default), the first raised exception is immediately propagated to the task that awaits on `gather()`. Other awaitables in the *aws* sequence **won’t be cancelled** and will continue to run.
    *   If *return_exceptions* is `True`, exceptions are treated the same as successful results, and aggregated in the result list.
    *   If any Task or Future from the *aws* sequence is *cancelled*, it is treated as if it raised [`CancelledError`](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-exceptions.html#asyncio.CancelledError) – the `gather()` call is **not** cancelled in this case. This is to prevent the cancellation of one submitted Task/Future to cause other Tasks/Futures to be cancelled.

### Timeouts

*   *coroutine* `asyncio.wait_for`(*aw*, *timeout*, ***, *loop=None*)

    *   Wait for the *aw* [awaitable](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-task.html#asyncio-awaitables) to complete with a timeout.
    *   If a timeout occurs, it **cancels** the task and raises [`asyncio.TimeoutError`](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-exceptions.html#asyncio.TimeoutError).

*   *coroutine* `asyncio.wait`(*aws*, ***, *loop=None*, *timeout=None*, *return_when=ALL_COMPLETED*)

    *   Run [awaitable objects](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-task.html#asyncio-awaitables) in the *aws* iterable concurrently and block until the condition specified by *return_when*
    *   The *aws* iterable must not be empty
    *   Returns two sets of Tasks/Futures: `(done, pending)`.

    Usage:

    ```python
    done, pending = await asyncio.wait(aws)
    ```

    *   If any awaitable in *aws* is a coroutine, it is automatically scheduled as a Task. Passing coroutines objects to `wait()` directly is deprecated as it leads to [confusing behavior](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-task.html#asyncio-example-wait-coroutine).

*   `asyncio.as_completed`(*aws*, ***, *loop=None*, *timeout=None*)

    Run [awaitable objects](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-task.html#asyncio-awaitables) in the *aws* iterable concurrently. Return an iterator of coroutines. Each coroutine returned can be awaited to get the earliest next result from the iterable of the remaining awaitables.

### Running in Threads

*   *coroutine* `asyncio.to_thread`(*func*, */*, **args*, ***kwargs*)

    *   This coroutine function is primarily intended to be used for executing IO-bound functions/methods that would otherwise block the event loop if they were ran in the main thread

        ```python
        def blocking_io():
            print(f"start blocking_io at {time.strftime('%X')}")
            # Note that time.sleep() can be replaced with any blocking
            # IO-bound operation, such as file operations.
            time.sleep(1)
            print(f"blocking_io complete at {time.strftime('%X')}")
        
        async def main():
            print(f"started main at {time.strftime('%X')}")
        
            await asyncio.gather(
                asyncio.to_thread(blocking_io),
                asyncio.sleep(1))
        
            print(f"finished main at {time.strftime('%X')}")
        
        
        asyncio.run(main())
        
        # Expected output:
        #
        # started main at 19:50:53
        # start blocking_io at 19:50:53
        # blocking_io complete at 19:50:54
        # finished main at 19:50:54
        ```

    Directly calling blocking_io() in any coroutine would block the event loop for its duration, resulting in an additional 1 second of run time. Instead, by using asyncio.to_thread(), we can run it in a separate thread without blocking the event loop.

### Scheduling from other Threads

-   `asyncio.run_coroutine_threadsafe`(*coro*, *loop*)
    -   This function is meant to be called from a different OS thread than the one where the event loop is running. 

## Streams

Streams are high-level async/await-ready primitives to work with network connections. Streams allow sending and receiving data without using callbacks or low-level protocols and transports.

-   `coroutine asyncio.open_connection`(*host=None*, *port=None*, ***, *loop=None*, *limit=None*, *ssl=None*, *family=0*, *proto=0*, *flags=0*, *sock=None*, *local_addr=None*, *server_hostname=None*, *ssl_handshake_timeout=None*)

    -   Establish a network connection and return a pair of `(reader, writer)` objects.
    -   The returned *reader* and *writer* objects are instances of [`StreamReader`](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-stream.html#asyncio.StreamReader) and [`StreamWriter`](dfile:///Users/khang306/Library/Application Support/Dash/DocSets/Python_3/Python 3.docset/Contents/Resources/Documents/doc/library/asyncio-stream.html#asyncio.StreamWriter) classes.

-   `coroutine asyncio.start_server`(*client_connected_cb*, *host=None*, *port=None*, ***, *loop=None*, *limit=None*, *family=socket.AF_UNSPEC*, *flags=socket.AI_PASSIVE*, *sock=None*, *backlog=100*, *ssl=None*, *reuse_address=None*, *reuse_port=None*, *ssl_handshake_timeout=None*, *start_serving=True*)

    Start a socket server.

## Subprocess

```python
import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

asyncio.run(run('ls /zzz'))
```

```python
async def main():
    await asyncio.gather(
        run('ls /zzz'),
        run('sleep 1; echo "hello"'))

asyncio.run(main())
```

```python
import asyncio
import sys

async def get_date():
    code = 'import datetime; print(datetime.datetime.now())'

    # Create the subprocess; redirect the standard output
    # into a pipe.
    proc = await asyncio.create_subprocess_exec(
        sys.executable, '-c', code,
        stdout=asyncio.subprocess.PIPE)

    # Read one line of output.
    data = await proc.stdout.readline()
    line = data.decode('ascii').rstrip()

    # Wait for the subprocess exit.
    await proc.wait()
    return line

date = asyncio.run(get_date())
print(f"Current date: {date}")
```

## Queues

```python
import asyncio
import random
import time


async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        await asyncio.sleep(sleep_for)

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f"{name} has slept for {sleep_for:.2f} seconds")


async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for _ in range(20):
        sleep_for = random.uniform(0.05, 1.0)
        total_sleep_time += sleep_for
        queue.put_nowait(sleep_for)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f"worker-{i}", queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print("====")
    print(f"3 workers slept in parallel for {total_slept_for:.2f} seconds")
    print(f"total expected sleep time: {total_sleep_time:.2f} seconds")


asyncio.run(main())

```

