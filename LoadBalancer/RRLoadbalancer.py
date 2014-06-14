import threading
import sys
import time

lock=threading.RLock()
NUM_TASKS=10
TASK_TIME=[4,5,2,3,1,3,4,2,1,4]
NUM_WORKER=3
EVENT=threading.Event()


class Queue:
  def __init__(self):
    self.start=0
    self.end=0
    self.queue=[]
    self.turn=0

  def add(self,element):
    self.queue.append(element)
    self.end+=1
    
  def __getitem__(self,index):
    return self.queue[index]

  def remove(self):
    if not self.isEmpty():
      if self.start < self.end:
        self.start+=1
    else:
      print "Queue Empty"

  def isEmpty(self):
    if self.start==self.end:
      return True
    else:
      return False


taskqueue=Queue()


class Worker(threading.Thread):
  def __init__(self,id):
    self.stop=EVENT
    threading.Thread.__init__(self,args=(id, self.stop))
    self.id=id
    self.exit=False
    
  def run(self):
    self.getNextTask()


  def processTask(self,task):
    global exit_flag
    print "Worker %d processing task %d for %d seconds"%(self.id,task.id,task.time)
    time.sleep(task.time)
    self.stop.wait()
    if not taskqueue.isEmpty():
      self.getNextTask()
    else:
      self.exit=True
      self.stop.set()


  def getNextTask(self):
    global taskqueue
    global lock
    while taskqueue.turn!=self.id:
      if not taskqueue.isEmpty():
        self.stop.wait()
      else:
        break
    else:
      if taskqueue.start !=taskqueue.end:
        with lock:
          elem=taskqueue[taskqueue.start]
          taskqueue.turn=(taskqueue.turn+1)%NUM_WORKER
          taskqueue.remove()
        self.stop.set()
        self.processTask(elem)
      else:
        self.exit=True
        self.stop.set()
    self.exit=True



class Task:
    def __init__(self,id,reqTime):
        self.id=id
        self.time=reqTime

def startWorkers(workerlist):
      for workers in workerlist:
        workers.start()

def checkAndstopWorkers(workerlist):
  count=len(workerlist)
  current=0
  for workers in workerlist:
    if workers.exit==True:
      current+=1
  if current==count:
    sys.exit(0)
  else:
    current=0

if __name__=="__main__":
  workerlist=[Worker(i) for i in xrange(0,NUM_WORKER)]
  for i in xrange(0,NUM_TASKS):
    taskqueue.add(Task(i,TASK_TIME[i]))
  startWorkers(workerlist) 
  while True:
    checkAndstopWorkers(workerlist)
  
  