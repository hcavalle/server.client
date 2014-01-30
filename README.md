server.client
=============

A simple server and client in python using the gevent library for concurrency. 

step 1: initial architecture design
=============
DESIGN

Architecture
python gevent
	GeventServer App
		Server
		ConnectionPool
		Channels
		ConnectionThread class



	Client App
		Sends name (desired channel)
			List all connected clients
			List all servers

Thought Process

IMPLEMENTATION


INSTALL

System purpose
To allow for real time notifications between a server and client applications. 

Proposed System Design
The system is comprised of two interfacing python applications: a client and a server, written using the gevent library. The client application can connect to, send messages to and receive messages from the server. The server application can receive connections and messages, and send messages to the client. Messages can be text or json payloads. 

The Server
The server service application is to consist of three primary components and one optional component (implemented as classes): ServerListener, ConnectionHandler, ClientManger, ServerManager (optional if time allows). 
	ServerListener
		Instantiated on running the server application, and is responsible for opening up two sockets (A and B) set to listen persistently for incoming client connections/communications (A) and incoming server communications (B). 

	ConnectionHandler
		Instantiated on incoming connection request from client application, and spawns a greenlet (thread-like routine within application process) and is responsible for handling receipt of inbound messages and sending of outbound messages to the initiating client. There is an instance of ConnectionHandler for each client connection. The proposed methods are:
			ClientMessageSender - accepts message as argument to sent to connected client
			ClientMessageReceiver - accepts message as argument to send to MessageHandler
			MessageHandler - accepts message as argument, parses and calls related function based on incoming message text
				Name - set, get
				Ip - get
				Connected - time, (duration?)
				Close
			

	ChannelManager
		Manages channels available to clients on a server. Clients can subscribe and publish to a channel.
		ChannelList
			Channel
			ChannelPub
			ChannelSub

	ClientManager
		ActiveClientList - Class with getters and setters
			ip
			name
			start_time
			duration
		ClientHistory
			Historical aggregation of all client conenctions. Data same as above, as hashmap.

	ServerManager
		Maintains a list of Servers running simultaneously (within the same memory). To be instantiated on server start, and polls for other server processes running and exchanges basic information.
			Server process_id

		Could potential round robin client connection requests based on load...

The Client
	ConnectionHandler (server)
		ConnectionRequester
			Sends a connection request to the server application to establish connection to a server. It sends the:
			ip
			processid
		Connection
			TCP connection to server established for comm.
	MessageReceiver
		Consumes and parses incoming data from server and displays it to screen. 
	MessageSender
		Send

Implementation Choices
Python was chosen over go for ease of development (time constraint), more thorough documentation available and more pervasive adoption. The server's top level subcomponents are implemented as objects to allow for logical clarity, modularity of functionality and abstraction of concepts involved in the implementation. 

A single consumer and producer model was chosen for the client for elegance and logical inclusion. The components are unified logically (abstracted to overarching client entity), but separated functionally (modularized into independent functions). 


RUN


Client
	two modules: sender and receiver
	ConnectionRequest
	MessageSend
	MessageReceive

Server App
	Server listener
	Connection Handler
		Client Sender
		Client Receiver
			Client Message Handler
				Available client triggered funcs:
					List Clients
					List Servers
					Help
					Reverse text
					Set welcome
	Client manager
		(Client History)
		Active Client List
			Client
				ip
				name
				welcome
				(message history)
	ServerManager
		Server List
		Scan for other server procs on server up, add self to other list, add other to self list
		CheckLoad()...







