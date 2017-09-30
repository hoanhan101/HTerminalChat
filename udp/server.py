#!/usr/bin/env python3
"""
    broad_serve2.py - UDP server that listens for multicast messages on port 9000 and prints them out and responds
                      to the sender with the message that was sent.
    Author: Andrew Cencini (acencini@bennington.edu)
    Date: 9/17/2017
"""
import socket
import struct

MCAST_GRP = '224.0.0.1'		# listen to all hosts on the local subnet
MCAST_PORT = 9000		# listen on UDP port 9000

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# lets go of the socket after a crash
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind to all active network interfaces on the given UDP port
s.bind(('', MCAST_PORT))

# this is needed to set up the multicast group as an address to listen to
# we get the mcast address in network order (aton) - INADDR_ANY in this case
# just means listen on all local interfaces; we pack this into mreq so 
# we can listen to all callers
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

#client_addresses = []
#
#while True:
#    data, addr = s.recvfrom(10240)
#    
#    if addr not in client_addresses:
#        client_addresses.append(addr)
#    
#
#    data = data.decode()
#    print("{0} received: {1}".format(addr[0], data))
#
#    print(client_addresses)
#    # bounce the message back to the caller
#    for client_addr in client_addresses:
#        s.sendto(data.encode(), client_addr)
#        print("Sent {0} to {1}".format(data, addr[0]))


client_addresses = {}

while True:
    data, addr = s.recvfrom(10240)

    data = data.decode()
    if data[0] == '@':
        #add the username info to client_addresses
        #print(data)
        client_addresses[addr[0]] = [data]
        client_addresses[addr[0]].append(addr[1])
        print('User {0} has connected.'.format(data))
    else:
        user = client_addresses[addr[0]][0]
        print("RECEIVED {0} FROM {1}".format(data, user))

    client_addresses[addr[0]][1] = addr[1]

    print(client_addresses)
    # bounce the message back to the caller
    for IP, port in client_addresses.items():
        if IP == addr[0]:
            pass
        else:
            s.sendto(data.encode(), (IP, port))
            print("SENT {0} TO {1}".format(data, IP))
