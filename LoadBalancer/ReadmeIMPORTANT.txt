In the LoadBalancer, I have wriiten 2 scripts.

1.LoadBalancer.py (Incomplete)
  This is a more organized and Object Oriented script. This determines how we can actually make use of OOPS concepts in Python. However,  this script as of now assigns the task to the threads in a Round Robin fashion with the constraint that id assigns task to 2nd thread only after first thread has completed its execution. Hence parallelism is not achieved . I am looking for a way to it parallelly with the RoundRobinQueueManegr approach.

  In the meantime, I have written one more script which achieives the RoundRobin assignment along with parallelism without the use of any Manager. It contains the interaction of Worker threads with the taskqueue directly.


2.RRLoadBalancer.py(Complete)
  In this script, I have a SHARED taskqueue used by all the threads in Pool. In this the Thread Workers can access the Queue themselves. 

  In the above case(Case#1), the RoundRobinQueueManager maintains the interaction between the Tasks queue and the Thread workers. This is a better and scalable approach though.

