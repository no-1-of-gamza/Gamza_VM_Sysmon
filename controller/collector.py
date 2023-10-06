import subprocess
import os
import sys
import time

from shutil import copyfile
import psutil

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from setting.host import KibanaYML

class Elasticsearch:
    def __init__(self):
        self.pid = os.getpid()
        
    def status(self):
        for proc in psutil.Process(self.pid).children(recursive=True):
            if proc.name() == "CONTRO~1.EXE":
                return True
        return False

    def start(self):
        try:
            args = ["C:\\elasticsearch\\bin\\elasticsearch.bat"]
            process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            
        except Exception:
            print("Failed to start elasticsearch. Please check your elasticsearch in C drive\n")
            return False
        
        print("ready to start elasticsearch...")
        
        while True:
            msg = process.stdout.readline()
            if not msg:
                break
            
            decoded_msg = msg.decode('utf-8')
            if "starting ..." in decoded_msg:
                return True
        
        return False
    
    def stop(self):
        if not self.status():
            print("ElasticSearch is already stopped")
            return True
        
        for child in psutil.Process(self.pid).children(recursive=True):
            if child.name() == "java.exe":
                child.kill()
                break
        time.sleep(5)
        
        self.process = None
        
        return not self.status()

class Kibana:
    def __init__(self):
        self.pid = os.getpid()
    
    def status(self):
        for proc in psutil.Process(self.pid).children(recursive=True):
            if proc.name() == "node.exe":
                return True
        return False
    
    def config(self):
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
        
        return True
    
    def start(self):
        is_success = self.config()
        if not is_success:
            return False

        try:
            args = ["C:\\kibana\\bin\\kibana.bat"]
            process = subprocess.Popen(args, stdout=subprocess.PIPE)
            
        except Exception:
            print("Failed to start kibana. Please check your kibana in C drive\n")
            return False
        
        print("ready to start kibana...")
        
        while True:
            msg = process.stdout.readline()
            if not msg:
                break
            
            decoded_msg = msg.decode('utf-8')
            if "Kibana is starting" in decoded_msg or "Kibana is currently running" in decoded_msg:
                return True
        
        return False
    
    def stop(self):
        if not self.status():
            print("Kibana is already stopped")
            return True
        
        for child in psutil.Process(self.pid).children(recursive=True):
            if child.name() == "node.exe":
                child.kill()
                break
        time.sleep(5)
        
        self.process = None
        
        return not self.status()
    