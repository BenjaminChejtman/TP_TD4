from scapy.all import *
def ping(host):
    print(f"Ping {host}")
    #COMPLETAR
 return

ping("google.com")

def unpkt(host):
    ping = IP(dst = host)/TCP(dport=80)
    reply = sr1(ping, timeout=1)

    if reply 
