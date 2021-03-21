from random import randint
from time import sleep

def randomSleep():
    sleep(randint(1, 2))
    return

def remSpaces(string):
    a = string.split()
    new_string = "".join(a)
    return new_string
