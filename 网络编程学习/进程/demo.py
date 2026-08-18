from multiprocessing import Process
import time
import os


my_sum = 0

def a(t1, a):
    for i in range(t1):
        my_sum+=1

    print(f"a ID: {os.getpid()}")

def b(t2, b):
    for i in range(t2):
        my_sum+=1

    print(f"b ID: {os.getpid()}")



if __name__ =='__main__':
    p1 = Process(target=a, kwargs={'t1':1000000, 'a':'ima'},daemon=True)
    p2 = Process(target=b, kwargs={'t2':1000000, 'b':'imb'},daemon=True)
    # p1.daemon = True
    # p2.daemon = True
    p1.start()
    print('-' * 23)
    p2.start()
    print(f"main ID: {os.getpid()}")
    print(f"parent ID: {os.getppid()}")
    time.sleep(0.1)
    print("Over")


