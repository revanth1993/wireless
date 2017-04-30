# DSDV routing protocol

Code should be run with super user privileges

Install netifaces using pip module

pip install netifaces

Each individual file of HelloPacket.py HelloReplyPacket.py DDPacket.py can be run independently to generate packets
using raw sockets

Run sudo python HelloPacket.py interfacename #generates a hellopacket and sends it out of the interfacename
    sudo python HelloReplyPacket.py interfacename #generates a helloreplypacket and sends it out of the interfacename
    sudo python DDPacket.py interfacename #generates a ddpacket and sends it out of the interfacename

Use wireshark to capture the packet and observe the fields

ExtractPacket.py has a utility function to extract the necessary fields of a packet received from the raw socket like source MAC, destination MAC etc.

To run the routing protocol

python dsdv.py interfacename

for ex: python dsdv.py eth0

the dsdv.py file does the following

creates three background threads

thread-1  hellotimer - sends hello packets every 10 seconds

thread-2  deadtimer  - poll neighbors every 15 seconds considers it dead if it doesnot recieve a helloreplypacket within those 15 seconds

thread-3  listensocket - creates a raw socket and listens to the incoming packets
                         for the listensocket thread, it has three conditions depending on the type of packet received
                          1) received hellopacket - send helloreplypacket
                          2) received helloreplypacket - update neighbors
                          3) received ddpacket - update routing information base and broadcast the change







