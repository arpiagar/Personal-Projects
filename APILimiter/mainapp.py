#!flask/bin/python
from flask import Flask, jsonify,abort,make_response,request
from threading import Thread,RLock,Timer
import atexit
import time


ip_address_tracker={} #Global DS shared between the request threads
MAX_LIMIT=1000 #Number of requests allowed by a single IP.
whitelistip=[] #List containing the WhiteList IP.
blacklistip=[] #List containing the BlackList IP.
REFRESH_TIME=1 #Time after which we refresh the global dictionary. Required , otherwise the Python would run out of memory due to request from various Ip addresses.
  

dataLock = RLock() # Re entrant locks to avoid Thread deadlock .

def cleartracker():
        global ip_address_tracker
        with dataLock:
            ip_address_tracker={}   

# Thread running as a Daemon to refresh the global ip_address_tracker dict after the specified REFRESH_TIME
class CustomThread(Thread):
    global ip_address_tracker
    def __init__(self):
        super(CustomThread,self).__init__()
    
    def run(self):
        while True:
            time.sleep(REFRESH_TIME)
            cleartracker()
        

    

app = Flask(__name__)
#def create_app(app):
class RequestHandler():
    customThread=CustomThread()
    customThread.setDaemon(True)    
    customThread.start()

    def __init__(self,app):
        customThread=CustomThread()
        customThread.setDaemon(True)    
        customThread.start()
        self.read()
        app.run(debug = True)
    #When interrupt is called , the Whitelist and Black IP's are dumped into the files.
    def read(self):
        with  open('WhiteListIP.txt') as f:
            content=f.read()
        for lines in content.split('\n'):
            whitelistip.append(lines)
        with open('BlackListIP.txt') as f:
            content=f.read()
        for lines in content.split('\n'):
            blacklistip.append(lines)
           
def interrupt():
    print "Interrupt Called"
    global customThread
    global whitelistip
    global blacklistip
    with dataLock:
        try:
            f=open('WhiteListIP.txt','wb')
            for elem in whitelistip:
                f.write(elem+'\n')
        finally:
            f.close()
        try:
            f=open('BlackListIP.txt','wb')
            for elem in blacklistip:
                f.write(elem+'\n')
        finally:
            f.close() 
   
#app.run(debug = True) # App is run only after running the background CustomThread.
atexit.register(interrupt)
        
    
@app.route('/login')
def index():
    remote_addr=request.remote_addr
    if remote_addr in whitelistip and remote_addr not in blacklistip:
        if ip_address_tracker.has_key(remote_addr):
            if ip_address_tracker[remote_addr]<MAX_LIMIT:
                ip_address_tracker[remote_addr]+=1
            else:
                abort(404)
        else:
            ip_address_tracker[remote_addr]=1
        return str(ip_address_tracker[remote_addr]) 
    else:
        return "Not Authorized"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


if __name__ == '__main__':  
    RequestHandler(app)
