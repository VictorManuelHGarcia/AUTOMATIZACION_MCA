import re
import asyncio

async def find(reader, word, max_time=1):
    try:
        response = await asyncio.wait_for(reader.readuntil(word), timeout=max_time)
        response = True
    except:
        response = False
    #print(response)
    return response

async def isAN(prompt):
    if "AN".encode('utf-8') in prompt:
        print("Es un AN")
    else:
        print("Es un CPE")
        

async def raisecom(reader, writer,prompt):
    if prompt == b">":
        writer.write("enable\n") 
        await reader.readuntil(b":")
        writer.write("raisecom\n") 
        await reader.readuntil(b"#")

    writer.write("show version\n")
    output = await reader.readuntil(b"#")
    await isAN(output)
    if "ISCOM2608".encode('utf-8') in output:
        #llamar proceso del modelo
        #await ISCOM2608(reader, writer)
        print("Es un ISCOM2608G")
    elif "RAX711-C".encode('utf-8') in output:
        #await RAX711C(reader, writer)
        print("Es un RAX711-C")
    elif "RAX711-R".encode('utf-8') in output:
        print("Es un RAX711-R")
        #await RAX711R(reader,writer)
    elif "ISCOM2924".encode('utf-8') in output:
        print("Es un ISCOM2924")
        print(await puertos(reader,writer,28))
        #await ISCOM2924(reader, writer)
    elif "ISCOM2948".encode('utf-8') in output:
        print("Es un ISCOM2948")
        print(await puertos(reader,writer,52))
    else:
        print("Modelo desconocido")
    
#CPE
async def ISCOM2608(reader, writer):
    writer.write("config terminal\n") 
    await reader.readuntil(b"#")
    writer.write("interface range gigaethernet 1/1/1-10\n")
    await reader.readuntil(b"#")
    writer.write("oam enable\n")
    await reader.readuntil(b"#")
    writer.write("oam passive\n")
    await reader.readuntil(b"#")
    writer.write("oam notify dying-gasp enable\n")
    out = await reader.readuntil(b"#")
    print(out.decode('utf-8'))
#AN
async def ISCOM2924(reader, writer):
    #p = puertos(reader,writer,28)
    p = ["port 4", "port 18"]
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    for puerto in p:
        writer.write("interface " + puerto + "\n")
        out += await reader.readuntil(b"#")
        writer.write("oam enable\n")
        out += await reader.readuntil(b"#")
        writer.write("oam active\n")
        out += await reader.readuntil(b"#")
        writer.write("oam peer event trap enable\n")
        out += await reader.readuntil(b"#")
        writer.write("oam event trap enable\n")
        out += await reader.readuntil(b"#")
        writer.write("exit\n")
        out += await reader.readuntil(b"#")
    writer.write("end\n")
    out += await reader.readuntil(b"#")
    writer.write("show run interface port-list 4\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))

#AN
async def ISCOM2948(reader, writer):
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    writer.write("interface port 4\n")
    out += await reader.readuntil(b"#")
    writer.write("oam enable\n")
    out += await reader.readuntil(b"#")
    writer.write("oam active\n")
    out += await reader.readuntil(b"#")
    writer.write("oam peer event trap enable\n")
    out += await reader.readuntil(b"#")
    writer.write("oam event trap enable\n")
    out += await reader.readuntil(b"#")
    writer.write("end\n")
    out += await reader.readuntil(b"#")
    writer.write("show run interface port-list 4\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))

#CPE
async def RAX711C(reader, writer):
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    writer.write("interface range line 1-4\n")
    out += await reader.readuntil(b"#")
    writer.write("oam enable\n")
    out += await reader.readuntil(b"#")
    writer.write("oam passive\n")
    out += await reader.readuntil(b"#")
    writer.write("oam notify dying-gasp enable\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))

#CPE
async def RAX711R(reader, writer):
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    writer.write("interface gigaethernet 1/1/1\n")
    out += await reader.readuntil(b"#")
    writer.write("oam enable\n")
    out += await reader.readuntil(b"#")
    writer.write("oam passive\n")
    out += await reader.readuntil(b"#")
    writer.write("oam notify dying-gasp enable\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))
    
#AN
async def RAX721(reader, writer):
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    writer.write("interface range line 1-4\n")
    out += await reader.readuntil(b"#")
    writer.write("oam enable\n")
    out += await reader.readuntil(b"#")
    writer.write("oam passive\n")
    out += await reader.readuntil(b"#")
    writer.write("oam notify dying-gasp enable\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))

async def puertos(reader, writer, value):
    writer.write("sh int port-list 1-" + str(value) + " des\n")
    await reader.readline()
    out = await reader.readuntil(b"#")
    print(out.decode('utf-8'))
    #Contador de Puertos Disponibles:
    Contador = out.decode('utf-8').split()
    ports = []
    for i in range(0, len(Contador)):
        if re.match(r'P[0-9]+', Contador[i]):
            if not "TMCA" in Contador[i+1]:
                aux = Contador[i].split('P')
                ports.append("port " + aux[1])
            else:
                print("port: " + Contador[i].split('P')[1] + " es troncal")
            i += 1
    return ports

