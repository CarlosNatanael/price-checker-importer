# src/core/uploader.py
import ftplib
import socket
import io
from typing import List

class VPUploader:
    def __init__(self, ip_list: List[str], user: str = 'tanca', password: str = 'tanca'):
        self.ip_list = ip_list
        self.user = user
        self.password = password
        self.port = 21 # Porta padrão FTP (Verificar no manual se é 21 ou 2121)

    def send_file_ftp(self, file_path: str, remote_name: str = "itens.txt"):
        """
        Envia o arquivo gerado para uma lista de verificadores via FTP.
        Muitos VPs (Tanca/Jetway) rodam um servidor FTP interno para receber a carga.
        """
        results = {}
        
        with open(file_path, 'rb') as f:
            file_content = f.read()

        for ip in self.ip_list:
            try:
                print(f"Conectando ao VP {ip}...")
                ftp = ftplib.FTP()
                ftp.connect(ip, self.port, timeout=5)
                ftp.login(self.user, self.password)
                
                # Envia o arquivo binário
                # 'STOR' é o comando FTP para upload
                f_obj = io.BytesIO(file_content) 
                ftp.storbinary(f'STOR {remote_name}', f_obj)
                
                ftp.quit()
                results[ip] = "Sucesso"
                print(f"✅ Upload concluído para {ip}")
                
            except Exception as e:
                results[ip] = f"Erro: {str(e)}"
                print(f"❌ Falha em {ip}: {e}")
                
        return results

    def send_socket_command(self, ip: str, command: str):
        """
        Caso o manual exija um comando de 'Refresh' após o envio do arquivo.
        Ex: Enviar um byte específico para o aparelho reiniciar e ler o arquivo novo.
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(3)
                s.connect((ip, 6550)) # Porta de comando comum em Tanca (Verificar Manual)
                s.sendall(command.encode('ascii'))
        except Exception as e:
            print(f"Erro ao enviar comando para {ip}: {e}")