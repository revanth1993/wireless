import DDPacket
import ExtractPacket
import HelloPacket,HelloReplyPacket
import socket
import time,sys
import threading
from datetime import datetime
from struct import *
import netifaces as ni

neighbors = {}
rib = {}
kill_all = 1
interface = ''

# on reception of hello reply packet update neighbors
def update_neighbors(srcip, s_mac, delay, age):
    # three conditions
    # 1. srcip not present in neighbors table update neighbors table and trigger a DD packet
    # 2. srcip already present delay is within the acceptable range update the delay
    # 3. srcip already present delay is way off, remove it from the neighbors table trigger a DD packet
    global neighbors
    if srcip not in neighbors:
        print "first entry in neighbors table and sending a DD packet"
        neighbors[srcip] = [s_mac,delay,age]
        print neighbors
        sendDD()

    else:
        print "updating table with new delay"
        neighbors[srcip] = [s_mac,delay,age]
        print neighbors

# on an update on local RIB send a DD packet
def sendDD():
    global interface
    global rib
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((interface,0))
    s.send(DDPacket.ddPacket(interface,rib))
    s.close()

# on reception of hello reply packet if triggers a change in the local RIB or on reception of DD packet
# which results in the change of local RIB update RIB

def updateRIB(neighbor_rib):
    # only if a DD packet is received this function is called, neighbor_rib is passed to the function which is extracted from
    # the extractpacketfields function, it is a dictionary with key as the destination ip and the values as cost, sequence number
    # next hop should be set in the RIB and send a DD packet
    pass

def sendHello():
    # periodically send hello packets through the interface
    global kill_all
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((interface,0))
    hellopacket = HelloPacket.helloPacket(interface)
    while kill_all:
        t = datetime.now()
        timestamp = pack('!3c',chr(((t.microsecond/100)/100)%100),chr((t.microsecond/100)%100),chr(t.microsecond%100))
        packet = hellopacket + timestamp
        s.send(packet)
        print "hello packet sent at ", t
        time.sleep(10)


def updateFIB():
    #update the host FIB
    pass

def listenSocket():
    global kill_all
    listen = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x800))
    while kill_all:
        packet = listen.recvfrom(65565)
        packet = packet[0]
        if ord(packet[23]) != 253:
            continue

        src_mac,dst_mac,eth_type,src_ip,dst_ip,dsdv_type,rib_neighbor = ExtractPacket.extractPacketFields(packet)


        if dsdv_type == 1:
            s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
            s.bind((interface,0))
            s.send(HelloReplyPacket.helloReplyPacket(interface,src_mac,src_ip,packet[35:38]))
            print "sent a hello reply packet to ",src_ip
            s.close()

        elif dsdv_type == 2:
            t = datetime.now()
            timestamp = ord(packet[35])*10000 + ord(packet[36])*100 + ord(packet[37])
            print "hello reply came from ",src_ip, t.microsecond
            delay = t.microsecond - timestamp
            update_neighbors(src_ip,src_mac,delay,10)

        elif dsdv_type == 3:
            updateRIB(rib_neighbor)


def main():

    global kill_all,interface,rib



    interface = sys.argv[1]

    # Intialise RIB
    # with local ip, set delay to 0, initiate a sequence number
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    rib[ip] = [ip,0,2]


    hellothread = threading.Thread(target=sendHello, args=())
    hellothread.start()

    listenthread = threading.Thread(target=listenSocket, args=())
    listenthread.start()

    x = raw_input()
    kill_all = 0
    hellothread.join(timeout = 1)
    listenthread.join(timeout = 1)




if __name__ == "__main__":
    main()

