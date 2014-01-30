#python clientmain.py 127.0.0.1 23400 "test"
import shlex
from pprint import pprint
import gevent
from gevent import Greenlet
import gevent.socket
import sys

import simplejson as json

class Client(object):
  clientsocket = None
  def __init__(self, host, port):
    self.dest_host = host
    self.dest_port = int(port)
    self.dest_addr = (host, port)
    self.name = None

  def welcome(self):
    name = None
    while not self.name:
      name_in = raw_input("Welcome! What's your name?\n")
      if len(name_in)>0:
        self.name = name_in
        print "Hi "+self.name+". Here's what you can do here\n"
        self.show_help()

  def connect(self):
    self.clientsocket = gevent.socket.create_connection(self.dest_addr)
    if (self.clientsocket):
      print "Connected to server! \n"
    self.welcome()
    self.clientsocket.send("name "+self.name);

    while True:
      g1 = Greenlet(self.client_sender() )
      g2 = Greenlet(self.client_receiver() )

  def client_sender(self):
    line = raw_input("Enter command: ")
    if len(line)>0:
      if ( line == "exit"):
        print "exiting..."
        sys.exit()
      if ( line == "help"):
        self.show_help()
      self.send_message(line) 

  def show_help(self):
    print "Commands available: \n"
  
  def client_receiver(self):
    line = self.clientsocket.recv(10000)
    if len(line)>0:
      self.parse_response(line)  
 #   gevent.sleep(0)
  
  def parse_response(self, response):
    print response

  def send_message(self, message):
    try:
      self.clientsocket.send(message)
    except:
     print "error sending message ", sys.exc_info()[0] 

if __name__ == "__main__":
  client = Client(sys.argv[1], int(sys.argv[2]))
  client.connect()

