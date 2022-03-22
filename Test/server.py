import socket
from _thread import *
import sys

def parsePos(data):
    try:
        d = data.split(":")[1].split(",")
        return int(d[0]), int(d[1])
    except:
        return 0,0

def colides(c1, c2):
    x1, y1 = c1
    x2, y2 = c2

    if (x2 <= x1 + 50 and y2 <= y1 + 50):
        return True
    
    return False


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '127.0.0.1'
port = 32016

server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:150,150"]
def threaded_client(conn):
    global currentId, pos
    conn.send(str.encode(currentId))
    currentId = "1"
    reply = ''
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply
                
                if id == 0: nid = 1
                if id == 1: nid = 0

                coords1 = parsePos(pos[0])
                coords2 = parsePos(pos[1])

                reply = pos[nid][:]
                print("Sending: " + reply)

                if (colides(coords1, coords2)):
                    conn.sendall(str.encode('gameover'))

            conn.sendall(str.encode(reply))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))