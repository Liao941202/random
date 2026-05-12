import random
import time

# Generate 1M 16-bit integers
N = 1_000_000
MAX_VAL = 65536  # 2^16
data = [random.randint(0, MAX_VAL - 1) for _ in range(N)]

arr = data.copy()
t0 = time.perf_counter()
result_builtin = sorted(arr)
t1 = time.perf_counter()
time_builtin = t1 - t0

def counting_sort(arr, k):
    C = [0] * (k + 1)
    for x in arr:
        C[x] += 1
    for i in range(1, k + 1):
        C[i] += C[i - 1]
    B = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        B[C[arr[i]] - 1] = arr[i]
        C[arr[i]] -= 1
    return B

arr = data.copy()
t0 = time.perf_counter()
result_counting = counting_sort(arr, MAX_VAL - 1)
t1 = time.perf_counter()
time_counting = t1 - t0

def counting_sort_digit(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 256
    for x in arr:
        digit = (x >> exp) & 0xFF
        count[digit] += 1
    for i in range(1, 256):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        digit = (arr[i] >> exp) & 0xFF
        count[digit] -= 1
        output[count[digit]] = arr[i]
    return output

def radix_sort(arr):
    arr = counting_sort_digit(arr, 0)   # bits 0-7
    arr = counting_sort_digit(arr, 8)   # bits 8-15
    return arr

arr = data.copy()
t0 = time.perf_counter()
result_radix = radix_sort(arr)
t1 = time.perf_counter()
time_radix = t1 - t0

assert result_builtin == result_counting, "Counting Sort incorrect!"
assert result_builtin == result_radix, "Radix Sort incorrect!"

print(f"N = {N:,} 筆 16-bit integers")
print(f"Python sorted() : {time_builtin:.4f} 秒")
print(f"Counting Sort   : {time_counting:.4f} 秒")
print(f"Radix Sort      : {time_radix:.4f} 秒")
print()
print(f"Counting / sorted : {time_counting / time_builtin:.1f}x")
print(f"Radix    / sorted : {time_radix / time_builtin:.1f}x")
