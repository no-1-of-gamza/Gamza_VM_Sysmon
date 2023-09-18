import subprocess

# vm 리스트 가져오기
def list_vm() -> list:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    command = "list vms"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()
        
    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    print(result)
    
    return result

# vm 시작
def start_vm(vm_name) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    # vm 실행 옵션 선택
    type = ''
    type_num = input("Do you want to run a virtual machine with a gui type? <yes/no>\n>> ")
    if type_num == 'yes':       # gui
        type = 'gui'
    else:                       # gui를 띄우지 않음
        type = 'headless'

    command = f"startvm {vm_name} --type {type}"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    print(result)

    return result.returncode

# vm 종료
def stop_vm(vm_name) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]
    
    command = f"controlvm {vm_name} poweroff"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    print(result)

    return result.returncode

# 스냅샷 생성
def snapshot_vm(vm_name, snapshot_name) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]

    command = f"snapshot {vm_name} take {snapshot_name} --live "
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    print(result)

    return result.returncode

# 스냅샷 시점으로 롤백
def rollback_vm(vm_name, snapshot_name) -> bool:
    vboxmanage_path = "C:\\Program Files\\Oracle\\VirtualBox\\vboxmanage.exe"
    vboxmanage_cmd = [vboxmanage_path]
    
    command = f"snapshot {vm_name} restore {snapshot_name}"
    vboxmanage_cmd = vboxmanage_cmd[0:1] + command.split()

    result = subprocess.run(vboxmanage_cmd, stdout=subprocess.PIPE, text=True)
    print(result)
    
    return result.returncode
