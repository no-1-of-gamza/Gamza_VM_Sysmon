import os

class WinlogbeatYML:
    def __init__(self, host_ip):
        self.elasticsearch_host = f"http://{host_ip}:9200"
        self.kibana_host = f"http://{host_ip}:5601"

    def create_config(self):
        Winlogbeat_config = f"""\

winlogbeat.event_logs:
  - name: Application
    ignore_older: 72h

  - name: System

  - name: Security

  - name: Microsoft-Windows-Sysmon/Operational
 
  - name: Windows PowerShell
    event_id: 400, 403, 600, 800

  - name: Microsoft-Windows-PowerShell/Operational
    event_id: 4103, 4104, 4105, 4106

  - name: ForwardedEvents
    tags: [forwarded]

# ====================== Elasticsearch template settings =======================

setup.template.settings:
  index.number_of_shards: 1

# =================================== Kibana ===================================

setup.kibana:
  host: "{self.kibana_host}"

# ---------------------------- Elasticsearch Output ----------------------------
output.elasticsearch:
  hosts: ["{self.elasticsearch_host}"]

  # Pipeline to route events to security, sysmon, or powershell pipelines.
  pipeline: "winlogbeat-%{{[agent.version]}}-routing"
  winlogbeat.period: 60s

# ================================= Processors =================================
processors:
  - add_host_metadata:
      when.not.contains.tags: forwarded
  - add_cloud_metadata: ~
"""

        with open("winlogbeat.yml", "w") as kibana_file:
            kibana_file.write(Winlogbeat_config)

        if os.path.exists("./winlogbeat.yml"):
            return True
        else:
            return False
