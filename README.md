server.client
=============

A simple server and client in python using the gevent library for concurrency. 

**overview & my process**
This document includes my initial software design, my notes after development of the applications and thoughts on what logical next steps would be. 

Outside of research on python and go languages prior to starting the design phase (both are/were new to me) I spent about 2-3 hours thinking through the architecture. I then spent around 10 hours or so writing, testing and debugging the  applications. And then a little extra to touch this wonderful document up! The intention here was to stay as reasonably close to the 8-10 hour limit suggested for development of this project. Given that I'm less experienced than most candidates I gave myself more time for upfront research and planning. 

setup
=============
The applications are dependent on the following libraries and has only been tested on python version 2.7.4:
* gevent
* sys
* shlex

Both shlex and sys are default in this version of python. To install gevent, use pip or easy install. 
pip install gevent
or
easy_install gevent

To install pip or easy_install use your linux distro's package manager (eg: yum, apt). For example, apt-get install python-pip.

basic usage
=============
To run the server: 
python servermain.py <hostname> <port>
example: python servermain.py 127.0.0.1 23400

To run the client:
python clientmain.py <serverhost> <serverport>
example: python clientmain.py 127.0.0.1 23400

phase 1: initial architecture design & thought process
=============
This are my original notes on the planned system architecture before developing the applications. I have cleaned up the format and brushed up the writing after finishing the application. Deviations from the original plan in this section are noted with the 'POST NOTE:' comments. These will be elaborated on in the implementation, decisions & notes section.

* **system purpose**
To allow for real time notifications between two lightweight python applications: a server and a client. 

* **proposed system design**
The system is comprised of two interfacing python applications, a client and a server Both rely on the the gevent library for concurrency. The client application can interact with the server in the following ways:
* connect to a running instance
* send messages to and receive messages from the server
* create channels
* subscribe to existing channels
* publish messages to channels

The server application is designed to:
* receive incoming connections from multiple concurrent instances of the client application
* receive multiple concurrent messages from connected clients
* instantiate and house 'channels' to which clients can subscribe, publish to and receive messages from
* messages are text (ideally would handle json) 

* **the server**
The server service application is to acheive the functionality above through the implementation three primary components and one optional component (implemented as classes): ServerListener, ConnectionHandler, ClientManger, (ServerManager) (optional if time allows - POST NOTE: time did not allow). 
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

	ServerManager (POST NOTE: not implemented)
		Maintains a list of Servers running simultaneously (within the same memory). To be instantiated on server start, and polls for other server processes running and exchanges basic information.
			Server process_id

		Could potential round robin client connection requests based on load...

* **the client**
* two modules: sender and receiver
* ConnectionRequest
*	MessageSend
*	MessageReceive

  Client
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

**phase 2: implementation, descisions and notes**
=============
In the end, the application largely followed the initial design outlined with the exception of a few notable exclusions:
* concurrent running of multiple server instances
* handling of JSON payloads

* **why python, gevent, OOP and other stuff**
Python was chosen over go for ease of development (time constraint), more thorough documentation available and more pervasive adoption. The server's top level subcomponents are implemented as objects to allow for logical clarity, modularity of functionality and abstraction of concepts. Similarly, I chose to use the gevent library for socket, server and 'threading' (greenlets are not true threads, but microthreads that all run in a single thread, swithing to emulate true concurrency - my current understanding at least!). This choice was made to lessen development time, though it came at the expense of my fully understanding the underlying implementation of sockets, servers and threading in python. Given more time, I would likely choose to rewrite this using python threads, or even go. 

At a more conceptual level, I chose to go with an object orientation, 1. because I am more familiar with OOP than functional programming. Though, for the purpose of a light client server I might reconsider. Functional programming is still new to me but the idea of functions as first class objects is very powerful, and might serve well in this case (though in some cases, I do pass functions as parameters since python can do this).   

A single consumer and producer model was chosen for the client for elegance and logical inclusion. The components are unified logically (abstracted to overarching client entity), but separated functionally (modularized into independent functions). 

I chose not to very sparingly comment the code, since I find it self-documentating and short/simple enough to not warrant it.

Though I'm sure there are others, there is one known bug I was unable to resolve given my trying to stay within a reasonable timeline: if multiple clients are subscribed to a channel, and a message is published to the channel, all clients subscribed receive the message. But, the message isn't displayed immediately; it only displays on input on the subsequent message from the client. This is because of the way the receiver is implemented, and I just couldn't work it out in time :(

* **next steps & time constraints** 
If I had more time, and continued down the path I chose here there are some features and structural changes I would like to add in:
* use setuptools for installation and run
* allow for distributed servers, with either a master message queue or entirely distrobuted design (each server treats the other like a different class of client)
  * load balancing based on number of clients connected to each server
* accept JSON payloads, this would be the first I would want to tackle
* much improved exception handling and user feedback
  * particularly on handling invalid input, or on dropped client/server connections
* restructure the app into main and class files, and use setuptools for install. This seems a bit redundant almost, due to the brevity of the single .py files. 
* client to client discovery and messaging (the former of these has the data structures in place on the server side, but time did not allow to continue)

THANK YOU!
=============




