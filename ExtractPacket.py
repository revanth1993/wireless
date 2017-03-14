import socket,sys
from struct import *


def extractPacketFields(packet):

    if ord(packet[23]) == 253:

        src_mac = hex(packet[0])[2:]+':'+hex(packet[1])[2:]+':'+hex(packet[2])[2:]+':'+hex(packet[3])[2:]+':'+hex(packet[4])[2:]+':'+hex(packet[5])[2:]
        dst_mac = hex(packet[6])[2:]+':'+hex(packet[7])[2:]+':'+hex(packet[8])[2:]+':'+hex(packet[9])[2:]+':'+hex(packet[10])[2:]+':'+hex(packet[11])[2:]
        eth_type = hex(packet[12])+hex(packet[13])[2:]


        src_ip = ord(packet[26])+'.'+ord(packet[27])+'.'+ord(packet[28])+'.'+ord(packet[29])
        dst_ip = ord(packet[30])+'.'+ord(packet[31])+'.'+ord(packet[32])+'.'+ord(packet[33])
        dsdv_type = ord(packet[34])
        return src_mac,dst_mac,eth_type,src_ip,dst_ip,dsdv_type
