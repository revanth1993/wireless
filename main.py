import DDPacket
import ExtractPacket
import HelloPacket,HelloReplyPacket
import socket
import time,sys
import threading
from datetime import datetime
from struct import *

neighbors = {}
rib = {}
kill_all = 1
interface = ''

# on reception of hello reply packet update neighbors
def update_neighbors(srcip, s_mac, delay,age):
    if srcip not in neighbors:
        print "updating neighbors table"
        neighbors[srcip] = [s_mac,delay,age]
        print neighbors

# on an update on local RIB send a DD packet
def sendDD(sending_socket,interface):
    sending_socket.send(DDPacket.ddPacket(interface,rib))

# on reception of hello reply packet if triggers a change in the local RIB or on reception of DD packet
# which results in the change of local RIB update RIB

def updateRIB(packet):
    src_mac,dst_mac,eth_type,src_ip,dst_ip,dsdv_type,rib_neighbor = ExtractPacket.extractPacketFields(packet)

    if dsdv_type == 2:
        # hello reply packet update the local RIB and neighbors data structure get the timer
        pass
    if dsdv_type == 3:
        # DD packet updating RIB logic goes here
        pass

def sendHello():
    # periodically send hello packets through the interface
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((interface,0))
    packet = HelloPacket.helloPacket(interface)
    while kill_all:
        t = datetime.now()
        timestamp = pack('!3c',chr(((t.microsecond/100)/100)%100),chr((t.microsecond/100)%100),chr(t.microsecond%100))
        packet += timestamp
        s.send(packet)
        print "hello packet sent at ", t
        time.sleep(10)


def updateFIB():
    #update the host FIB
    pass

def listenSocket():
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
            s.send(HelloReplyPacket.helloReplyPacket(interface,src_mac,src_ip,packet[24:27]))
            print "sent a hello reply packet to ",src_ip
            s.close()

        elif dsdv_type == 2:
            t = datetime.now()
            timestamp = ord(packet[24])*100000 + ord(packet[25])*1000 + ord(packet[26])
            print "hello reply came from ",src_ip, t
            delay = t.microsecond - timestamp
            update_neighbors(src_ip,src_mac,delay,10)

        elif dsdv_type == 3:
            updateRIB(rib_neighbor)


def main():

    global kill_all,interface

    interface = sys.argv[1]



    hellothread = threading.Thread(target=sendHello,args=())
    hellothread.start()

    listenthread = threading.Thread(target=listenSocket, args=())
    listenthread.start()

    x = raw_input()
    kill_all = 0
    hellothread.join(timeout = 1)
    listenthread.join(timeout=1)




if __name__ == "__main__":
    main()

