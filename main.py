import DDPacket
import ExtractPacket
import HelloPacket,HelloReplyPacket
import socket
import time,sys
import threading
from datetime import datetime
from struct import *
import netifaces as ni
from netifaces import *

neighbors = {}
rib = {}
kill_all = 1
interface = ''

# on reception of hello reply packet update neighbors
def update_neighbors(srcip, s_mac, delay, flag):
    # three conditions
    # 1. srcip not present in neighbors table update neighbors table and trigger a DD packet
    # 2. srcip already present delay is within the acceptable range update the delay
    # 3. srcip already present delay is way off, remove it from the neighbors table trigger a DD packet
    global neighbors
    if srcip not in neighbors:
        print "first entry in neighbors table and sending a DD packet"
        neighbors[srcip] = [s_mac,delay,flag]
        print neighbors
        sendDD()

    else:
        print "updating table with new delay"
        neighbors[srcip] = [s_mac,delay,flag]
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

def updateRIB(srcip, neighbor_rib):
    # only if a DD packet is received this function is called, neighbor_rib is passed to the function which is extracted from
    # the extractpacketfields function, it is a dictionary with key as the destination ip and the values as cost, sequence number
    # next hop should be set in the RIB and send a DD packet
    #
    # algo for updating RIB  -- neighbors broadcast the ip addresses that they know of
    # 1) destination ip not present in local RIB - host first time learning about an ip
    # 2) destination ip already present
    #       a) check sequence number if it is less discard
    #       b) if it is equal and even update with the minimum delay
    #       c) if it is greater and odd neighbor is advertising that the destination ip is not reachable ?? how to tackle this?
    #           may be making the delay to a max value 9999, while updating the local FIB if the delay is 9999 dont add an entry

    # updating RIB delay should be a sum of delay that neighbor advertises and delay to the neighbor
    # next hop is the srcip parameter passed to the function

    global rib,neighbors
    change = 0

    print "updating RIB with neighbor ",neighbor_rib
    for entry in neighbor_rib:
        if entry not in rib:
            change = 1
            rib[entry] = [srcip,neighbor_rib[entry][0]+neighbors[srcip][1], neighbor_rib[entry][1]]
        else:
            sequence_number_neighbor = neighbor_rib[entry][1]
            delay_neighbor = neighbor_rib[entry][0]
            sequence_number_local = rib[entry][2]
            delay_local = rib[entry][1]
            delay_to_neighbor = neighbors[entry][1]
            if sequence_number_neighbor == sequence_number_local and delay_local != min(delay_local,delay_neighbor+delay_to_neighbor):
                change = 1
                rib[entry] = [srcip,neighbor_rib[entry][0],neighbor_rib[entry][1]]
            elif sequence_number_neighbor%2 != 0:
                change = 1
                rib[entry] = [srcip,neighbor_rib[entry][0],neighbor_rib[entry][1]]
    if change:
        sendDD()

def deadtimer():
    global kill_all, neighbors

    while kill_all:
        dead_neighbors = []
        for entry in neighbors:
            if neighbors[entry][1] == 0:
                continue
            elif neighbors[entry][2]:
                neighbors[entry][2] = 0
            else:
                dead_neighbors.append(entry)

        for dead_neighbor in dead_neighbors:
            print "neighbor considered dead ",dead_neighbor
            del neighbors[dead_neighbor]
        time.sleep(10)

def sendHello():
    # periodically send hello packets through the interface
    global kill_all
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((interface,0))
    hellopacket = HelloPacket.helloPacket(interface)
    while kill_all:
        t = datetime.now()
        stamp = (t.second%10)*100000 + t.microsecond/10
        timestamp = pack('!3c',chr(((stamp/100)/100)%100),chr((stamp/100)%100),chr(stamp%100))
        packet = hellopacket + timestamp
        s.send(packet)
        print "[HELLO] ", t
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
            #print "[HELLO REPLY] ",src_ip
            s.close()

        elif dsdv_type == 2:
            t = datetime.now()
            stamp_now = (t.second%10)*100000 + t.microsecond/10
            timestamp = ord(packet[35])*10000 + ord(packet[36])*100 + ord(packet[37])
            print "[HELLO REPLY] ",src_ip, t
            delay = stamp_now - timestamp
            update_neighbors(src_ip,src_mac,delay,1)

        elif dsdv_type == 3:
            print "[DD PACKET] ", src_ip, rib_neighbor
            if src_ip not in neighbors:
                print "No update, Neighborship not formed yet with ", src_ip
                continue
            updateRIB(src_ip, rib_neighbor)

def printRIB():
    global rib
    print "DstIP\t\t\tNextHop\t\t\tDelay\t\t\tSeq_Num"
    for dstip in rib:
        print str(dstip)+"\t\t\t"+str(rib[dstip][0])+"\t\t\t"+str(rib[dstip][1])+"\t\t\t"+str(rib[dstip][2])

def printNeighbors():
    global neighbors
    print "DstIP\t\t\tMAC\t\t\tDelay"
    for dstip in neighbors:
        print str(dstip)+"\t\t\t"+str(neighbors[dstip][0])+"\t\t\t"+str(neighbors[dstip][1])


def main():

    global kill_all,interface,rib

    interface = sys.argv[1]

    # Intialise RIB
    # with local ip, set delay to 0, initiate a sequence number
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    rib[ip] = [ip,0,2]
    neighbors[ip] = [ni.ifaddresses(interface)[AF_LINK][0]['addr'], 0 , 1]

    hellothread = threading.Thread(target=sendHello, args=())
    hellothread.start()

    deadtimerthread = threading.Thread(target=deadtimer, args=())
    deadtimerthread.start()

    listenthread = threading.Thread(target=listenSocket, args=())
    listenthread.start()

    x = raw_input("1. View neighbors 2. Routing information base 3. Stop & Exit")
    while(True):
        if x == '1':
            printNeighbors()
        elif x == '2':
            printRIB()
        elif x == '3':
            break
        x = raw_input("1. View neighbors 2. Routing information base 3. Stop & Exi")

    kill_all = 0
    hellothread.join(timeout = 1)
    listenthread.join(timeout = 1)




if __name__ == "__main__":
    main()

