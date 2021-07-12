from concurrent.futures import ThreadPoolExecutor
import time


def wait(seconds):
    time.sleep(seconds)
    return seconds * 2


def main():
    a = [1, 2, 3]
    with ThreadPoolExecutor() as exec:
        b = exec.map(wait, a)
    print(list(b))


if __name__ == "__main__":
    main()
