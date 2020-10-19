import etcd3
import time
import datetime
import functools
import concurrent.futures
import math
import os
ETCD_WATCH_COUNT = 0

def get_level1(func):
    a = {"leve1": 1 }
    print(a)
    def operator1(*args):
        a[func.__name__] = func(*args)
        return a
    print(a)
    return operator1

def get_level2(func):
    b = {"leve2": 2}
    print(b)
    def operator2(*args):
        b[func.__name__] = func(*args)
        return b
    print(b)
    return operator2



class level3(object):
    def __init__(self, op):
        self.op = op
    
    def __call__(self, func):
        def wrapped_function(*args):
            print(self.op)
            return func(*args)
        return wrapped_function

@level3("add")
def add(op1, op2):
    return op1+op2




PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    print(os.getpid())
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def fib(n):
    if n < 3:
        return 1
    return fib(n - 1) + fib(n - 2)

def main():
    start_time = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        task_list = executor.map(fib,  range(3, 35), chunksize=4)
        for item in task_list:
            print(item)
    print("ProcessPoolExecutor time is: {}".format(time.time() - start_time))

if __name__ == '__main__':
    main()
    #etcd = etcd3.client(host='192.168.30.144', port=2379, ca_cert="etcd/ca.pem", cert_cert="etcd/client.pem",cert_key='etcd/client-key.pem')

    #with etcd.lock('/key') as locker:
    #    print(etcd.get('/key'))
    #    etcd.put("/key", "locked by vscode")
    #    print(etcd.get('/key').value)
    # cancel watch
    



