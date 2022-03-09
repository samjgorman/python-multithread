''''

Making reads and writes to a shared data structure:

This demo program requires thread coordination with
semaphores to avoid race conditions in which...
1. The reader reads garbage data where valid data was not yet written
2.  The writer overwrites unread data

The reader and writer threads need to access the context of each other.
A reader should not write until valid data is available to read.
A writer should not write until there is space available to write.

Note that as an example, print statements are included to demonstrate concurrency.

Sources: 
https://slides.com/troccoli/cs110-win2122-lecture-17/fullscreen#/38/0/2
https://web.stanford.edu/class/cs110/examples/threads/lect17/reader-writer.cc

'''

from threading import Thread, Lock, Semaphore
from collections import deque
from random import choice, uniform
import string
import time


BUF_SIZE = 10
NUM_ITERATIONS = 100


def simulateNetworkDelay():
    time.sleep(uniform(0.05, 0.15))


def writeData():
    simulateNetworkDelay()
    return choice(string.ascii_letters)


def writeToBuf(buf,  isEmptySlotSem, isFullSlotSem, numIterations):

    for i in range(numIterations):
        ch = writeData()
        # Await signal that buf has empty slots to write to
        isEmptySlotSem.acquire()
        buf[i % BUF_SIZE] = ch
        # Signal that buf has written to & filled slot
        print("Writing ", ch, " to buf")
        isFullSlotSem.release()


def readFromBuf(buf, isEmptySlotSem, isFullSlotSem, numIterations):
    readFromBuffer = []
    for i in range(numIterations):
        # Await signal that buf has full slots to read from
        isFullSlotSem.acquire()
        simulateNetworkDelay()
        readCh = buf[i % BUF_SIZE]
        # Signal that buf now has an empty slot to write to
        print("Reading ", readCh, " from buf")

        readFromBuffer.append(readCh)
        isEmptySlotSem.release()

    print(readFromBuffer)


def main():

    isEmptySlotSem = Semaphore(value=BUF_SIZE)
    isFullSlotSem = Semaphore(value=0)

    buf = deque([], maxlen=BUF_SIZE)
    for i in range(BUF_SIZE):
        buf.append('')

    writer = Thread(target=writeToBuf, args=(
        buf, isEmptySlotSem, isFullSlotSem, NUM_ITERATIONS))
    reader = Thread(target=readFromBuf, args=(
        buf, isEmptySlotSem, isFullSlotSem, NUM_ITERATIONS))

    writer.start()
    reader.start()

    writer.join()
    reader.join()


if __name__ == "__main__":
    main()
