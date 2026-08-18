from threading import Thread, Lock
import time
import os


my_sum = 0

mutex = Lock()
def a(t1):
    global my_sum
    mutex.acquire()
    for _ in range(t1):
        my_sum+=1
    print(f"a: {my_sum}")
    mutex.release()


def b(t2):
    global my_sum

    for _ in range(t2):
        my_sum+=1
    print(f"b: {my_sum}")




if __name__ =='__main__':
    p1 = Thread(target=a, kwargs={'t1':1000000},daemon=True)
    p2 = Thread(target=b, kwargs={'t2':1000000},daemon=True)
    # p1.daemon = True
    # p2.daemon = True
    p1.start()
    print('-' * 23)
    p2.start()

    time.sleep(0.1)
    print("Over")


