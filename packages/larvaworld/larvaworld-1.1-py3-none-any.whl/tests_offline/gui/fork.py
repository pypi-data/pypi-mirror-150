import os
import sys
import signal
import time
import numpy as np

p1=(120,35)
p2=(20,335)


def compute_dst(point1, point2):
  x1, y1 = point1
  x2, y2 = point2
  return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def handle_signal(signum, frame):
  print ('Caught signal "%s"' % signum)
  if signum == signal.SIGTERM:
    print ('SIGTERM. Exiting!')
    sys.exit(1)
  elif signum == signal.SIGHUP:
    print ('SIGHUP')
  elif signum == signal.SIGUSR1:
    print ('SIGUSR1 Calling wait()')
    pid, status = os.wait()
    print ('PID was: %s.' % pid)


def main():
  print( 'Starting..')
  signal.signal(signal.SIGCHLD, handle_signal)
  signal.signal(signal.SIGHUP, handle_signal)
  signal.signal(signal.SIGTERM, handle_signal)
  signal.signal(signal.SIGUSR1, handle_signal)

  try:
    ff_pid = os.fork()
  except OSError as err:
    print ('Unable to fork: %s' % err)
  print(ff_pid)
  if ff_pid > 0:
    # Parent.
    print( 'First fork.')
    print ('Child PID: %d' % ff_pid)
    sys.exit(0)
  elif ff_pid == 0:
    # Child 1.
    # print(os.getsid(ff_pid))
    print(compute_dst(p1,p2))
    os.setsid()
    # print(os.getsid(ff_pid))
    os.chdir('/')
    # print(os.getsid(ff_pid))
  print(ff_pid)
    # try:
    #     sf_pid = os.fork()
    # except OSError as err:
    #     print ('Unable to fork: %s' % err)
    #
    # if sf_pid > 0:
    #   # Parent 1.
    #   print ('Second fork.')
    #   print ('Child PID: %d' % sf_pid)
    #   os._exit(os.EX_OK)
    # elif sf_pid == 0:
    #   # Child 2.
    #   while True:
    #     time.sleep(1)


if __name__ == '__main__':
 main()