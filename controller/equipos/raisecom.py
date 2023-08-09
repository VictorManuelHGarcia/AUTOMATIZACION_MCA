import re
import asyncio

async def find(reader, word, max_time=1):
    try:
        response = await asyncio.wait_for(reader.readuntil(word), timeout=max_time)
    except:
        response = False
    return response
        
async def raisecom(reader, writer,prompt):
    if prompt == b">":
        writer.write("enable\n") 
        await reader.readuntil(b":")
        writer.write("raisecom\n") 
        await reader.readuntil(b"#")

    writer.write("show version\n")
    output = await reader.readuntil(b"#")
    if "ISCOM2608".encode('utf-8') in output:
        #llamar proceso del modelo
        #await ISCOM2608(reader, writer)
        print("Es un CPE")
        print("Es un ISCOM2608G")
    elif "RAX711-C".encode('utf-8') in output:
        #await RAX711C(reader, writer)
        print("Es un CPE")
        print("Es un RAX711-C")
    elif "RAX711-R".encode('utf-8') in output:
        print("Es un CPE")
        print("Es un RAX711-R")
        #await RAX711R(reader,writer)
    elif "RAX721".encode('utf-8') in output:
        print("Es un AN")
        print("Es un RAX721")
        await puertos2(reader, writer)
    elif "ISCOM2924".encode('utf-8') in output:
        print("Es un AN")
        print("Es un ISCOM2924")
        #print(await puertos(reader,writer,28))
        await ISCOM29XX(reader, writer,28)
    elif "ISCOM2948".encode('utf-8') in output:
        print("Es un AN")
        print("Es un ISCOM2948")
        await puertos(reader,writer,52)
    else:
        print("Modelo desconocido")
    
#CPE
async def ISCOM2608(reader, writer):
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    writer.write("interface range gigaethernet 1/1/1-10\n")
    out += await reader.readuntil(b"#")
    writer.write("oam enable\n")
    out += await reader.readuntil(b"#")
    writer.write("oam passive\n")
    out += await reader.readuntil(b"#")
    writer.write("oam notify dying-gasp enable\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))
#AN
async def ISCOM29XX(reader, writer, ports):
    #p = await puertos(reader,writer, ports)
    p = ["port 3"]
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
    print(out.decode('utf-8'))

async def ISCOM29XX_INVERSO(reader, writer, ports):
    p = await puertos(reader,writer,ports)
    #p = ["port 4"]
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    for puerto in p:
        writer.write("interface " + puerto + "\n")
        out += await reader.readuntil(b"#")
        writer.write("oam peer event trap disable\n")
        out += await reader.readuntil(b"#")
        writer.write("oam event trap disable\n")
        out += await reader.readuntil(b"#")
        writer.write("oam passive\n")
        out += await reader.readuntil(b"#")
        writer.write("oam disable\n")
        out += await reader.readuntil(b"#")
        writer.write("exit\n")
        out += await reader.readuntil(b"#")
    writer.write("end\n")
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
    p = await puertos2(reader, writer)
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    for puerto in p:
        writer.write("interface " + puerto + "\n")
        out += await reader.readuntil(b"#")
        writer.write("oam enable\n")
        out += await reader.readuntil(b"#")
        writer.write("oam passive\n")
        out += await reader.readuntil(b"#")
        writer.write("oam notify dying-gasp enable\n")
        out += await reader.readuntil(b"#")
        writer.write("exit\n")
    writer.write("end\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))

async def puertos(reader, writer, value):
    writer.write("sh int port-list 1-" + str(value) + " des\n")
    #await reader.readline()
    out = await reader.readuntil(b"#")
    #print(out.decode('utf-8'))
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

async def puertos2(reader, writer):
    writer.write("show interface brief\n")
    out = await paginar(reader, writer)
    """output = await reader.readuntil(b" --More-- ")
    if output :
        out = output
        
    writer.write(chr(32))"""
    out += await reader.readuntil(b"#")
    #print(out.decode())
    #Contador de Puertos Disponibles:
    Contador = out.decode('utf-8').split()
    ports = []
    for i in range(0, len(Contador)):
        if re.match(r'TGE1/[1-9]/[1-9]+', Contador[i]):
            if not "TMCA" in Contador[i+8]:
                aux = Contador[i].split('TGE')
                ports.append("tengigabitethernet " + aux[1])
            else:
                print("tengigabitethernet " + Contador[i].split('TGE')[1] + " es troncal")
            i += 9
        elif re.match(r'GE1/2/[1-9]+', Contador[i]):
            if not "TMCA" in Contador[i+8]:
                aux = Contador[i].split('GE')
                ports.append("gigabitethernet " + aux[1])
            else:
                print("gigabitethernet " + Contador[i].split('GE')[1] + " es troncal")
            i += 9
    return ports

async def paginar(reader, writer):
    output = "".encode()
    while True:
        try:
            aux = await find(reader, b" --More-- ")
            if aux :
                output += aux
                writer.write(chr(32))
            else:
                break
        except:
            break
    return output