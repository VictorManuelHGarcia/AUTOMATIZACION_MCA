import ipaddress
import re

def get_available_ips(network_segment):
    try:
        network = ipaddress.IPv4Network(network_segment, strict=False)
        available_ips = [str(ip) for ip in network.hosts()][1:]
        return available_ips
    except ValueError:
        return None

# Ejemplo de uso


def validar_segmento_red(segmento):
    patron = r'^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\/(3[0-2]|[12]?[0-9])$'
    return re.match(patron, segmento) is not None

"""#segmento = "192.168.1.1/32"
if validar_segmento_red(segmento):
    print("Segmento de red válido.")
else:
    print("Segmento de red inválido.")"""


"""network_segment = "192.168.1.0/27"
available_ips = get_available_ips(network_segment)

if available_ips:
    print("Direcciones IP disponibles (excepto la primera IP utilizable):")
    for ip in available_ips:
        print(ip)
else:
    print("Segmento de red no válido.")"""
