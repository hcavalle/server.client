#main for server application
from pprint import pprint
import socket
import gevent
import gevent.server
import gevent.socket
import gevent.queue
import sys
import datetime

import simplejson as json

#import connectionhandler

class ConnectionManger(object):
  active_client_list = []
  client_history = []
 
  def client_connect(self, socket, address):
  #add socket. funcs 
    print "new connection"
    socket.send("you're connected!");
    client = Client(socket, address)

    self.active_client_list.append(client)
    #time = now()
    self.client_history.append(client) #add time as second in tuple

    #return (socket, address)

#CAN MOVE TO SERVERi CLASSV CONNECT FUNC?
    while True:
      line = socket.recv(8192)
      if len(line)>0:
        print line
        self.handle_input(client, line)
      #on close exit gracefully, remoce from active list

  def handle_input(self, client, client_input):
    #set available requests, key (command) value (function, args)
    #parse client input into pieces, (command args) and based on command, call function based on dict above
    exploded_input = client_input.split()
    print exploded_input
    if exploded_input[0] == "subscribe":
      print "CLIENT INPUT", exploded_input[0]
      #client.add_sub(exploded_input[1])    
    #print client_input

class RequestHandler(object):
  available_requests = {
    "subscribe": "",
    "listchannels": "",
    "addchannel": "",
    "listclients": "",
  }
  def __init__(client_input):
    print "test"
    

class Client(object):
  name = None
  def __init__(self, connection, address):
    self.address = address
    self.connection = connection
    self.message_history = [] #possibly connection instead
  #set message push as eithe queue or .receive ...
  def add_message_history_item(self, message):
    #time = datetime.datetime.now()
    self.message_history.append(message)
    

class Channel(object):
  def __init__(self, name):
    self.name = name
    self.subs = set() #what?
    self.messages = []
  
  def subscribe(self, client):
    self.subs.add(client)

  def add_message(self, message):
    for client in self.subs:
      print(client.name)
      client.send(message)
      #client.queue.put_nowait(message)
      #send to all using send
    self.messages.append(message)

class ChannelManager(object):
  channel_list = []
  
  def create_channel(self, name):
    self.channel_list.append(Channel(name))

class ServerApp(object):

  connection_manager = ConnectionManger()
  channel_manager = ChannelManager()
  
  def __init__(self, host, port):
    print "Server starting..."
    self.host = host
    self.port = port
    self.address = (host, port)
    self.tcp_server = gevent.server.StreamServer( (self.host, self.port), self.connection_manager.client_connect )
    self.new_channel("main_channel")
    self.print_info()
    print "Server started"

  def new_connection(self, socket, address):
    self.connection_manager.client_connect(socket, address)
    
  def new_channel(self, name):
    self.channel_manager.create_channel(name)
  
  def serve(self):
    try:
      gevent.spawn(self.tcp_server.serve_forever())
      print "Server started"
    except:
      print "Error starting server", sys.exc_info()[0]
      raise
  def print_info(self):
    print self.host, " ", self.port
    pprint(vars(self.tcp_server))

if __name__ == "__main__":
  server = ServerApp(sys.argv[1], int(sys.argv[2]))
  gevent.spawn(server.serve())
