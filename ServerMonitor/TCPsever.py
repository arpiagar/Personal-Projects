import socket


if __name__=="__main__":
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  print socket.gethostname()
  s.bind(('127.0.0.1',1212))
  s.listen(5)
while True:
  (clientsocket, address) = s.accept()
  print clientsocket,address