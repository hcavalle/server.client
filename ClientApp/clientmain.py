from pprint import pprint
import gevent
import gevent.socket
import sys

class Client(object):
  clientsocket = None
  def __init__(self, host, port, name):
    self.dest_host = host
    self.dest_port = int(port)
    self.dest_addr = (host, port)
    self.name = name

  def connect(self):
    self.clientsocket = gevent.socket.create_connection(self.dest_addr)
    self.send_message("test")
    gevent.spawn( self.client_sender() )
    gevent.spawn( self.client_receiver() )

  def client_sender(self):
    while True:
      line = raw_input("Enter command: ")
      if len(line)>0:
        if ( line == "exit"):
          print "exiting..."
          sys.exit()
        if ( line == "help"):
          self.show_help()

        self.send_message(line) 

  def show_help(self):
    print "Commands available: "
  
  def client_receiver(self):
    while True:
      line = self.recv(8192)
      if len(line)>0:
        self.parse_response()  
  
  def parse_response(response):
    print response

  def send_message(self, message):
    try:
      print "sending message"
      self.clientsocket.send(message)
      print "message: ", message, " sent"
    except:
     print "error sending message ", sys.exc_info()[0] 

if __name__ == "__main__":
  client = Client(sys.argv[1], int(sys.argv[2]), sys.argv[3])
  gevent.spawn( client.connect() )

  pprint( vars(client.clientsocket) )
  print client.clientsocket.getsockname()
