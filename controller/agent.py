from http.server import BaseHTTPRequestHandler, HTTPServer
import subprocess
import base64
import json
import socket

# POST 요청: 명령어 수행
def exec_command(command) -> (bool, str):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"{command}\n>> {result.stdout}")
    except Exception as e:
        print(f'Error: {str(e)}')
        return False
    return True, result.stdout

# 가상머신에 파일 저장: 외부 -> 가상머신
def save_file(file_path, file_data) -> bool:
    try:
        with open(file_path, 'wb') as f:
            f.write(file_data)
    except Exception as e:
        print(f'Error: {str(e)}')
        return False
    return True

# 클라이언트에 파일 다운로드: 가상머신 -> 외부
def load_file(file_path) -> (bool, bytes):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f'Error: {str(e)}')
        return False
    return True, data

class MyRequestHandler(BaseHTTPRequestHandler):
    # GET 요청
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Hello, this is a GET request!\n')
        
        # load_file 호출
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

    # POST 요청
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

        # save_file 호출
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

# 서버 실행
def run_server(port):
    # 서버의 ip를 가져옴
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)

    address = (ip_address, port)
    with HTTPServer(address, MyRequestHandler) as server:
        print('Starting server...')
        server.serve_forever()

if __name__ == '__main__':
    port = 8080
    run_server(port)

    # 클라이언트 요청에 따른 수행 루트
    handler = MyRequestHandler

    if handler.command == 'GET':
        handler.do_GET()
    elif handler.command == 'POST':
        handler.do_POST()
    else:
        print('Not a valid request')
