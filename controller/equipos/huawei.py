async def huawei(reader, writer):
    writer.write("display version\n")
    output = await reader.readuntil(b">")
    if "S5700".encode('utf-8') in output:
        #llamar proceso del modelo
        #await S5700(reader, writer)
        print("Es un AN")
        print("Es un S5700")
    elif "RAX711-C".encode('utf-8') in output:
        #await RAX711C(reader, writer)
        print("Es un CPE")
        print("Es un RAX711-C")

#CPE
async def S5700(reader, writer):
    writer.write("system-view\n") 
    out = await reader.readuntil(b"]")
    writer.write("efm enable\n")
    out += await reader.readuntil(b"]")
    writer.write("interface range GigabitEthernet 0/0/1 to GigabitEthernet 0/0/10\n")
    out += await reader.readuntil(b"]")
    writer.write("efm enable\n")
    out += await reader.readuntil(b"]")
    writer.write("return\n")
    out += await reader.readuntil(b">")
    print(out.decode('utf-8'))
        