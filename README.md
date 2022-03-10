# python-multithread
Experiments with multithreading in Python.

## Semaphores
### Dining Philosopher's Problem
Toy example originally designed by Dijkstra that illustrates
the pitfalls of deadlock and the paradigm of semaphores as permits.
### Binary Coordination
Pattern illustrating how to have a thread A proceed only
after receiving a signal from thread B.
### General Coordination
Pattern illustrating how to have a thread A proceed only after receiving a signal 
from thread(s) N times.
### Reader-Writer
Coordination of a reader thread & writer thread to access shared data structure.
### Threaded RSS Feed
Web scraper for RSS feed(s) to demonstrate multithreading and locks.

Examples adapted from C++ to Python from [Stanford CS110](https://web.stanford.edu/class/archive/cs/cs110/cs110.1216/) for my own learning purposes.
