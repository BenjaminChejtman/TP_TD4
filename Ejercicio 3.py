from scapy.all import *
import statistics
import time

def ping(host):
    print(f"Ping {host}")
    cantSent = 0
    cantRcv = 0
    lost = 0
    minimo = 1000
    maximo = 0
    rtts = []

    # Diccionario para interpretar códigos de error de ICMP tipo 3
    error_codes = {
        0: "Destination Network Unreachable",
        1: "Destination Host Unreachable",
        2: "Destination Protocol Unreachable",
        3: "Destination Port Unreachable",
        9: "Network Administratively Prohibited",
        10: "Host Administratively Prohibited"
    }

    for i in range(50):
        pkt = IP(dst=host, ttl=128)/ICMP()
        cantSent += 1
        start = time.time()
        reply = sr1(pkt, timeout=1, verbose=0)
        end = time.time()

        if reply:
            icmp_layer = reply.getlayer(ICMP)

            if icmp_layer.type == 0:    # El paquete llego correctamente
                cantRcv += 1
                rtt = (end - start) * 1000
                rtts.append(rtt)
                minimo = min(minimo, rtt)
                maximo = max(maximo, rtt)
                print(f"Respuesta {i+1}: Longitud = {len(reply)} bytes, RTT = {round(rtt, 2)} ms, TTL = {reply.ttl}")

            elif icmp_layer.type == 3:   # Hubo error en la respuesta ICMP de tipo 3, Destination Unreachable
                code = icmp_layer.code
                mensaje = error_codes.get(code, f"Código de error desconocido ({code})")
                lost += 1
                print(f"Respuesta {i+1}: Error ICMP tipo 3 - {mensaje}")

            else:   # Hubo otro tipo de error
                lost += 1
                print(f"Respuesta {i+1}: ICMP tipo inesperado ({icmp_layer.type})")

        else:  # Se perdio el paquete
            lost += 1
            print(f"Respuesta {i+1}: Tiempo de espera agotado")

    if rtts:
        promedio = statistics.mean(rtts)
        desviacion = statistics.stdev(rtts) if len(rtts) > 1 else 0.0    // Calcula el RTT promedio y su Desvio
    else:
        promedio = desviacion = minimo = maximo = 0.0
        
    print("\n--- Estadísticas ---")    // Exhibe las estadisticas de los paquetes enviados
    print(f'Paquetes enviados = {cantSent}')
    print(f'Paquetes recibidos = {cantRcv}')
    print(f'Paquetes perdidos = {lost}')
    print(f'Porcentaje perdidos = {(lost / cantSent) * 100:.2f}%')
    
    if cantRcv != 0:    // A menos que se hayan perdido todos los paquetes, exhibe estas estadisticas en la terminal
        print(f'RTT promedio = {promedio:.2f} ms')
        print(f'RTT máximo = {maximo:.2f} ms')
        print(f'RTT mínimo = {minimo:.2f} ms')
        print(f'Desvío estándar = {desviacion:.2f} ms')


ping("8.8.8.8")    // Ejemplo de entrada
