import threading
import sys
import time

lock=threading.RLock()
NUM_TASKS=10
TASK_TIME=[4,5,2,3,1,3,4,2,1,4]
NUM_WORKER=3
EVENT=threading.Event()
CURRENT_TASK=None
AVAILABLE_WORKERS=[]

class Worker(threading.Thread):
  def __init__(self,id):
    #self.stop=threading.Event()
    self.stop=EVENT
    threading.Thread.__init__(self,args=(id, self.stop))
    self.id=id
    self.running=False

  def startRunning(self):
    self.running=True

  def stopRunning(self):
    self.running=False

  def run(self):
    global CURRENT_TASK
    while True:
      if CURRENT_TASK!=None and self.id in AVAILABLE_WORKERS:
        with lock:
          taskAtHand=CURRENT_TASK
          CURRENT_TASK=None
        self.processTask(taskAtHand)
      else:
        self.stop.wait()
        



  def processTask(self,task):
    self.startRunning()
    print "Worker %d processing task %d for %d seconds"%(self.id,task.id,task.time)
    time.sleep(task.time)
    self.stopRunning()
    self.stop.wait()


class WorkerList:
    def __init__(self,workerlist):
      self.num=len(workerqueue)
      self.idle=[x.id for x in workerqueue]
      self.busy=[]


class Queue:

  def __init__(self):
    self.length=0
    self.queue=[]

  def add(self,element):
    self.queue.append(element)
    self.length+=1
    return 

  def remove(self):
    if self.length:
      self.queue=self.queue[1:]
      self.length-=1
    else:
      raise NameError('Stop Iteration')

  def next(self):
    elem=self.queue[0]
    self.remove()
    return elem

  def isEmpty(self):
    if self.length==0:
      return True
    else:
      return False



class RoundRobinQueue:
  def __init__(self):
    Queue.__init__(self)
    self.turn=0

  def next(self):
    Queue.next()
    self.turn=(self.turn+1)%NUM_WORKER

class Task:
    def __init__(self,id,reqTime):
        self.id=id
        self.time=reqTime

class TaskManager:
    def __init__(self,tasktype='dynamic',taskqueue=None,workerlist=None):
      self.tasktype=tasktype
      self.taskqueue=taskqueue
      self.workerlist=workerlist
      self.availableworkers=[]
      self.currenttask=None

      
    def startProcessing(self):
      if not self.taskqueue and  not self.workerlist:
        print "Invalid Taskqueue or Workerlist"
        sys.exit(-1)
      
      if self.tasktype.lower()=='roundrobin':
        self.startWorkers()
        r=RoundRobinTaskManager(self.tasktype,self.taskqueue,self.workerlist)
        r.startprocessing()
      elif self.tasktype.lower()=='dynamic':
        self.startWorkers()
        d=DynamicTaskManager(self.tasktype,self.taskqueue,self.workerlist)
      else:
        print "Invalid Algo type entered"
        self.stopWorkers()
        sys.exit(-1)

    def startWorkers(self):
      for workers in self.workerlist:
        workers.start()

    def stopWorkers(self):
      for workers in self.workerlist:
        workers.stop.clear()

class RoundRobinTaskManager(TaskManager):
  global CURRENT_TASK
  def __init__(self,tasktype='RoundRobin',taskqueue=None,workerlist=None):
      TaskManager.__init__(self,tasktype,taskqueue,workerlist)
      self.currentworker=-1
      self.num_worker=len(workerlist)
      
  

  def getNextWorker(self):
    while workerlist[(self.currentworker+1)%self.num_worker].running==True:
      continue
    self.currentworker=(self.currentworker+1)%self.num_worker
    print "Returning worker %d"%(self.workerlist[(self.currentworker+1)%self.num_worker].id)
    return self.workerlist[(self.currentworker+1)%self.num_worker]

  def startprocessing(self):
    global CURRENT_TASK
    import pdb;pdb.set_trace()
    while not self.taskqueue.isEmpty():
      try:
        worker=self.getNextWorker()
        self.currentworker=worker.id
        if CURRENT_TASK==None:
          while worker.running!=False:
            with lock:
              CURRENT_TASK=self.taskqueue.next()
              AVAILABLE_WORKERS=[worker.id]
          worker.stop.set()
        #worker.processTask(self.currenttask)
      except:
        print "Task queue is empty"
        break
    self.stopWorkers()

  




def startWorkers(workerlist):
      for workers in workerlist:
        workers.start()

if __name__=="__main__":
  taskqueue=Queue() 
  workerlist=[Worker(i) for i in xrange(0,NUM_WORKER)]
  for i in xrange(0,NUM_TASKS):
    taskqueue.add(Task(i,TASK_TIME[i]))
  #algotype=raw_input('Enter either "RoundRobin" or "Dynamic
  algotype="roundROBIN" 
  t=TaskManager(algotype,taskqueue,workerlist)
  t.startProcessing()
