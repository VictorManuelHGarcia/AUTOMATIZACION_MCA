import asyncio

async def find(reader, word, max_time=1):
    try:
        response = await asyncio.wait_for(reader.readuntil(word), timeout=max_time)
    except:
        response = False
    #print(response)
    return response


async def paginar(reader, writer):
    output = ""
    while True:
        res = await find(reader, "--More--")
        if res:
            output += res
            writer.write(chr(32))
        else:
            res = await find(reader, b"#")
            if res:
                output += res    
            break
    return output
    

async def cisco(reader, writer):
    writer.write("show version\n")
    output = await paginar()
    #await isAN(output)
    if "ME-3400-24FS".encode('utf-8') in output:
        #llamar proceso del modelo
        print("Es un ME-3400-24FS")
        #await ME340024FS(reader, writer)
    elif "ME-3400G-12CS".encode('utf-8') in output:
        print("Es un ME-3400G-12CS")
        #await ME3400G12CS(reader, writer)
    elif "ASR920".encode('utf-8') in output:
        print("Es un ASR920")
        #await ASR920(reader, writer)


#AN
async def ME340024FS(reader, writer):
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    writer.write("interface range fastEthernet 0/1-24 , gigabitEthernet 0/1-2\n")
    out += await reader.readuntil(b"#")
    writer.write("ethernet oam\n")
    out += await reader.readuntil(b"#")
    writer.write("ethernet oam mode passive\n")
    out += await reader.readuntil(b"#")
    writer.write("end\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))

#AN
async def ME3400G12CS(reader, writer):
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    writer.write("interface range GigabitEthernet 0/1-16\n")
    out += await reader.readuntil(b"#")
    writer.write("ethernet oam\n")
    out += await reader.readuntil(b"#")
    writer.write("ethernet oam mode passive\n")
    out += await reader.readuntil(b"#")
    writer.write("end\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))

async def ASR920(reader, writer):
    writer.write("config terminal\n") 
    out = await reader.readuntil(b"#")
    writer.write("interface range gigabitEthernet 0/0/0-23\n")
    out += await reader.readuntil(b"#")
    writer.write("ethernet oam\n")
    out += await reader.readuntil(b"#")
    writer.write("ethernet oam mode passive\n")
    out += await reader.readuntil(b"#")
    writer.write("service instance 1 ethernet\n")
    out += await reader.readuntil(b"#")
    writer.write("encapsulation untagged\n")
    out += await reader.readuntil(b"#")
    writer.write("bridge-domain 1\n")
    out += await reader.readuntil(b"#")
    writer.write("end\n")
    out += await reader.readuntil(b"#")
    print(out.decode('utf-8'))