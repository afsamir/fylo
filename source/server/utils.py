from functools import reduce
from math import ceil, gcd, sqrt
import operator
from random import randint, random


def logger(func):
    def wrapper(*args):
        # print("client: " + str(args))
        output = func(*args)
        # print("server: " + str(output))
        return output

    return wrapper


def is_prime(num):
    sqr = ceil(sqrt(num))
    for i in range(2, sqr + 1):
        if num % i is 0:
            return False
    return True


def random_big_prime():
    i = randint(100000000, 100000000000)
    while True:
        if is_prime(i):
            return i
        else:
            i = i + 1


def generate_ras_key():
    p, q = random_big_prime(), random_big_prime()
    n = p * q
    phi_n = (p - 1) * (q - 1)
    d, e = 0, 0
    for i in range(2, phi_n):
        if gcd(i, phi_n) is 1:
            e = i
            break

    for i in range(1, phi_n):
        if float((i * phi_n + 1) / e).is_integer():
            d = int((i * phi_n + 1) / e)
            break

    return (n, e), (n, d)


def rsa_encrypt(msg, private_key):
    binary_representation = "".join(
        list(map(lambda x: bin(x)[2:], bytearray(msg, "utf8")))
    )
    x = int(binary_representation, 2)
    print(binary_representation)
    return bin_power(binary_representation, private_key[1]) % private_key[0]


def bin_power(base, exp):
    x = bin(exp)
    print(x)
    arr = []
    for i in range(len(x) - 1, 1, -1):
        if x[i] is "1":
            arr.append(int(base) << i)
    return reduce(lambda x, y: x * y, arr)


keys = generate_ras_key()
