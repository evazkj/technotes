# Wait and Notify

*   Example:

    ```java
    class TaskQueue {
        Queue<String> queue = new LinkedList<>();
    
        public synchronized void addTask(String s) {
            this.queue.add(s);
        }
    
        public synchronized String getTask() {
            while (queue.isEmpty()) {
            }
            return queue.remove();
        }
    }
    ```

    the while loop will never end because it takes the "this" as lock and no one else can `addtask`

    *   Use wait and notify to release lock

    ```java
    public synchronized String getTask() {
        while (queue.isEmpty()) {
            // 释放this锁:
            this.wait();
            // 重新获取this锁
        }
        return queue.remove();
    }
    public synchronized void addTask(String s) {
        this.queue.add(s);
        this.notify(); // 唤醒在this锁等待的线程
    }
    
    // we can also use this.notifyAll()
    ```

    `notify()` will wake one thread, while `notifyAll()` will wake up all threads that are waiting.

*   假设我们有三个thread在从poll中getTask，一开始他们三个都在wait。当我们addTask之后，三个thread只有一个会从wait中醒来读取task。并且在程序结束后释放。