import DDPacket

neighbors = {}
rib = {}

def update_neighbors(srcip, s_mac, delay,age):
    neighbors[srcip] = [s_mac,delay,age]

def sendDD(sending_socket,interface):
    sending_socket.send(DDPacket.ddPacket(interface,rib))
