import DDPacket
import ExtractPacket
import HelloPacket
import socket
import time,sys
import threading

neighbors = {}
rib = {}

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

def sendHello(interface):
    # periodically send hello packets through the interface
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((interface,0))
    while True:
        HelloPacket.sendHelloPacket(s,interface)
        time.sleep(5)


def updateFIB():
    #update the host FIB
    pass



def main():

    interface = sys.argv[1]
    hellothread = threading.Thread(target=sendHello(),args=(interface))
    hellothread.start()

    x = raw_input()
    hellothread.join(timeout = 1)



if __name__ == "__main__":
    main()

