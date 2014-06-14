import socket
import urllib2
from datetime import datetime
import sys

RESPONSE_TIMEOUT=5

class MonitorServer:
  def __init__(self,ip=None,port=None,url=None,tcp=False,Http=False):
    self.tcpcheck=tcp
    self.httpcheck=Http
    self.ip=ip
    self.port=port
    self.url=url
    self.server_test()

  def server_test(self):
    if self.tcpcheck:
      self.tcp_test()
    if self.httpcheck:
      self.http_test()


  def tcp_test(self):
    if self.ip!=None and self.port!=None:
      try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip,self.port))
        s.close()
        print "TCP service running Successfully at port %s:%d"%(self.ip,self.port)
      except:
        print "TCP Service  down at mentioned port....!!"
    else:
      print "Either IP address or Port Missing"


  def http_test(self):
    if self.url!=None:
      start=datetime.now()
      try:
        response = urllib2.urlopen(self.url)
      except:
        print "Invalid Url. Threw Exception"
        sys.exit(-1)
      if response.getcode()==200:
        end=datetime.now()
        if (end-start).seconds<=RESPONSE_TIMEOUT:
          print "Sever is HEALTHY"
        else:
          print "Server is OVERLOADED"
      else:
        print "Server is DOWN"

def usage():
    print "\n"
    print "#"*10+"Sample command can be of types:"+"#"*10
    print "\n"
    print "python ServerMonitor.py tcp 10.0.0.12:8000"
    print "\n"
    print "python ServerMonitor.py http http://www.google.com"
    print "\n"


if __name__=='__main__':
  if len(sys.argv)!=3:
    usage()
    sys.exit(-1)
  if sys.argv[1]=="tcp":
    ip,port=sys.argv[2].split(":")
    port=int(port)
    MonitorServer(ip=ip,port=port,tcp=True)
  if sys.argv[1]=="http":
    url=sys.argv[2]
    MonitorServer(url=url,Http=True)
 

  

