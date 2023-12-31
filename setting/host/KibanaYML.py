import socket
import os

class KibanaYML:
    def __init__(self):
        self.elasticsearch_host = f"http://{self.get_local_ip()}:9200"

    def get_local_ip(self):
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            return local_ip
        except Exception as e:
            print(f"IP 주소를 가져오는 중 오류 발생: {e}")
            return False

    def create_config(self):
        kibana_config = f"""\
server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["{self.elasticsearch_host}"]
elasticsearch.requestTimeout: 180000
elasticsearch.username: "kibana"
elasticsearch.password: "111111"

logging.root.level: info
logging.appenders.default:
  type: file
  fileName: C:\\kibana\\logs\\kibana.log
  layout:
    type: json
"""

        with open("kibana.yml", "w") as kibana_file:
            kibana_file.write(kibana_config)

        if os.path.exists("./kibana.yml"):
            return True
        else:
            return False
