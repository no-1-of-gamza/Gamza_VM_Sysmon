from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import base64
import json
import socket
import os, sys
import signal
import time

from shutil import copyfile
import urllib.parse as urlparse
import psutil

import WinlogbeatYML
from log import Log

def SignalHandler_SIGINT(SignalNumber, Frame):
    global log
    
    log.close()
    sys.exit(0)

def exec_command(command):
    global log
    
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        log.write("Error: "+str(e)+"\n")
        return False
    return True, result.stdout

def save_file(file_path, file_data):
    global log
    
    try:
        with open(file_path, 'wb') as f:
            f.write(file_data)
    except Exception as e:
        log.write("Error: "+str(e)+"\n")
        return False
    return True

def load_file(file_path):
    global log
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        log.write("Error: "+str(e)+"\n")
        return False
    return True, data

def beat_config(host_ip):
    global log
    
    yml = WinlogbeatYML.WinlogbeatYML(host_ip)
    is_error = yml.create_config()
    if not is_error:
        log.write("[Winlogbeat] Failed to create kibana configuration file. Try again\n")
        return False
    
    current_path = os.path.join(os.getcwd(), "winlogbeat.yml")
    try:
        copyfile(current_path,'C:\\winlogbeat\\winlogbeat.yml')
    except Exception:
        log.write("[Winlogbeat] Failed to move winlogbeat.yml. Please check your winlogbeat.yml file in winlogbeat folder\n")
        return False
    
    return True

def beat_start():
    global log
    
    try:
        args = ["C:\\winlogbeat\\winlogbeat.exe", "-c", "C:\\winlogbeat\\winlogbeat.yml"]
        process = subprocess.Popen(args)
    except Exception:
        log.write("[Winlogbeat] Failed to start winlogbeat. Please check your winlogbeat in C drive\n")
        return False
    log.write("[Winlogbeat] ready to start winlogbeat...\n")
    
    time.sleep(3)
    for proc in psutil.process_iter():
        if proc.name() == "winlogbeat.exe":
            log.write("[Winlogbeat] success to start winlogbeat...\n")
            return True
    return False

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global log
    
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, this is a GET request!\n')
        
        elif self.path.startswith('/download'):
            try:
                file_name = self.path[len('/download/'):]
                file_path = 'C:\\' + file_name
                check, file_data = load_file(file_path)
                if check:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(file_data)
                else:
                    log.write("Error: "+str(e)+"\n")
            except Exception as e:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 Not Found: File does not exist')
        
        elif self.path.startswith('/beat?i='):
            parsed_path = urlparse.urlparse(self.path)
            host_ip = parsed_path.query[2:]
            if host_ip == '':
                log.write("Invalid host ip address\n")
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404')
                return
            
            if not beat_config(host_ip):
                log.write("Failed to create config\n")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'500')
                return
            
            log.write("Success to create Winlogbeat config\n")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'200')
        
        elif self.path.startswith('/beat/start'):
            is_success = beat_start()
            if is_success:
                log.write("Success to start Winlogbeat config\n")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'200')
            else:
                log.write("Failed to create config\n")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'500')
        else:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Server Error')

    def do_POST(self):
        global log
        
        if self.path == '/command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                command = data.get('command')
                arg = data.get('arg')
                
                full_command = f'{command} {arg}'
                result, command_data = exec_command(full_command)
                if result:
                    log.write("Success to execute command\n")
                    command_data = (base64.b64encode(command_data.encode('utf-8'))).decode('ascii')
                    response_data = {'message': 'Data received successfully', 'data': command_data}
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response_json = json.dumps(response_data).encode('utf-8')
                    self.wfile.write(response_json)
                    
                else:
                    log.write("Failed to execute command\n")
                    
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'500')
                    
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Bad Request: Invalid JSON data')

        elif self.path == '/upload':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                file_name = data['file_name']
                file_data = data['file_data']
                file_bytes = base64.b64decode(file_data)
                
                if save_file(file_name, file_bytes):   
                    log.write("Success to upload file.\n")
                     
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'File uploaded successfully')
                else:
                    log.write("Failed to upload file.\n")
                    
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'File upload failed')
                    
            except Exception as e:
                log.write(f'Server Error: {str(e)}\n'.encode('utf-8'))
                
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'Server Error: {str(e)}'.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run_server(port):
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    address = (ip_address, port)
    with HTTPServer(address, MyRequestHandler) as server:
        print('Starting server...{}:{}'.format(ip_address, port))
        server.serve_forever()

if __name__ == '__main__':
    global log
    log = Log()

    signal.signal(signal.SIGINT, SignalHandler_SIGINT)
    
    port = 8080
    run_server(port)

    handler = MyRequestHandler

    if handler.command == 'GET':
        handler.do_GET()
    elif handler.command == 'POST':
        handler.do_POST()
    else:
        log.write("Not a valid request\n")
