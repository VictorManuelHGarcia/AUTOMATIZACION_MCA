import telnetlib3
import asyncio

IP_PAN = "10.4.33.193"

user = 0x726f647269676f2e6469617a
password = 0x686f6c613132333435363839313040
TACACS_USER = bytes_hex.decode('utf-8')
TACACS_PASS = format(password, 'x')

PASSWORD = ""

segmento = "" 

async def proceso(ip):
    host = ip
    port = 23  

    # Establecer la conexión Telnet
    reader, writer = await telnetlib3.open_connection(host, port)

    reader.readuntil(b"Username:")
    writer.write("")

    writer.write("exit\n")
    await writer.drain()
    writer.close()
    
async def find(reader, word, max_time=1):
    try:
        response = await asyncio.wait_for(reader.readuntil(word), timeout=max_time)
        response = True
    except:
        response = False
    #print(response)
    return response


async def main():
    await proceso(IP_PAN)


#asyncio.run(main())
print(TACACS_PASS)