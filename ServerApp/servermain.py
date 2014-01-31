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
    socket.setblocking(0)
    client = Client(socket, address)
    print "New connection from ", address

    self.active_client_list.append(client)
    #time = now()
    self.client_history.append(client) #add time as second in tuple

    return (client)

class Client(object):
  name = "Anon"

  def __init__(self, socket, address):
    self.address = address
    self.socket = socket
    self.message_history = [] #possibly connection instead
    self.subs = [] #what?
  #set message push as eithe queue or .receive ...

  def send(self, message):
    self.socket.send(message)

  def add_message_history_item(self, message):
    #time = datetime.datetime.now()
    self.message_history.append(message)

  def set_name(self, name):
    self.name = name
    self.send(("Name set to:", name ))

  def subscribe(self, channel):
    self.subs.append(channel)

class Channel(object):
  def __init__(self, name):
    self.name = name
    self.subs = set() #what?
    self.message_history = []
  
  def subscribe(self, client):
    self.subs.add(client)
    message = client.name+" added to "+self.name
    print message
    client.send(message)

  def publish(self, message, name):
    for client in self.subs:
      print(client.name)
      client.send(message)
      #client.queue.put_nowait(message)
      #send to all using send
    self.message_history.append(message)

class ChannelManager(object):
  channels = {}
  
  def is_valid_channel(self, name):
    #ideallly would be abstracted to object class, and take classType and object, see if object matches class def
    if (name in self.channels.keys()):
      return True
    return False
    
  def create_channel(self, name):
      self.channels[name] = Channel(name)

  def get_channel_by_name(self, name):
    if (self.is_valid_channel(name)):
      return self.channels[name]

  def get_channel_list(self):
    return self.channels

  def subscribe_channel(self, name, client):
    channel = self.get_channel_by_name(name)
    if (channel):
      channel.subscribe(client) 
      client.subscribe(channel)

class ServerApp(object):

  connection_manager = ConnectionManger()
  channel_manager = ChannelManager()
  
  def __init__(self, host, port):
    print "Server starting..."
    self.host = host
    self.port = port
    self.address = (host, port)
    self.tcp_server = gevent.server.StreamServer( (self.host, self.port), self.new_connection )
    self.channel_manager.create_channel("main_channel")
    self.print_info()
    print "Server started"

  def new_connection(self, socket, address):
    client = self.connection_manager.client_connect(socket, address)
    #CAN MOVE TO SERVERi CLASSV CONNECT FUNC?
    input_handle = self.handle_input(client)
    #input_handle.join()
      #on close exit gracefully, remoce from active list

  def handle_input(self, client):
    #set available requests, key (command) value (function, args)
    #parse client input into pieces, (command args) and based on command, call function based on dict above
    commands = { 
      "name": "Takes one argument and sets it to your name on server.",
      "listchannels": "Takes no arguments and dislplays available channels on server",
      "createchannel": "Takes one argument and creates a channel on server with arg1 as name",
      "subscribe": "Takes one argument as the name of the channel to subscribe to messages from", 
      "publish": "Takes two string arguments: first is channel name, second string to publish to that channel"
    }
    while True:
      client.socket.settimeout(1000)
      client_input = client.socket.recv(8192)
      client.add_message_history_item(client_input)

      if not client_input:
        break 
      print client.name, ": ", client_input
      exploded_input = client_input.split()

      if exploded_input[0] == "listchannels":
        channels = self.channel_manager.get_channel_list()
        for name in channels.keys():
          response = name+"\n"
          client.send(response)
      elif exploded_input[0] == "subscribe":
        self.channel_manager.subscribe_channel(exploded_input[1], client)
      elif exploded_input[0] == "publish_message":
        #check if is memeber
        channel = self.channel_manager.get_channel_by_name(exploded_input[1])
        channel.publish(exploded_input[2], client.name)
        #else:client.send("Join a channel first.\n")
      elif exploded_input[0] == "createchannel":
        self.channel_manager.create_channel(exploded_input[1]) 
        client.send("Channel created. \n")
      elif exploded_input[0] == "name":
        client.name = exploded_input[1]
        client.send("Name updated. \n")
      elif exploded_input[0] == "exit":
        client.socket.close()
        print client.name+" disconnected"
      else:
        client.send("\nAvailable commands are:\n\n")
        for key, value in commands.items():
          client.send(key+"\n")
          client.send("\t"+value+"\n\n")
        #client.send("message received and logged.\n")
        
    
  def new_channel(self, name):
    self.channel_manager.create_channel(name)
  
  def serve(self):
    try:
      self.tcp_server.serve_forever(), new_connection
      print "Server started"
    except:
      print "Error starting server", sys.exc_info()[0]
      raise
  def print_info(self):
    print self.host, " ", self.port
   # pprint(vars(self.tcp_server))

if __name__ == "__main__":
  server = ServerApp(sys.argv[1], int(sys.argv[2]))
  server.serve()
