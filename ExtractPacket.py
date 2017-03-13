import socket,sys
from struct import *


def extractPacketFields(packet):

    if ord(packet[23]) == 253:

        src_mac = hex(packet[0])[2:]+hex(packet[1])[2:]+hex(packet[2])[2:]+hex(packet[3])[2:]+hex(packet[4])[2:]+hex(packet[5])[2:]
        dst_mac = hex(packet[6])[2:]+hex(packet[7])[2:]+hex(packet[8])[2:]+hex(packet[9])[2:]+hex(packet[10])[2:]+hex(packet[11])[2:]
        eth_type = hex(packet[12])+hex(packet[13])[2:]


        src_ip = hex(packet[26])[2:]+hex(packet[27])[2:]+hex(packet[28])[2:]+hex(packet[29])[2:]
        dst_ip = hex(packet[30])[2:]+hex(packet[31])[2:]+hex(packet[32])[2:]+hex(packet[33])[2:]

