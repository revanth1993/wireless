import socket, sys
from struct import *
import netifaces as ni
from netifaces import *


'''

                                IP HEADER

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version|  IHL  |Type of Service|          Total Length         |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Identification        |Flags|      Fragment Offset    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Time to Live |    Protocol   |         Header Checksum       |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                       Source Address                          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Destination Address                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+   ---------------------|
   |      Type     |           No. of entries in the database      |                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                        |
   |                          IP Address                           |     #Payload           |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                        |
   |           Delay               |     Sequence Number           |                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+  -----------------------





'''



def ddPacket(interface,rib):
    if interface not in ni.interfaces():
        return None

    S_MAC = ni.ifaddresses(interface)[AF_LINK][0]['addr'].split(":")
    S_MAC = pack('!6c',chr(int(S_MAC[0], 16)), chr(int(S_MAC[1],16)),  chr(int(S_MAC[2],16)) , chr(int(S_MAC[3],16)), chr(int(S_MAC[4],16)), chr(int(S_MAC[5],16)))
    D_MAC = pack('!6c',chr(int('ff', 16)), chr(int('ff',16)),  chr(int('ff',16)) , chr(int('ff',16)), chr(int('ff',16)), chr(int('ff',16)))
    ETH_TYPE = pack('!2c',chr(int('08',16)),chr(int('00',16)))

    ethernet_header = S_MAC+D_MAC+ETH_TYPE  # 14 bytes


    ip_v_ihl  = pack('!c',chr(int('45',16)))
    ip_tos = pack('!c',chr(int('00',16)))
    ip_tot_len = pack('!2c',chr(int('00',16)),chr(int('00',16)))
    ip_id = pack('!2c',chr(int('ff',16)),chr(int('ff',16)))
    ip_frag_off = pack('!2c',chr(int('00',16)),chr(int('00',16)))
    ip_ttl = pack('!c',chr(int('ff',16)))
    ip_proto = pack('!c',chr(253))
    ip_check = pack('!2c',chr(0),chr(0))

    Src_IP = ni.ifaddresses(interface)[ni.AF_INET][0]['addr'].split('.')

    ip_src = pack('!4c',chr(int(Src_IP[0])),chr(int(Src_IP[1])),chr(int(Src_IP[2])),chr(int(Src_IP[3])))
    ip_dst = pack('!4c',chr(224),chr(0),chr(0),chr(4))


    ip_header = ip_v_ihl + ip_tos + ip_tot_len + ip_id + ip_frag_off + ip_ttl + ip_proto + ip_check + ip_src + ip_dst

    payload = pack('!c',chr(3))

    return ethernet_header+ip_header+payload


def main():

    interface = sys.argv[1]
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    s.bind((interface,0))
    s.send(ddPacket(interface))


if __name__ == "__main__":
    main()

