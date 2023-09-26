import subprocess
from shutil import copyfile
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from setting.host import KibanaYML

class Elasticsearch:
    def __init__(self):
        self.process = None
        
    def status(self):
        if self.process == None:
            print("Elasticsearch didn't start yet")
            return False
        
        if self.process.poll() == None:
            return True
        else:
            return False

    def start(self):
        try:
            args = ["C:\\elasticsearch\\bin\\elasticsearch.bat"]
            self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
        except Exception:
            print("Failed to start elasticsearch. Please check your elasticsearch in C drive\n")
            return False
        
        print("ready to start elasticsearch...")
        
        while True:
            msg = self.process.stdout.readline()
            if not msg:
                break
            
            if "starting ..." in msg.decode('utf-8'):
                return True
        
        return False
    
    def stop(self):
        if self.process == None:
            print("Elasticsearch didn't start yet")
            return False
        
        result = self.process.kill()
        self.process = None
        
        return result

class Kibana:
    def __init__(self):
        self.process = None
    
    def status(self):
        if self.process == None:
            print("Kibana didn't start yet")
            return False
        
        if self.process.poll() == None:
            return True
        else:
            return False
    
    def start(self):
        yml = KibanaYML.KibanaYML()
        is_error = yml.create_config()
        if not is_error:
            print("Failed to create kibana configuration file. Try again\n")
            return False
        
        current_path = os.path.join(os.getcwd(), "kibana.yml")
        try:
            copyfile(current_path,'C:\\kibana\\config\\kibana.yml')
        except Exception:
            print("Failed to move kibana.yml. Please check your kibana.yml file in kibana folder\n")
            return False

        try:
            args = ["C:\\kibana\\bin\\kibana.bat"]
            self.process = subprocess.Popen(args, stdout=subprocess.PIPE)
            
        except Exception:
            print("Failed to start kibana. Please check your kibana in C drive\n")
            return False
        
        print("ready to start kibana...")
        
        while True:
            msg = self.process.stdout.readline()
            if not msg:
                break
            
            if "Kibana is starting" in msg.decode('utf-8'):
                return True
        
        return False
    
    def stop(self):
        if self.process == None:
            print("Kibana didn't start yet")
            return False
        
        result = self.process.terminate()
        self.process = None
        
        return result
    