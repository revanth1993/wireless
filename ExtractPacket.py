import socket,sys
from struct import *

def getIP(packet):
    return str(ord(packet[0]))+'.'+str(ord(packet[1]))+'.'+str(ord(packet[2]))+'.'+str(ord(packet[3]))

def extractPacketFields(packet):

    if not ord(packet[23]) == 253:
        return

    dst_mac = format(ord(packet[0]),'02x') + ':' + format(ord(packet[1]),'02x') + ':' + format(ord(packet[2]),'02x') + ':' + format(ord(packet[3]),'02x') + ':' + format(ord(packet[4]),'02x') + ':' +format(ord(packet[5]),'02x')
    src_mac = format(ord(packet[6]),'02x') + ':' + format(ord(packet[7]),'02x') + ':' + format(ord(packet[8]),'02x') + ':' + format(ord(packet[9]),'02x') + ':' + format(ord(packet[10]),'02x') + ':' +format(ord(packet[11]),'02x')
    eth_type = format(ord(packet[12]),'02x') + format(ord(packet[13]),'02x')


    src_ip = str(ord(packet[26]))+'.'+str(ord(packet[27]))+'.'+str(ord(packet[28]))+'.'+str(ord(packet[29]))
    dst_ip = str(ord(packet[30]))+'.'+str(ord(packet[31]))+'.'+str(ord(packet[32]))+'.'+str(ord(packet[33]))
    dsdv_type = ord(packet[34])

    rib_neighbor = {}

    if dsdv_type == 3:
        entries = ord(packet[35])
        start = 38

        for entry in xrange(entries):
            rib_neighbor[getIP(packet[start:start+4])] = [int(packet[start+5]+packet[start+6],16),int(packet[start+7]+packet[start+8],16)]
            start += 8*entry

    return src_mac,dst_mac,eth_type,src_ip,dst_ip,dsdv_type,rib_neighbor


