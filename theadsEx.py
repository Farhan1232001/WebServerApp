# SuperFastPython.com
# example of using a pipe between processes
from time import sleep
from random import random
from multiprocessing import Process
from multiprocessing import Pipe
 
# generate work
def sender(connection):
    print('Sender: Running', flush=True)
    # generate work
    for i in range(10):
        # generate a value
        value = random()
        # block
        sleep(value)
        # send data
        connection.send(value)
    # all done
    connection.send(None)
    print('Sender: Done', flush=True)
 
# consume work
def receiver(connection):
    print('Receiver: Running', flush=True)
    # consume work
    while True:
        # get a unit of work
        item = connection.recv()
        # report
        print(f'>receiver got {item}', flush=True)
        # check for stop
        if item is None:
            break
    # all done
    print('Receiver: Done', flush=True)
 
# entry point
if __name__ == '__main__':
    # create the pipe
    conn1, conn2 = Pipe()
    # start the sender
    sender_process = Process(target=sender, args=(conn2,))
    sender_process.start()
    # start the receiver
    receiver_process = Process(target=receiver, args=(conn1,))
    receiver_process.start()
    # wait for all processes to finish
    sender_process.join()
    receiver_process.join()


"""
import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
    datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    x.join()
    logging.info("Main    : all done")
"""