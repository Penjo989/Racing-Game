import socket
from _thread import *
import threading
import time
import pygame
addr_list=[]
players=[]
restart = False
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 5555
currentPlayer = 0
try:
    s.bind(("", port))
    print("server running")
except socket.error as e:
    str(e)
def run():
    global restart
    global addr_list
    global players
    restart = False
    currentPlayer = 0
    addr_list=[]
    players = ["0%0$0* &", "0%0$0* &"]
    print("waiting for connection")
    def get(address):
        global players
        global addr_list
        global restart
        while True:
            if currentPlayer==2:
                try:
                    data, addr = s.recvfrom(64)
                    if data.decode() == "disconnect":
                        restart = True
                        break
                    if addr ==addr_list[0]:
                        players[0]=data.decode()
                        s.sendto(str.encode(players[1]), addr)
                    elif currentPlayer ==2:
                        players[1]=data.decode()
                        s.sendto(str.encode(players[0]), addr)
                except:
                    pass

        print("Lost connection from " ,address)
    while not restart:
        if currentPlayer==2:
            time.sleep(1)
        else:
            data, addr = s.recvfrom(64)
            if addr in addr_list:
                if data.decode() == "disconnect":
                    restart = True
                else:
                    players[0]= data.decode()
            else:
                s.sendto(str.encode(players[currentPlayer]), addr)
                addr_list.append(addr)
                print("Connected to:", addr)
                start_new_thread(get, (addr,))
                currentPlayer += 1
                if currentPlayer==1:
                    print("waiting for connection")
    print("Server Is Down")

while True:
    run()
    print("Restarting")
    time.sleep(5)
