import telnetlib3
import asyncio
from equipos.raisecom import raisecom
from equipos.cisco import cisco
from equipos.huawei import huawei
import time
import re
import concurrent.futures
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

IP_RAXLAB = "10.4.91.241"
IP_MANZANILLO = "10.4.216.178"
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

async def find(reader, word, max_time=1):
    try:
        response = await asyncio.wait_for(reader.readuntil(word), timeout=max_time)
        return response.decode('utf-8')
    except:
        return False
class Worker:
    def __init__(self):
        self.reader = None
        self.writer = None
        self.reader_lock = asyncio.Lock()  # Agregamos un semáforo (lock) para sincronización
        self.credentials = [{'user': USER_RAISECOM, 'pass': PASS_RAISECOM},
                            {'user': USER_MCA, 'pass': PASS_MCA},
                            {'user': TACACS_USER, 'pass': TACACS_PASS},
                            {'user': USER_MCA_MIN, 'pass': PASS_MCA},
                            {'user': USER_HUAWEI, 'pass': PASS_HUAWEI}]
        self.host = None
        self.PORT = 23
        self.LIMIT_SESSION = 3
        self.prompt = b"#"
        self.model = None
        self.id = 0
        self.table = None

    async def auth(self):
        flag = False
        for sesion in range(2):
            self.reader, self.writer = await telnetlib3.open_connection(self.host, self.PORT)
            self.prompt = b"#"
            self.model = None

            if await find(self.reader, b"Login:"):
                self.model = "raisecom"
            elif await find(self.reader, b"Username:"):
                self.model = "cisco o huawei"

            for credential in range(self.LIMIT_SESSION):
                i = self.credentials[credential + (self.LIMIT_SESSION * sesion)]
                username = i['user']
                password = i['pass']
                self.writer.write(username + "\n")
                await self.reader.readuntil(b"Password:")
                self.writer.write(password + "\n")

                if await find(self.reader, b"#"):
                    if not self.model == "raisecom":
                        self.model = "cisco"
                    print("Comienza: " + str(self.host))
                    self.prompt = b"#"
                    flag = True
                    break
                elif await find(self.reader, b">"):
                    if not self.model == "raisecom":
                        self.model = "huawei"
                    self.prompt = b">"
                    flag = True
                    break
            
            if flag:
                self.writer.write("\n")
                text = await find(self.reader, b"#")
                self.writer.write("\n")
                text = re.sub(r'[\r\n\s+]', '', text)
                self.edit_table(self.id, 2, text)
                break

    async def process(self, ip):
        start_time = time.time()
        self.host = ip
        
        async with self.reader_lock:  # Aseguramos que solo una corrutina acceda al reader a la vez
            await self.auth()

            if self.model == "raisecom":
                await raisecom(self.reader, self.writer, self.prompt)
            elif self.model == "huawei":
                pass
            elif self.model == "cisco":
                pass

        print("Termina: " + str(self.host))
        self.writer.write("exit\n")
        await self.writer.drain()
        self.writer.close()
        end_time = time.time()
        print(end_time - start_time)
        self.id += 1

    def edit_table(self, row, column, value):
        if self.table is not None:
            self.table.SetCellValue(row, column, str(value))
            self.gui.Update()
        
    def connect_gui(self, gui):
        self.gui = gui
        self.table = self.gui.success_grid

async def main():
    worker = Worker()
    ips_to_validate = [IP_RAXLAB, IP_LAB2924]

    tasks = [worker.process(ip) for ip in ips_to_validate]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
