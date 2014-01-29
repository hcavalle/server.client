#main for server application
from pprint import pprint
import socket
import gevent
import gevent.server
import gevent.socket
import gevent.queue
import sys

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

    while True:
      line = socket.recv(8192)
      if len(line)>0:
        print line  
        self.parse_client_input(line)
      #on close exit gracefully, remoce from active list
  
    return (socket, address)
  def parse_client_input(self, client_input):
    print client_input

class Client(object):
  name = None
  def __init__(self, connection, address):
    self.address = address
    self.connection = connection
    self.messages = gevent.queue.Queue() #possibly connection instead
  #set message push as eithe queue or .receive ...

class Channel(object):
  def __init__(name):
    self.subs = set() #what?
    self.messages = []
  
  def subscribe(self, client):
    self.subs.add(client)

  def add_message(self, message):
    for client in self.subs:
      print(client)
      #client.queue.put_nowait(message)
      #send to all using send
    self.messages.append(message)

class ChannelManager(object):
  channel_list = []
  
  def create_channel(name):
    channel_list.append(Channel(name))

class ServerApp(object):

  connection_manager = ConnectionManger()
  channel_manager = ChannelManager()
  
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.address = (host, port)
    self.tcp_server = gevent.server.StreamServer( (self.host, self.port), self.connection_manager.client_connect )

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

if __name__ == "__main__":
  server = ServerApp(sys.argv[1], int(sys.argv[2]))
  server.serve()
  print server.host+" "+server.port
  pprint(vars(server.tcp_server))
