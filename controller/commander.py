import requests
import json
import base64
import os
import subprocess

class request_vm:
    def __init__(self, port, vm_name):
        self.port = port
        self.vm_name = vm_name
        self.vm_IP = '127.0.0.1'

        vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
        vboxmanage_cmd = [vboxmanage_path]
        network_adapter = "/VirtualBox/GuestInfo/Net/0/V4/IP"
    
        command = f"guestproperty get {vm_name} {network_adapter}"
        vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

        result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
        index = result.stdout.find("Value:")
        if index != -1:
            str = result.stdout[index + len("Value:"):]
            self.vm_IP = str.strip()
            print(f"'{self.vm_name}' IP: {self.vm_IP}\n")
        else:
            print(f"'{self.vm_name}' IP not found\n")

    def server_check(self):
        response = requests.get(f'http://{self.vm_IP}:{self.port}/')
        if 'Hello' in response.text:
            return True
        return False

    def download(self, file_name) -> bool:
        response = requests.get(f'http://{self.vm_IP}:{self.port}/download/{file_name}')
        if response.status_code == 200:
            try:
                file_data = response.content
                file_path = os.path.join('C:\\', file_name)

                with open(file_path, 'wb') as f:
                    f.write(file_data)
            except Exception as e:
                print(f'{str(e)}')
                return False
            return True
        else:
            return False

    def upload(self, file_path) -> bool:
        try:
            with open(file_path, 'rb') as f:
                file_data = base64.b64encode(f.read()).decode('utf-8')
            data = {'file_name': file_path, 'file_data': file_data}
            response = requests.post(f'http://{self.vm_IP}:{self.port}/upload', json=data)
            
        except Exception as e:
            print(f'Error: {str(e)}')
            return False
        return True

    def commander(self, command):
        data = {'command': '', 'arg': ''}
        command_parts = command.split()
        
        data['command'] = command_parts[0]
        data['arg'] = " ".join(command_parts[1:])

        headers = {'Content-type': 'application/json'}
        response = requests.post(f'http://{self.vm_IP}:{self.port}/command', data=json.dumps(data), headers=headers)

        result = response.json()
        result = (result['data']).encode('ascii')
        result = (base64.b64decode(result)).decode('utf-8')
        
        return result
