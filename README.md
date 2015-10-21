# DNS-Proxy-Server
A DNS Proxy Server implementation in java. Store n recent DNS queries in HashMap. (n is user input)

===================================
System Requirements
===================================
1. The System running the Application must have Java 8.

===================================
Compiling and Running
===================================
   -------------------------------------
   DNSProxyServer -> DNSProxyServer.java
   -------------------------------------
   #javac DNSProxyServer.java
   
   #java DNSProxyServer 'IP of Nameserver' 'Port for opening Socket' 'Cache_Size'

   (All arguments without quotes)
   
   -> IP of Nameserver is the IP of your local DNS Server.
   
   -> Port number on which a temporary socket for connection between Terminal and you application should listen.
   
   -> The 'Cache_Size' is the number of entries you want to cache in the server.
