import socket

target_host = "X.X.X.X"
target_port = XXXX

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host, target_port))

# send some data
client.send(b"GET / HTTP/1.1\r\nHost: X.X.X.X\r\n\r\n")

# receive some data
response = client.recv(4096)

print(response.decode())
client.close()
