import socket,sys
from struct import *
import ExtractPacket as EP
def eth_header(packet):

    print "---------------ETHERNET HEADER----------------------"
    print "SRC_MAC : %0.2X:%0.2X:%0.2X:%0.2X:%0.2X:%0.2X" % (ord(packet[0]),ord(packet[1]),ord(packet[2]),ord(packet[3]),ord(packet[4]),ord(packet[5]))  
    print "DST_MAC : %0.2X:%0.2X:%0.2X:%0.2X:%0.2X:%0.2X" % (ord(packet[6]),ord(packet[7]),ord(packet[8]),ord(packet[9]),ord(packet[10]),ord(packet[11]))
    print "ETHER_TYPE : 0x%0.2X%0.2X"%(ord(packet[12]),ord(packet[13]))

    print "-----------------------------------------------"

def ip_header(ip_packet):
    print "---------------IP HEADER-----------------------"

    print "IP Version: " , (ord(ip_packet[0])>>4)
    print "IP Header Length: %d Bytes" % ((ord(ip_packet[0])&15)*4)
    print "QoS: " , (ord(ip_packet[1]))
    print "IP Packet Length: %d Bytes" % ((ord(ip_packet[2])<<8) + (ord(ip_packet[3])))
    print "TTL :" ,ord(ip_packet[8])
    print "IP Protocol: " , ord(ip_packet[9])
    print "Source IP: %d.%d.%d.%d " %(ord(ip_packet[12]),ord(ip_packet[13]),ord(ip_packet[14]),ord(ip_packet[15]))
    print "Destination IP: %d.%d.%d.%d " %(ord(ip_packet[16]),ord(ip_packet[17]),ord(ip_packet[18]),ord(ip_packet[19]))
    print "-----------------------------------------------"

def user_data(packet_data):
    print "----------------USER DATA------------------------"
    print "-------------------------------------------------"

def main():
    listen = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.htons(0x800))
    while True:
        packet = listen.recvfrom(65565)
        packet = packet[0]
        print "-----------"
        print EP.extractPacketFields(packet)
        print "-----------"
    #user_data(packet[20:])

main()
