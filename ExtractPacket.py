import socket,sys
from struct import *

def getIP(packet):
    return str(ord(packet[0]))+'.'+str(ord(packet[1]))+'.'+str(ord(packet[2]))+'.'+str(ord(packet[3]))

def extractPacketFields(packet):

    src_mac = hex(ord(packet[0]))[2:]+':'+hex(ord(packet[1]))[2:]+':'+hex(ord(packet[2]))[2:]+':'+hex(ord(packet[3]))[2:]+':'+hex(ord(packet[4]))[2:]+':'+hex(ord(packet[5]))[2:]
    dst_mac = hex(ord(packet[6]))[2:]+':'+hex(ord(packet[7]))[2:]+':'+hex(ord(packet[8]))[2:]+':'+hex(ord(packet[9]))[2:]+':'+hex(ord(packet[10]))[2:]+':'+hex(ord(packet[11]))[2:]
    eth_type = hex(ord(packet[12]))+hex(ord(packet[13]))[2:]


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


