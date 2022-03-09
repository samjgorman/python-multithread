'''
Dining Philosphers Problem:

Toy example (originally designed by Dijkstra) that illustrates
the pitfalls of deadlock and the paradigm of semaphores as permits.

The problem:
(Abridged from https://slides.com/troccoli/cs110-win2122-lecture-15/fullscreen#/20/0/4)

Five philosophers sit around a circular table, eating spaghetti.
There is one fork for each of them.
Each philosopher thinks, then eats, and repeats this three times for
their three daily meals.

To eat, a philosopher must grab the fork on their left and the fork on their right.
Then they chow on spaghetti to nourish their big, philosophizing brain.
When they're full, they put down the forks in the same order they picked them up and
return to thinking for a while.

To think, the a philosopher keeps to themselves for some amount of time.
Sometimes they think for a long time, and sometimes they barely think at all.

https://en.wikipedia.org/wiki/Dining_philosophers_problem

'''

from threading import Thread, Lock, Semaphore
from random import randint
import time

K_NUM_PHILOSOPHERS = 5
K_NUM_FORKS = 5


def eat(permits, left, right):
    permits.acquire()
    timeToEat = randint(1, 2)
    left.acquire()
    time.sleep(timeToEat)
    right.acquire()
    timeToEat = randint(1, 2)
    time.sleep(timeToEat)
    print("Im eating for ", timeToEat, " seconds")
    permits.release()  # Done eating, return the permit...

    left.release()
    right.release()


def philosophize(permits, left, right):
    timeToSleep = randint(1, 2)
    time.sleep(timeToSleep)
    print("Im thinking for ", timeToSleep, " seconds")
    eat(permits, left, right)


def cleanup(threads):
    for thread in threads:
        thread.join()


def main():
    forks = []
    permits = Semaphore(value=K_NUM_FORKS-1)
    threads = []

    for i in range(K_NUM_FORKS):
        fork = Lock()
        forks.append(fork)

    for i in range(K_NUM_PHILOSOPHERS):
        left = forks[i]
        right = forks[(i+1) % K_NUM_PHILOSOPHERS]
        thread = Thread(target=philosophize, args=(permits, left, right))
        threads.append(thread)

        thread.start()

    cleanup(threads)


if __name__ == "__main__":
    main()
