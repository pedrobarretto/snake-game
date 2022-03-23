import socket
from _thread import *
import sys
import pickle
from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL) 

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
# pos = ["0:50,50", "1:150,150"]
model = {
    'id': currentId,
    'snake_body': [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			],
    'snake_body2': [[100, 50],
			[90, 50],
			[80, 50],
			[70, 50]
			],
    'snake_position': [100, 50],
    'snake_position2': [100, 50],
    'fruit_position': [10, 10],
    'score': 0,
    'score2': 0
}
def threaded_client(conn):
    global currentId, snake_pos
    # conn.send(str.encode(currentId))
    conn.sendall(pickle.dumps(model))
    currentId = "1"
    reply = {}
    while True:
        try:
            data = pickle.loads(conn.recv(1000000000000))
            print('server data: ', data)
            # reply = data.decode('utf-8')
            if not data:
                conn.send(str.encode("Goodbye"))
                break
            else:
                print("Recieved: " + data)
                # arr = reply.split(":")
                # id = int(arr[0])
                # pos[id] = reply
                id = data.id
                
                if id == 0: nid = 1
                if id == 1: nid = 0

                if data.id == 0:
                    model.snake_position2 = data.snake_position2
                    model.snake_body2 = data.snake_body2
                    model.score2 = data.score2
                else:
                    model.snake_position = data.snake_position
                    model.snake_body = data.snake_body
                    model.score = data.score

                # coords1 = parsePos(pos[0])
                # coords2 = parsePos(pos[1])

                # reply = pos[nid][:]
                # era data
                print("Sending: " + data)

                if (colides(coords1, coords2)):
                    conn.sendall(str.encode('gameover'))

            # conn.sendall(str.encode(reply))
            # era data
            conn.sendall(pickle.dumps(data))
        except:
            break

    print("Connection Closed")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn,))