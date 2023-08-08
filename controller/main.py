import telnetlib3
import asyncio
from equipos.raisecom import raisecom
from equipos.cisco import cisco
from equipos.huawei import huawei


#CREDENCIALES
USER_MCA = "MCA"
USER_MCA_MIN = "mca"
PASS_MCA = "M3tr0c4rr13r#"

USER_RAISECOM = "raisecom"
PASS_RAISECOM = "raisecom"

USER_HUAWEI = "Admin"
PASS_HUAWEI = "admin@huawei.com"

TACACS_USER = bytes.fromhex("726f647269676f2e6469617a").decode('utf-8')
TACACS_PASS = bytes.fromhex("686f6c613132333435363839313040").decode('utf-8')

#EQUIPOS DE PRUEBA

#RAISECOM
IP_LAB2924 = "10.4.1.47"
IP_RAX711C = "10.4.184.227"
IP_RAX721 = "10.4.169.146"
IP_RAX711R = "10.5.4.38"
IP_2608 = "10.4.191.112"
IP_TEPIC = "10.4.130.40"
#CISCO
IP_CISCO = "10.4.1.62"
IP_ME = "10.4.37.133"

#HUAWEI
IP_HUAWEI = "10.4.31.137"



#FUNCION PARA CADA IP
async def proceso(ip):
    host = ip
    port = 23  
    limit = 3
    credentials = [{'user':USER_MCA, 'pass' : PASS_MCA}, 
                   {'user':USER_RAISECOM, 'pass':PASS_RAISECOM}, 
                   {'user':USER_HUAWEI, 'pass':PASS_HUAWEI},
                   {'user':TACACS_USER, 'pass':TACACS_PASS},
                   {'user':USER_MCA_MIN, 'pass':PASS_MCA}]
    
    flag = False
    # Establecer la conexión Telnet
    for sesion in range(2):
        reader, writer = await telnetlib3.open_connection(host, port)
        #LEER EL PROMPT
        prompt = b"#"
        modelo = None

        #VERIFICAR RAMA DEL VENDOR
        if await find(reader, b"Login:"):
            modelo = "raisecom"
        elif await find(reader, b"Username:"):
            modelo = "cisco o huawei"

        #MAXIMO DE 3 INTENTOS POR SESION
        for credential in range(limit):
            i = credentials[credential + (limit*sesion)]
            #print(i)
            #CARGAR CREDENCIALES
            username = i['user'] ; password = i['pass']
            writer.write(username + "\n")
            await reader.readuntil(b"Password:")
            writer.write(password + "\n")

            #VERIFICAR SI ENTRAMOS
            if await find(reader, b"#"):
                if not modelo == "raisecom":
                    modelo = "cisco"
                print("Ya entramos")
                pp = b"#"
                flag = True
                break
            elif await find(reader, b">"):
                if not modelo == "raisecom":
                    modelo = "huawei"
                pp = b">"
                flag = True
                break
        
        #YA INGRESAMOS
        if flag:
            print(modelo)
            break

    if modelo == "raisecom":
        await raisecom(reader, writer, pp)
    elif modelo == "huawei":
        #await huawei(reader, writer)
        print("es Huawei")
    elif modelo == "cisco":
        #await cisco(reader, writer)
        print("es Cisco")

    writer.write("exit\n")
    await writer.drain()
    writer.close()


async def find(reader, word, max_time=1):
    try:
        response = await asyncio.wait_for(reader.readuntil(word), timeout=max_time)
        return response.decode('utf-8')
    except:
        return False


async def main():
    await proceso(IP_LAB2924)


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