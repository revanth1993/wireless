import DDPacket
import ExtractPacket
import HelloPacket,HelloReplyPacket
import socket
import time,sys
import threading

neighbors = {}
rib = {}
kill_all = 1
interface = ''

# on reception of hello reply packet update neighbors
def update_neighbors(srcip, s_mac, delay,age):
    neighbors[srcip] = [s_mac,delay,age]

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
    while kill_all:
        HelloPacket.sendHelloPacket(s,interface)
        time.sleep(5)


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
            print "received a hello packet"
            s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
            s.bind((interface,0))
            HelloReplyPacket.sendHelloReplyPacket(interface,dst_mac,dst_ip)
            s.close()

        elif dsdv_type == 2:
            print "received hello reply"
            delay = 1
            update_neighbors(src_ip,src_mac,1,10)

        elif dsdv_type == 3:
            updateRIB(packet)


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

