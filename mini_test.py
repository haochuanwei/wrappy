from wrappy import guard, probe, memoize
import time

@memoize(cache_limit=200, persist_path='./factorials.pkl')
@guard()
def factorial(n):
    assert isinstance(n, int) and n > -1
    time.sleep(0.1)
    if n == 0:
        return 1
    return n * factorial(n-1)

probed_factorial = probe()(factorial)

if __name__ == '__main__':
    probed_factorial(1)
    factorial(-1)
    for k in range(100, 110):
        factorial(k)
        print(k)
