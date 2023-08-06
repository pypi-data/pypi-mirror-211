# Time    : 2023/6/1 13:44:52
# Author  : dabinhuang
# File    : gentor.py
# Version : python3.7.5

import random

def generate_random_numbers(n):
    return [random.randint(1, 100) for _ in range(n)]
