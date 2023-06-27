import multiprocessing
import time

def cpu_bound(number):
    return sum(i * i for i in range (number))

def find_sums_sync(numbers):
    for number in numbers:
        cpu_bound(number)
def find_sums_multiprocessing(numbers):
    with multiprocessing.Pool() as pool:
        pool.map(cpu_bound, numbers)

if __name__ == '__main__':
    numbers = [5_000_000 + x for x in range(20)]

    start_time = time.time()
    find_sums_sync(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds for synchronous")

    start_time = time.time()
    find_sums_multiprocessing(numbers)
    duration = time.time() - start_time
    print(f"Duration {duration} seconds for multiprocessing")