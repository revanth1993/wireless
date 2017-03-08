import socket,sys
from struct import *
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

packet = ''

src_ip = '10.0.2.15'
dst_ip = '10.0.2.15'

ip_ihl = 5
ip_ver = 4
ip_tos = 0
ip_tot_len = 0
ip_id = 54321
ip_frag_off = 0
ip_ttl = 255
ip_proto = 253
ip_check = 0
ip_saddr = socket.inet_aton(src_ip)
ip_daddr = socket.inet_aton(dst_ip)
ip_ihl_ver = (ip_ver<<4) + ip_ihl
ip_header = pack('!BBHHHBBH4s4s', ip_ihl_ver,ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto , ip_check, ip_saddr,ip_daddr)

packet = ip_header+'user data'
s.sendto(packet, (dst_ip,0)) 


