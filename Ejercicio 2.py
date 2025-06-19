from scapy.all import *
import statistics
import time

def ping(host):
    print(f"Ping {host}")
    cantSent:int = 0
    cantRcv:int = 0
    lost:int = 0
    minimo:int = 1000
    maximo:int = 0
    rtts:list[int] = []    

    for i in range(0,10):  
        pkt = IP(dst=host, ttl=128)/ICMP()
        cantSent+=1
        start = time.time()
        reply = sr1(pkt, timeout=1, verbose=0)
        end = time.time()

        if reply:
            cantRcv+=1

            rtt = (end - start) * 1000
            rtts.append(rtt)

            if rtt > maximo:
                maximo = rtt

            if rtt < minimo:
                minimo = rtt
                
            print(f"Paquete {i+1}: Longitud = {len(reply)} bytes, RTT = {round(rtt, 2)} ms, TTL = {reply.ttl}")
            
        else:
            lost+=1
            print(f"Respuesta {i+1}: Tiempo de espera agotado")
    
    if rtts:
        promedio = statistics.mean(rtts)
        st = statistics.stdev(rtts) if len(rtts) > 1 else 0.0
    else:
        promedio = st = 0.0

    print("\n--- Estadísticas ---")
    print('Paquetes enviados = ' + str(cantSent))
    print('Paquetes recibidos = ' + str(cantRcv))
    print('Paquetes perdidos = ' + str(lost))
    print('Porcentaje perdidos = ' + str((lost/cantSent)*100) + '%')
 
    if cantRcv != 0:    # A menos que se hayan perdido todos los paquetes, exhibe estas estadisticas en la terminal
        print(f'RTT promedio = {promedio:.2f} ms')
        print(f'RTT máximo = {maximo:.2f} ms')
        print(f'RTT mínimo = {minimo:.2f} ms')
        print(f'Desvío estándar = {desviacion:.2f} ms')

    return

ping("google.com")
