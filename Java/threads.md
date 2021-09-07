*   Thread interruption

    ```java
    // Use InterruptedException in thread to detect whether it has been interrupted
    try {
        Thread.sleep(100);
    } catch (InterruptedException e) {
        break;
    }
    ```

*   Daemon thread: JVM will not care if Deamon thread has finished, so it's perfect for some infinite loop tasks. 

    ```java
    Thread t = new MyThread();
    t.setDaemon(true);
    t.start();
    ```

*   Synchronized lock: like Mutex, but the actual "locl" doesn't have to be a specific mutex instance, it can be any instance.

```java
public class Main {
    public static void main(String[] args) throws Exception {
        var add = new AddThread();
        var dec = new DecThread();
        add.start();
        dec.start();
        add.join();
        dec.join();
        System.out.println(Counter.count);
    }
}

class Counter {
    public static final Object lock = new Object();
    public static int count = 0;
}

class AddThread extends Thread {
    public void run() {
        for (int i=0; i<10000; i++) {
            synchronized(Counter.lock) {
                Counter.count += 1;
            }
        }
    }
}

class DecThread extends Thread {
    public void run() {
        for (int i=0; i<10000; i++) {
            synchronized(Counter.lock) {
                Counter.count -= 1;
            }
        }
    }
}
```

*   A better way to lock is to wrap it into the object:

    ```java
    public class Counter {
        private int count = 0;
    
        public void add(int n) {
            synchronized(this) {
                count += n;
            }
        }
    
        public void dec(int n) {
            synchronized(this) {
                count -= n;
            }
        }
    
        public int get() {
            return count;
        }
    }
    
    // not we lock the Counter instance, it is equivalent to:
    public synchronized void add(int n) { // 锁住this
        count += n;
    } // 解锁
    ```

    