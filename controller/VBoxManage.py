import subprocess

# vm 리스트 확인
def list_vm() -> list:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    command = "list vms"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()
        
    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    vm_list = result.stdout.split("\n")[:-1]
    
    vm_list = parse_vm_list(vm_list)
    return vm_list

def parse_vm_list(vm_list) -> list:
    parsed_list = []
    
    for item in vm_list:
        name_range = list(filter(lambda x: item[x] == '\"', range(len(item))))
        uid_start = item.index("{")
        uid_end = item.index("}")
        
        parsed_list.append([item[name_range[0]+1:name_range[1]], item[uid_start+1:uid_end]])
    
    return parsed_list

# 실행중인 vm 리스트 확인
def list_runningvms() -> list:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    command = "list runningvms"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()
        
    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    running_vm_list = result.stdout.split("\n")[:-1]

    running_vm_list = parse_running_vm(running_vm_list)    
    return running_vm_list

def parse_running_vm(vm_list) -> list:
    parsed_list = []
    
    for item in vm_list:
        name_range = list(filter(lambda x: item[x] == '\"', range(len(item))))
        
        parsed_list.append(item[name_range[0]+1:name_range[1]])
    
    return parsed_list

# vm 시작
def start_vm(vm_name, interface_type) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    command = f"startvm {vm_name} --type {interface_type}"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)

    return result.returncode

# vm 종료
def stop_vm(vm_name) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]
    
    command = f"controlvm {vm_name} poweroff"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)

    return result.returncode

# 스냅샷 리스트 확인
def list_snapshot(vm_name) -> list:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    command = f"snapshot {vm_name} list --details"      # --details옵션(세부정보)은 제외 가능
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    snapshot_list = result.stdout.split(")")[:-1]
    
    snapshot_list = parse_snapshot_list(snapshot_list)
    return snapshot_list

def parse_snapshot_list(snapshot_list) -> list:
    parsed_list = []
    
    for item in snapshot_list:
        separator_index = list(filter(lambda x: item[x] == ':', range(len(item))))
        
        parsed_list.append([item[separator_index[0]+2:separator_index[1]-6], item[separator_index[1]+2:]])
    
    return parsed_list

# 스냅샷 생성
def snapshot_vm(vm_name, snapshot_name) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    command = f"snapshot {vm_name} take {snapshot_name} --live "
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)

    return result.returncode

# 스냅샷 삭제
def snapshot_delete(vm_name, snapshot_name) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    command = f"snapshot {vm_name} delete {snapshot_name}"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)

    return result.returncode

# 스냅샷 시점으로 롤백
def rollback_vm(vm_name, snapshot_name) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]
    
    command = f"snapshot {vm_name} restore {snapshot_name}"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    
    return result.returncode
