import telnetlib3
import asyncio
from equipos.raisecom import raisecom
from equipos.cisco import cisco
from equipos.huawei import huawei

IP_CISCO = "10.4.1.62"
IP_RAISECOM = "10.4.1.47"
IP_HUAWEI = "10.4.31.137"

IP_2608 = "10.4.191.112"
IP_RAX711C = "10.4.184.227"
IP_RAX721 = ""
IP_2924 = ""
IP_RAX711R = "10.5.4.38"

USER_MCA = "MCA"
USER_MCA_MIN = "mca"
USER_RAISECOM = "raisecom"
USER_HUAWEI = "Admin"

PASS_MCA = "M3tr0c4rr13r#"
PASS_RAISECOM = "raisecom"
PASS_HUAWEI = "admin@huawei.com"

async def proceso(ip):
    host = ip
    port = 23  

    # Establecer la conexión Telnet
    reader, writer = await telnetlib3.open_connection(host, port)

    #LEER EL PROMPT
    credentials = [{'user':USER_MCA, 'pass' : PASS_MCA}, {'user':USER_MCA_MIN, 'pass':PASS_MCA}]
    prompt = b"#"
    modelo = ""


    if await find(reader, b"Login:"):
        modelo = "raisecom"
        credentials.append({'user':USER_RAISECOM, 'pass':PASS_RAISECOM})
    elif await find(reader, b"Username: "):
        modelo = "cisco"
    elif await find(reader, b"Username:"):
        modelo = "huawei"
        credentials.append({'user':USER_HUAWEI, 'pass':PASS_HUAWEI})
        prompt = b">"

    for i in credentials:
        username = i['user'] ; password = i['pass']
        #print(i)
        #inicio de sesion
        #await reader.readuntil(login_tag)
        writer.write(username + "\n")

        # Contraseña
        await reader.readuntil(b"Password:")
        writer.write(password + "\n")

        if await find(reader, b"#") or await find(reader, b"<"):
            print("Ya entramos")
            break

    if modelo == "raisecom":
        await raisecom(reader, writer)
    elif modelo == "huawei":
        await huawei(reader, writer)
    elif modelo == "cisco":
        await cisco(reader, writer)

    writer.write("exit\n")
    await writer.drain()
    writer.close()


async def find(reader, word, max_time=1):
    try:
        response = await asyncio.wait_for(reader.readuntil(word), timeout=max_time)
        return response.decode('utf-8')
    except:
        return False

async def isAN(prompt):
    if "AN".encode('utf-8') in prompt:
        print("Es un AN")
    else:
        print("Es un CPE")

async def main():
    await proceso(IP_2608)


asyncio.run(main())

    #VALIDACION DE PUERTO RAISECOM
"""writer.write("show run int port-list 27\n")
    if await find(reader, b"!"):
        print("Puerto ocupado")
    else:
        print("Puerto disponible")
    output = await reader.readuntil(b"#")"""

#print(output.decode('utf-8'))

"""#Aplicar comandos del json
for i in comandos[modelo]:
    print(comandos[modelo][i])
    writer.write(comandos[modelo][i] + "\n")
    output = await reader.readuntil(b"#") 
    print(output.decode('utf-8'))"""

#VALIDACION DE VLAN RAISECOM
"""vlan = b"1199"
writer.write("show vlan "+ str(vlan)+ "\n")
print("show vlan "+ vlan.decode() + "\n")
if await find(reader, vlan.decode()):
    print("VLAN ocupada")
else:
    print("VLAN disponible")
output = await reader.readuntil(b"#") """

#print(output.decode('utf-8'))


"""writer.write("show bridge-domain 1199\n")

# Leer la salida del comando
output = await reader.readuntil(b"#") 
#display += output)

texto = output.decode('utf-8')

# Depurar buffer por completo
#print(output.decode('utf-8'))

if "GigabitEthernet0/0/1 " in texto:
    writer.write("show running-config interface GigabitEthernet0/0/1 \n")
    output = await reader.readuntil(b"#") 
    print(output.decode('utf-8'))

#await reader.readuntil(b"#")  """

"""
# Enviar comando
writer.write("show version\n")

output = await reader.readuntil(b" --More-- ")
if output :
    display = output
    print("smn")
writer.write(chr(32))

output = await reader.readuntil(b" --More-- ")
if output :
    display += output
    print("smn")
writer.write(chr(32))

print("hooa")


writer.write("show bridge-domain 1199\n")

# Leer la salida del comando
output = await reader.readuntil(b"#") 
#display += output)

texto = output.decode('utf-8')

# Depurar buffer por completo
#print(output.decode('utf-8'))

if "GigabitEthernet0/0/1 " in texto:
    writer.write("show running-config interface GigabitEthernet0/0/1 \n")
    output = await reader.readuntil(b"#") 
    print(output.decode('utf-8'))
"""


"""
writer.write("configure terminal\n")
await reader.readuntil(b"#")  

#Configuracion
writer.write("interface GigabitEthernet0/0/2\n")
await reader.readuntil(b"#")  
writer.write("description PRUEBA-PYTHON\n")
await reader.readuntil(b"#")  
writer.write("end\n")
await reader.readuntil(b"#")  

#Resultado
writer.write("show run interface GigabitEthernet0/0/2\n")
output = await reader.readuntil(b"#") 
print(output.decode('utf-8'))

"""

#Inhabilitar escritor


# Ejecutar el bucle de eventos para conectar y obtener la salida

"""# Paso 1: Abrir el archivo en modo lectura
    with open('comandos.json', 'r') as archivo_json:
        # Paso 2: Cargar el contenido JSON desde el archivo
        comandos = json.load(archivo_json)"""