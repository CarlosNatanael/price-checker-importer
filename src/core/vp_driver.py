# src/core/vp_driver.py
import ctypes
import os
import time
from typing import Tuple

class VPDriver:
    def __init__(self, dll_path: str = "VP_v3.dll"):
        self.dll = None
        self.is_running = False
        try:
            full_path = os.path.abspath(dll_path)
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"DLL não encontrada em: {full_path}")
            self.dll = ctypes.windll.LoadLibrary(full_path)
            self._setup_signatures()
            print(f"DLL carregada com sucesso: {full_path}")
        except Exception as e:
            print(f"Erro ao carregar DLL: {e}")
            self.dll = None

    def _setup_signatures(self):
        if not self.dll: return

        self.dll.tc_startserver.argtypes = [ctypes.c_int]
        self.dll.tc_startserver.restype = ctypes.c_int

        self.dll.bReceiveBarcode.argtypes = [ctypes.c_char_p]
        self.dll.bReceiveBarcode.restype = ctypes.c_int

        self.dll.bSendProdPrice.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
        self.dll.bSendProdPrice.restype = ctypes.c_int

        self.dll.GetTabConectados.restype = ctypes.c_int

    def start_server(self, port: int = 6500) -> bool:
        if not self.dll: return False
        try:
            if hasattr(self.dll, 'vInitialize'):
                self.dll.vInitialize()

            result = self.dll.tc_startserver(port)
            self.is_running = (result == 1) or (result == 0)
            return True
        except Exception as e:
            print(f"Erro ao iniciar servidor: {e}")
            return False

    def check_requests(self) -> Tuple[str, str]:
        if not self.dll: return None, None
        barcode_buffer = ctypes.create_string_buffer(128)
        result = self.dll.bReceiveBarcode(barcode_buffer)
        
        if result > 0:
            raw_data = barcode_buffer.value.decode('ascii', errors='ignore')
            return "UNKNOWN_IP", raw_data
        
        return None, None

    def send_price(self, ip_terminal: str, line1: str, line2: str):
        if not self.dll: return
        b_ip = ip_terminal.encode('ascii')
        b_l1 = line1[:20].ljust(20).encode('ascii')
        b_l2 = line2[:20].ljust(20).encode('ascii')
        self.dll.bSendProdPrice(b_ip, b_l1, b_l2)