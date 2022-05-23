# Esseallond Snarl

To run Snarl, begin by starting the server. This is done with  
the command   
./server  
this will run the server will all default values, possible values are below  
./server --levels FILE --clients N --wait N --observe --address IP --port NUM  

Once the server is started, the game will begin if N clients connect to the server  
before the timeout.   
The timeout resets every time a new client connects. To run a client use the command  
./client   
this will run the client with default values, possible values are below  
./client --address IP --port NUM

Once the determined number of clients are connected the game will begin.  
When a player's begins they will be told of their position.  
The must send back a value int,int in that format, no spaces, just two integers separated by commas.  
Any invalid moves sent will result in a skipped turn.

The level is over after everyone either exited or ejected. The next level will begin with everyone respawned.  
The game is over when all players are ejected or the final level is completed.

