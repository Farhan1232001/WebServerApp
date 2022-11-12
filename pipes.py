# https://python-course.eu/applications-python/pipes-in-python.php
# example program demoing piplines

import os

def child(pipeout):
  bottles = 99
  while True:
    bob = "bottles of beer"
    otw = "on the wall"
    take1 = "Take one down and pass it around"
    store = "Go to the store and buy some more"

    if bottles > 0:
      values =  (bottles, bob, otw, bottles, bob, take1, bottles - 1,bob,otw)
      verse = "%2d %s %s,\n%2d %s.\n%s,\n%2d %s %s.\n" % values
      os.write(pipeout, verse.encode())
      bottles -= 1
    else:
      bottles = 99
      values =  (bob, otw, bob, store, bottles, bob,otw)
      verse = "No more %s %s,\nno more %s.\n%s,\n%2d %s %s.\n" % values
      os.write(pipeout, verse)
def parent():
    pipein, pipeout = os.pipe()
    pid = os.fork() # Create a child process. Method returns 0 in the child process and the pid in parent process
    if pid == 0:
        # im the child
        os.close(pipein)
        child(pipeout)
    else:
        # im the parent
        os.close(pipeout)
        counter = 1
        pipein = os.fdopen(pipein)  # returns an open file object connected to the file descripter pipin (==Int)
        while True:
            print ('\nverse %d' % (counter))
            for i in range(4):
                verse = pipein.readline()[:-1]
                print ('%s' % (verse))
            counter += 1
            print

parent()