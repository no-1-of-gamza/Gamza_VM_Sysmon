from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import base64
import json
import socket
import os, sys
from shutil import copyfile

import WinlogbeatYML

class Winlogbeat:
    def __init__(self, host_ip):
        self.process = None
        self.host_ip = host_ip
    
    def status(self):
        if self.process == None:
            print("Winlogbeat didn't start yet")
            return False
        
        if self.process.poll() == None:
            return True
        else:
            return False
    
    def start(self):
        yml = WinlogbeatYML.WinlogbeatYML(self.host_ip)
        is_error = yml.create_config()
        if not is_error:
            print("Failed to create kibana configuration file. Try again\n")
            return False
        
        current_path = os.path.join(os.getcwd(), "winlogbeat.yml")
        try:
            copyfile(current_path,'C:\\winlogbeat\\winlogbeat.yml')
        except Exception:
            print("Failed to move winlogbeat.yml. Please check your winlogbeat.yml file in winlogbeat folder\n")
            return False

        try:
            args = ["C:\\winlogbeat\\winlogbeat.exe", "-c", "C:\\winlogbeat\\winlogbeat.yml", "-e"]
            self.process = subprocess.Popen(args, stdout=subprocess.PIPE)
        except Exception:
            print("Failed to start winlogbeat. Please check your winlogbeat in C drive\n")
            return False
        
        print("ready to start winlogbeat...")
        
        while True:
            msg = self.process.stdout.readline()
            if not msg:
                break
            
            if "Connecting to backoff" in msg.decode('utf-8')["message"]:
                return True
        
        return False
    
    def stop(self):
        if self.process == None:
            print("Winlogbeat didn't start yet")
            return False
        
        result = self.process.terminate()
        self.process = None
        
        return result

def exec_command(command) -> (bool, str):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"{command}\n>> {result.stdout}")
    except Exception as e:
        print(f'Error: {str(e)}')
        return False
    return True, result.stdout

def save_file(file_path, file_data) -> bool:
    try:
        with open(file_path, 'wb') as f:
            f.write(file_data)
    except Exception as e:
        print(f'Error: {str(e)}')
        return False
    return True

def load_file(file_path) -> (bool, bytes):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f'Error: {str(e)}')
        return False
    return True, data

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, this is a GET request!\n')
        
        elif self.path.startswith('/download'):
            try:
                file_name = self.path[len('/download/'):]
                print(file_name)
                file_path = 'C:\\' + file_name
                check, file_data = load_file(file_path)
                if check:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(file_data)
                else:
                    print(f'Error: {str(e)}')
            except Exception as e:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'404 Not Found: File does not exist')
        else:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Server Error')

    def do_POST(self):
        if self.path == '/command':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                command = data.get('command')
                arg = data.get('arg')
                full_command = f'{command} {arg}'
                result, command_data = exec_command(full_command)
                command_data = (base64.b64encode(command_data.encode('utf-8'))).decode('ascii')
                print(command_data)
                response_data = {'message': 'Data received successfully', 'data': command_data}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response_json = json.dumps(response_data).encode('utf-8')
                self.wfile.write(response_json)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Bad Request: Invalid JSON data')

        elif self.path == '/upload':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(data.decode('utf-8'))
                file_name = data['file_name']
                file_data = data['file_data']
                file_bytes = base64.b64decode(file_data)
                if save_file(file_name, file_bytes):    
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'File uploaded successfully')
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'File upload failed')
            except Exception as e:
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
        print('Starting server...')
        server.serve_forever()

if __name__ == '__main__':
    port = 8080
    run_server(port)

    handler = MyRequestHandler

    if handler.command == 'GET':
        handler.do_GET()
    elif handler.command == 'POST':
        handler.do_POST()
    else:
        print('Not a valid request')
