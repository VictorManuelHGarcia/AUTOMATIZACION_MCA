import wx
import wx.lib.scrolledpanel as scrolled
import wx.grid as gridlib
import openpyxl
import os
import threading
from ping3 import ping
import re
from main import Worker
import asyncio
from ip_manager import validar_segmento_red, get_available_ips

# Define la paleta de colores
COLOR1 = wx.Colour(20, 79, 116)
COLOR2 = wx.Colour(124, 182, 97)
COLOR3 = wx.Colour(237, 160, 38)
COLOR4 = wx.Colour(72, 124, 161)
COLOR5 = wx.Colour(227, 226, 220)

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(800, 600))
        
        # Panel principal
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(COLOR1)
        
        # Cuadro para los buscadores de archivos
        file_pick_box = wx.StaticBox(self.panel, label="Cargar IP's: ")
        file_pick_box.SetForegroundColour(wx.WHITE)
        file_pick_sizer = wx.StaticBoxSizer(file_pick_box, wx.VERTICAL)
        
        # Titulo de la interfaz
        self.title_label = wx.StaticText(self.panel, label="Automatización", style=wx.ALIGN_CENTER)
        self.title_label.SetForegroundColour(wx.WHITE)
        self.title_label.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        # Buscadores de archivos
        self.excel_file_path = ""
        
        self.calculate_sizer = wx.BoxSizer( wx.HORIZONTAL )

        ##
        #CAMPO PARA CALCULAR IP
        self.lbl_calculate_ips = wx.StaticText( self.panel, wx.ID_ANY, u"Ingresa un segmento de red:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.lbl_calculate_ips.Wrap( -1 )
        self.lbl_calculate_ips.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )

        self.calculate_sizer.Add( self.lbl_calculate_ips, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.ctrl_calculate_ip = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.calculate_sizer.Add( self.ctrl_calculate_ip, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        self.btn_calculate_ips = wx.Button( self.panel, wx.ID_ANY, u"Calcular", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.calculate_sizer.Add( self.btn_calculate_ips, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

        file_pick_sizer.Add(self.calculate_sizer, 0, wx.EXPAND | wx.ALL, 5)
        ##

        self.excel_file_picker_btn = wx.Button(self.panel, label="Selecciona el archivo con las direcciones IP:")
        self.excel_file_picker_btn.SetBackgroundColour(COLOR5)
        self.excel_file_picker_btn.Bind(wx.EVT_BUTTON, self.on_excel_file_picker)
        
        # Agregar etiquetas y botones al sizer del cuadro
        file_pick_sizer.Add(self.excel_file_picker_btn, 0, wx.EXPAND | wx.ALL, 5)
        
        # Sizer horizontal para los botones "Cargar IPs" y "Ejecutar comandos"
        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Botón para cargar direcciones IP
        self.load_ips_btn = wx.Button(self.panel, label="Cargar IPs")
        self.load_ips_btn.SetBackgroundColour(COLOR5)
        self.load_ips_btn.Bind(wx.EVT_BUTTON, self.on_load_ips)
        
        # Botón para ejecutar el script
        self.execute_commands_btn = wx.Button(self.panel, label="Ejecutar comandos")
        self.execute_commands_btn.SetBackgroundColour(COLOR5)
        self.execute_commands_btn.Bind(wx.EVT_BUTTON, self.on_execute_commands)

        # Botón para validar conectividad
        self.validate_connectivity_btn = wx.Button(self.panel, label="Validar Conectividad")
        self.validate_connectivity_btn.SetBackgroundColour(COLOR5)
        self.validate_connectivity_btn.Bind(wx.EVT_BUTTON, self.on_validate_connectivity)
        
        buttons_sizer.Add(self.load_ips_btn, 0, wx.EXPAND | wx.ALL, 5)
        buttons_sizer.Add(self.validate_connectivity_btn, 0, wx.EXPAND | wx.ALL, 5)  # Agregamos el botón de Validar Conectividad
        buttons_sizer.Add(self.execute_commands_btn, 0, wx.EXPAND | wx.ALL, 5)
        
        # Cuadro para las tablas de resultado
        result_box = wx.StaticBox(self.panel, label="Dispositivos: ")
        result_box.SetForegroundColour(wx.WHITE)
        result_sizer = wx.StaticBoxSizer(result_box, wx.VERTICAL)
        
        # Tabla de direcciones IP ingresadas con éxito
        self.success_grid = gridlib.Grid(self.panel)
        self.success_grid.CreateGrid(0, 5)
        self.success_grid.SetColLabelValue(0, "Ping")
        self.success_grid.SetColLabelValue(1, "Dirección IP")
        self.success_grid.SetColLabelValue(2, "Hostname")
        self.success_grid.SetColLabelValue(3, "Modelo")
        self.success_grid.SetColLabelValue(4, "Estatus:")
        self.success_grid.SetColSize(0, 80)
        self.success_grid.SetColSize(1, 150)
        self.success_grid.SetColSize(2, 200)
        self.success_grid.SetColSize(3, 150)
        self.success_grid.SetColSize(4, 80)
    

        # Agregar tablas al sizer del cuadro
        result_sizer.Add(self.success_grid, 1, wx.EXPAND | wx.ALL, 5)

        log_box = wx.StaticBox(self.panel, label="Log: ")
        log_box.SetForegroundColour(wx.WHITE)
        log_sizer = wx.StaticBoxSizer(log_box, wx.VERTICAL)

        # Log de la ejecución de comandos
        self.log_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.log_text.SetBackgroundColour(wx.BLACK)
        self.log_text.SetForegroundColour(wx.WHITE)
        log_sizer.Add(self.log_text, 1, wx.EXPAND | wx.ALL, 5)
        
        # Acomodar elementos en el sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.title_label, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.Add(file_pick_sizer, 0, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(buttons_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        main_sizer.Add(result_sizer, 1, wx.EXPAND | wx.ALL, 10)
        main_sizer.Add(log_sizer, 1, wx.EXPAND | wx.ALL, 10)
        
        self.panel.SetSizer(main_sizer)
        self.Layout()

        self.execute_commands_btn.Hide()
        self.validate_connectivity_btn.Hide()
        self.load_ips_btn.Hide()
        
        # Connect Events
        self.success_grid.Bind( wx.grid.EVT_GRID_SELECT_CELL, self.show_log)
        self.btn_calculate_ips.Bind( wx.EVT_BUTTON, self.calculate_ips )

        self.ips = {}
        self.memory = {}
        self.completed = 0
    
    def id_ip(self, group):
        self.ips = {}
        for id, ip in enumerate(group):
            self.ips[ip] = id
        

    def calculate_ips(self, event):
        segmento = str(self.ctrl_calculate_ip.GetValue())
        if validar_segmento_red(segmento):
            ips = get_available_ips(segmento)
            self.update_success_table(ips)
            self.validate_connectivity_btn.Show()
        else:
            wx.MessageBox('Este es un aviso de advertencia.', 'Advertencia', wx.ICON_ERROR | wx.OK)
        event.Skip()

    def on_validate_connectivity(self, event):
        num_rows = self.success_grid.GetNumberRows()
        ips_to_validate = [self.success_grid.GetCellValue(row, 1) for row in range(num_rows)]
        self.id_ip(ips_to_validate)
        self.execute_commands_btn.Show()

        # Realizar pings en hilos separados
        threads = []
        for ip in ips_to_validate:
            thread = threading.Thread(target=self.ping_ip_and_update_grid, args=(ip,))
            thread.start()
            threads.append(thread)

        # Esperar a que todos los hilos finalicen
        for thread in threads:
            thread.join()
        print(self.ips)
        for ip, id in self.ips.items():
            print(str(id) + " " + str(ip))

    def ping_ip_and_update_grid(self, ip):
        status = self.ping_ip(ip)
        #print(str(status))
        wx.CallAfter(self.update_grid_with_ping_result, ip, status)

    async def work(self, ip, id):
        worker = Worker()
        worker.connect_gui(self)
        await worker.process(ip, id)

    async def command_execute(self, ips):
        tasks = [self.work(ip, id) for ip, id in ips.items()]
        await asyncio.gather(*tasks)

    def update_grid_with_ping_result(self, ip, status):
        num_rows = self.success_grid.GetNumberRows()
        for row in range(num_rows):
            if self.success_grid.GetCellValue(row, 1) == ip:
                if status:
                    self.success_grid.SetCellValue(row, 0, "✔")  # Mostramos una palomita en la celda de estatus
                    self.success_grid.SetCellTextColour(row, 0, wx.Colour(0, 128, 0))  # Color verde para el texto "✔"
                else:
                    self.success_grid.SetCellValue(row, 0, "✘")  # Mostramos una X en la celda de estatus
                    self.success_grid.SetCellTextColour(row, 0, wx.Colour(255, 0, 0))  # Color rojo para el texto "✘"

    def ping_ip(self, ip):
        try:
            # Realizamos un ping a la IP con un tiempo de espera de 1 segundo
            response_time = ping(ip, timeout=1)
            patron_ip = r'^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})$'
            if re.match(patron_ip, ip):
                if not response_time is not None:
                    self.ips.pop(ip)
                    #self.edit_table(3, 4, "✘ (N/A)", wx.Colour(255, 0, 0))
                    return False
                return response_time is not None
            else:
                self.ips.pop(ip)
                print("Esta IP no es valida")
                return False
        except Exception:
            return False

    def on_txt_file_picker(self, event):
        dlg = wx.FileDialog(self, message="Elegir archivo de comandos", wildcard="Text files (*.txt)|*.txt", style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.txt_file_path = dlg.GetPath()
            self.txt_file_picker_btn.SetLabel(os.path.basename(self.txt_file_path))
        dlg.Destroy()
        
    def on_excel_file_picker(self, event):
        dlg = wx.FileDialog(self, message="Elegir archivo Excel", wildcard="Excel files (*.xlsx)|*.xlsx", style=wx.FD_OPEN)
        self.load_ips_btn.Show()
        if dlg.ShowModal() == wx.ID_OK:
            self.excel_file_path = dlg.GetPath()
            self.excel_file_picker_btn.SetLabel(os.path.basename(self.excel_file_path))
        dlg.Destroy()

    def on_load_ips(self, event):
        # Leer archivo de direcciones IP desde el archivo Excel seleccionado

        self.validate_connectivity_btn.Show()


        ip_list = []
        if self.excel_file_path:
            workbook = openpyxl.load_workbook(self.excel_file_path)
            sheet = workbook.active
            for row in sheet.iter_rows(values_only=True):
                ip_list.append(row[0])  # Asumiendo que la dirección IP está en la primera columna

        # Actualizar la tabla de direcciones IP
        self.update_success_table(ip_list)

    def on_execute_commands(self, event):
        self.memory = {}
        self.completed = 0
        asyncio.run(self.command_execute(self.ips))
        self.ips = {}
        """loop = asyncio.get_event_loop()
        loop.create_task(self.command_execute(ips_to_validate))"""

    def show_log( self, event ):
        id = int(event.Row)
        #AQUI VAMOS A C0ONSULTAR LA MEMORIA
        log = self.memory.get(id)
        if log:
            self.log_text.SetValue(str(log))
        else:
            self.log_text.SetValue("")
        event.Skip()

    def end_process(self):
        self.completed += 1
        if self.completed == len(self.ips):
            wx.MessageBox('Todos los workers han finalizado la ejecución.', 'Procesamiento finalizado', wx.ICON_INFORMATION | wx.OK)

    def update_success_table(self, data):
        num_rows = self.success_grid.GetNumberRows()
        if num_rows > 0:
            self.success_grid.DeleteRows(0, num_rows)
        self.success_grid.AppendRows(len(data))
        for row, ip in enumerate(data):
            self.success_grid.SetCellValue(row, 0, "")  # Dejar en blanco la celda de palomita
            self.success_grid.SetCellValue(row, 1, str(ip))
            self.success_grid.SetCellValue(row, 2, "")  # Dejar en blanco la celda de hostname
            
    def edit_table(self, row, column, value, color = None):
        self.success_grid.SetCellValue(row, column, str(value)) 
        if color != None:
            self.success_grid.SetCellTextColour(row, column, color)
            self.Update()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None, "Automatización")
    frame.Show()
    app.MainLoop()
