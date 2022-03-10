'''
General Coordination using semaphores

This pattern illustrates how to generalize binary coordination
to ensure a thread A proceeds only after receiving a signal 
from thread(s) N times.

Initialize to 0; thread A waits n times on it, 
and other n threads signal.  Thus, there are no permits initially, and A must have n permits to advance. 

https://slides.com/troccoli/cs110-win2122-lecture-17/fullscreen#/26/0/0
'''
from threading import Thread, Semaphore

K_NUM_SIGNALS = 14


def wait(permits):
    signalCount = 0  # Note signalCount plays no functional role
    for i in range(K_NUM_SIGNALS):
        print("Awaiting ", signalCount, " signals")
        permits.acquire()
        signalCount += 1
    print("Received ", K_NUM_SIGNALS, " signals")


def signal(permits):
    print("Signaling to thread A")
    permits.release()


def cleanup(threads):
    for thread in threads:
        thread.join()


def main():
    permits = Semaphore(value=0)

    threadA = Thread(target=wait, args=(permits,))
    threadA.start()

    threads = []
    for i in range(K_NUM_SIGNALS):
        thread = Thread(target=signal, args=(permits,))
        thread.start()
        threads.append(thread)

    threadA.join()
    cleanup(threads)


if __name__ == "__main__":
    main()
