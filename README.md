# Proxy-Cache_server

## Features
1. Caching:<br>
   The proxy server caches the content it retrieves from the web GET requests. If device wants to the same file, it retrieves it from the cache. 
   It's advantages includes: Reduced network traffic, Reduced fetching Time and increased network performance
   
2. Timeout handling:<br>
   It also has response timeout of 5s, if there's no response from the web server it automatically disconnects the  connection. This prevents the server from hanging

3. Multiple request handling:<br>
     The proxy server listen to multiple connections(max 5) simultenously. 


## Operation:
The server listens on port 8888 for client requests. Once the client establishes a connection and send a GET request, the server parses the request to extract the hostname and path(Host: example.com, Path: /index.html). 
The server proceed to check the path(filename) across the cache directory, if it checks out. it send the cached file to the client.
If there's no corresonding file in the cache, it forwards the request to the necessary web server to get  the needed file.

The response from the web server is cached in the cache folder before being sent to the client.


## Client-server side

   Get request from the web server(http://httpbin.org/get)
   
   ![Image](https://github.com/user-attachments/assets/075a4f9a-f16e-4597-bf65-7b9d7412fa4c)
   
   
   Get request from the proxy cache
   
   ![Image](https://github.com/user-attachments/assets/e7fde73e-c1df-4c33-bd2c-0af549cdb7b9)
   
   The web GET requests- curl
   
   ![Image](https://github.com/user-attachments/assets/e38d19f9-f0aa-40ed-96e3-d345949680f0)
