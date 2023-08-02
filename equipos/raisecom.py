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
        

async def raisecom(reader, writer):
    if await find(reader,b">"):
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
        await RAX711R(reader,writer)
    elif "ISCOM2924".encode('utf-8') in output:
        print("Es un ISCOM2924")
        #await ISCOM2924(reader, writer)
    elif "ISCOM2948".encode('utf-8') in output:
        print("Es un ISCOM2948")
    else:
        print("Modelo desconocido")
    

async def ISCOM2608(reader, writer):
    writer.write("config terminal\n") 
    writer.write("interface range gigaethernet 1/1/1-10\n")
    writer.write("oam enable\n")
    writer.write("oam passive\n")
    writer.write("oam notify dying-gasp enable\n")

async def ISCOM2924(reader, writer):
    writer.write("config terminal\n") 
    await reader.readuntil(b"#")
    writer.write("interface port 4\n")
    await reader.readuntil(b"#")
    writer.write("description Prueba-02/08/2023-PYTHON-PRUEBA\n")
    await reader.readuntil(b"#")
    writer.write("end\n")
    await reader.readuntil(b"#")
    writer.write("show run interface port-list 4\n")
    out = await reader.readuntil(b"#")
    print(out.decode('utf-8'))



async def RAX711C(reader, writer):
    writer.write("config terminal\n") 
    writer.write("interface range line 1-4\n")
    writer.write("oam enable\n")
    writer.write("oam passive\n")
    writer.write("oam notify dying-gasp enable\n")

async def RAX711R(reader, writer):
    """writer.write("config terminal\n") 
    writer.write("interface gigaethernet 1/1/1\n")
    writer.write("oam enable\n")
    writer.write("oam passive\n")
    writer.write("oam notify dying-gasp enable\n")"""
    print("Si funciona")

async def RAX721(reader, writer):
    writer.write("config terminal\n") 
    writer.write("interface range line 1-4\n")
    writer.write("oam enable\n")
    writer.write("oam passive\n")
    writer.write("oam notify dying-gasp enable\n")