import socket
from _thread import *
import time

server = "79.182.68.58"
port = 5555
conn_list=[]
currentPlayer = 0
def run():
    global conn_list
    global currentPlayer
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind(("", port))
    except socket.error as e:
        str(e)
    s.listen(2)
    print("Waiting for a connection, Server Started")
    currentPlayer = 0
    conn_list=[]
    players = ["0%0$0*", "0%0$0*"]
    def threaded_client(conn, player):
        global wait
        global conn_list
        global currentPlayer
        reply = ""
        conn.send(str.encode("hy"))
        while True:
            try:
                data = conn.recv(2048).decode()
                players[player] = data

                if not data:
                    print("Disconnected")
                    conn.sendall(str.encode("lost"))
                    break
                else:
                    if player == 1:
                        reply = players[0]
                    else:
                        reply = players[1]

                conn.sendall(str.encode(reply))
            except:
                break

        print("Lost connection")
        for i in conn_list:
            i.close()
        if len(conn_list) ==1:
            currentPlayer=0
        conn_list.clear()
    while True:
        if currentPlayer==2:
            if conn_list==[]:
                break
            print (len(conn_list))
            time.sleep(1)
        else:
            conn, addr = s.accept()
            conn_list.append(conn)
            print("Connected to:", addr)
            start_new_thread(threaded_client, (conn, currentPlayer))
            currentPlayer += 1

while True:
    run()