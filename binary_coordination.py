'''
Binary Coordination using semaphores

This pattern illustrates how to have a thread A proceed only
after receiving a signal from thread B.

This is done by initiating the semaphore to 0.
Thread A will wait on this signal by acquiring the semaphore,
while thread B will release the semaphore.

'''

from threading import Thread, Semaphore


def wait(permits):
    print("Awaiting thread A's signal")
    permits.acquire()
    print("Received thread A's signal")


def signal(permits):
    print("Signaling to thread B")
    permits.release()


def main():
    permits = Semaphore(value=0)

    threadA = Thread(target=wait, args=(permits,))
    threadA.start()

    threadB = Thread(target=signal, args=(permits,))
    threadB.start()

    threadA.join()
    threadB.join()


if __name__ == "__main__":
    main()
