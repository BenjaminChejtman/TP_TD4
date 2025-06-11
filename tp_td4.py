from scapy.all import *
import statistics
import time

def snd_pkt(host, pkt_ttl):
    pkt = IP(dst=host, ttl=pkt_ttl)/ICMP()
    reply = sr1(pkt, timeout=2, verbose=0)
    return reply

def ping(host, rango, pkt_ttl):    
    mensaje = ''
    cantSent:int = 0
    cantRcv:int = 0
    lost:int = 0
    minimo:int = 1000
    maximo:int = 0
    rtts:list[int] = []    

    for i in range(0, rango):   # Cosnulta: Cuantos paquetes tenemos que enviar?
        cantSent+=1
        start = time.time()
        reply = snd_pkt(host, pkt_ttl)
        end = time.time()

        if reply:
            cantRcv+=1
            lng = len(reply)
            rtt = (end - start) * 1000
            ttl = reply.ttl
            
            rtts.append(rtt)
            
            if rtt > maximo:
                maximo = rtt
            
            if rtt < minimo:
                minimo = rtt
        
        else:
            lost+=1
            
    if rtts:
        promedio = statistics.mean(rtts)
        st = statistics.stdev(rtts) if len(rtts) > 1 else 0.0
        
    else:
        promedio = st = 0.0

    mensaje = ('Paquetes enviados = ' + str(cantSent) + '\nPaquetes recibidos = ' + str(cantRcv) + '\nPaquetes perdidos = ' + str(lost) + '\nPorcentaje perdidos = ' + str((lost/cantSent)*100) + '%' + '\nRTT promedio = ' + str(promedio) + 'ms' + '\nRTT maximo = ' + str(maximo) + 'ms' + '\nRTT minimo = ' + str(minimo) + 'ms' + '\nDesvio Standard = ' + str(st))

    return mensaje

print(ping('8.8.8.8', 2, 5))
