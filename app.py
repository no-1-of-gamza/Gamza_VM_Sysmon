import signal
import sys
import os

from controller import VBoxManage

class Main:
    def __init__(self):
        self.target_vm = "None"
        self.target_malware = "None"
        self.analyzing = False
        
    def SignalHandler_SIGINT(self, SignalNumber, Frame):
        self.exit()
        
    def init_status(self):
        # 1. get list of all vms
        # 2. run vm & execute server (agent.py)
        # 3. take a snapshot of all vm's initial status
        
        pass

    def start(self):
        signal.signal(signal.SIGINT, self.SignalHandler_SIGINT)

        self.print_welcome()

        while True:
            command = input(">>> ").split(" ")
            if command[0] == "":
                pass

            elif command[0] == "exit":
                option = input("Are you sure to exit program? Your snapshots and logs will be deleted. <yes(default)/no>: ")
                option = option.lower()
                if option == 'no' or option == 'n':
                    continue
                
                self.exit()

            elif command[0] == "help":
                self.help()
                
            elif command[0] == "status":
                self.get_status()

            elif command[:2] == ["set", "vm"]:
                if len(command) < 3:
                    print("set vm: invalid command\n")
                    self.help()
                    continue
                
                vm_name = command[2]
                self.set_vm(vm_name)
                
            elif command[:2] == ["set", "malware"]:
                if len(command) < 3:
                    print("set malware: invalid command\n")
                    self.help()
                    continue
                
                malware_path = command[2]
                self.set_malware(malware_path)

            elif command[:2] == ["list", "vm"]:
                self.list_vm()
            
            elif command[:2] == ["list", "snapshot"]:
                if len(command) < 3:
                    print("list snapshot: invalid command\n")
                    self.help()
                    continue
                
                vm_name = command[2]
                self.list_snapshot(vm_name)
            
            elif command[:2] == ["take", "snapshot"]:
                if len(command) < 3:
                    print("take snapshot: invalid command\n")
                    self.help()
                    continue

                snapshot_name = command[2]
                self.take_snapshot(snapshot_name)

            elif command[0] == "rollback":
                if len(command) < 2:
                    print("rollback: invalid command\n")
                    self.help()
                    continue

                snapshot_name = command[1]
                self.rollback_snapshot(snapshot_name)
                
            elif command[:2] == ["start", "analyze"]:
                self.start_analyze()

            elif command[:2] == ["stop", "analyze"]:
                self.stop_analyze()

            else:
                print("\'{}\' is invalid command.\n".format(" ".join(command)))
                self.help()

    def print_welcome(self):
        welcome_message = """
        _______ _______ __   __ _______ _______ __ _______                                                                 
        |       |   _   |  |_|  |       |   _   |  |       |                                                                
        |    ___|  |_|  |       |____   |  |_|  |__|  _____|                                                                
        |   | __|       |       |____|  |       |  | |_____                                                                 
        |   ||  |       |       | ______|       |  |_____  |                                                                
        |   |_| |   _   | ||_|| | |_____|   _   |   _____| |                                                                
        |_______|__| |__|_|   |_|_______|__| |__|  |_______|                                                                
        __   __ _______ ___     _     _ _______ ______   _______   _______ _______ __    _ ______  _______ _______ __   __ 
        |  |_|  |   _   |   |   | | _ | |   _   |    _ | |       | |       |   _   |  |  | |      ||  _    |       |  |_|  |
        |       |  |_|  |   |   | || || |  |_|  |   | || |    ___| |  _____|  |_|  |   |_| |  _    | |_|   |   _   |       |
        |       |       |   |   |       |       |   |_||_|   |___  | |_____|       |       | | |   |       |  | |  |       |
        |       |       |   |___|       |       |    __  |    ___| |_____  |       |  _    | |_|   |  _   ||  |_|  ||     | 
        | ||_|| |   _   |       |   _   |   _   |   |  | |   |___   _____| |   _   | | |   |       | |_|   |       |   _   |
        |_|   |_|__| |__|_______|__| |__|__| |__|___|  |_|_______| |_______|__| |__|_|  |__|______||_______|_______|__| |__|

        To know how to use, use 'help' command.
        Have a nice time ~
        """
        
        print(welcome_message)

    def exit(self):
        
        # 1. Check any vm are current running(analyzing). If yes, 
        # 2. Rollback all vm to initial snapshot.
        # 3. Remove all snapshots for each vm except init_snapshot.
        
        sys.exit(0)

        
    def help(self):
        help = {
            "status": "Show current target vm/malware",
            "set vm [vm name]": "Set target Virtual Machine's name",
            "set malware [exe path]": "Set target malware execution file's path",
            "list vm": "List available Virtual Machine",
            "list snapshot [vm name]": "List saved snapshot",
            "take snapshot [new snapshot name]": "Take snapshot of current analyzing status",
            "rollback [snapshot name]": "Rollback current vm to specific snapshot",
            "start analyze": "Start analyze based on set information(vm, malware)",
            "stop analyze": "Stop analyze based on set information(vm, malware)",
            "exit": "Exit shell"
        }

        print("usage:", end="\n\n")
        for command in help.keys():
            print("{0:35s}\t{1:s}".format(command, help[command]))
        print()
        
    def get_status(self):
        if self.analyzing:
            print("Analyzing: {}".format("Running"))
        else:
            print("Analyzing: {}".format("Stopped"))
        
        print("\nTarget VM: {}".format(self.target_vm))
        print("Target Malware: {}\n".format(self.target_malware))
        
    def set_vm(self, vm_name):
        if self.analyzing:
            print("Cannot change target VM during analyzing\n")
            return
        
        vm_list = VBoxManage.list_vm()
        
        for vm in vm_list:
            if vm[0] == vm_name:
                self.target_vm = vm_name
                print("The analyze target VM is set to {}\n".format(self.target_vm))
                return
        
        print("Cannot be founded the VM name: \'{}\'\n".format(vm_name))
        
    def set_malware(self, malware_path):
        if self.analyzing:
            print("Cannot change target malware during analyzing\n")
            return
        if not os.path.exists(malware_path):
            print("File path is invalid\n")
            return
        if malware_path.split(".")[-1] != "exe":
            print("Only exe file is supported\n")
            return
        
        self.target_malware = malware_path
        print("The analyze target malware is set to {}\n".format(self.target_malware))
    
    def list_vm(self):
        vm_list = VBoxManage.list_vm()
            
        print("{0:15s}\t {1:40s}\t {2:s}".format("name", "uid", "status"))
        for vm in vm_list:
            if self.analyzing and vm[0] == self.target_vm:
                status = "analyzing"
            else:
                status = "off"
            print("{0:15s}\t {1:40s}\t {2:s}".format(vm[0], vm[1], status))
        print()
        
    def list_snapshot(self, vm_name):
        list_snapshot = VBoxManage.list_snapshot(vm_name)
                
        print("{0:15s}\t {1:s}".format("name", "uuid"))
        for snapshot in list_snapshot:
            print("{0:15s}\t {1:s}".format(snapshot[0], snapshot[1]))
        print()
        
    def take_snapshot(self, snapshot_name):
        running_vms = VBoxManage.list_runningvms()
        if self.target_vm not in running_vms:
            print("Failed to take a snapshot because the Target VM is not analyzing\n")
            return
        
        is_error = VBoxManage.snapshot_vm(self.target_vm, snapshot_name)
        if is_error:
            print("Failed to take snapshot. Please try again\n")
        else:
            print("Success to take snapshot: {}\n".format(snapshot_name))
    
    def rollback_snapshot(self, snapshot_name):
        running_vms = VBoxManage.list_runningvms()
        if self.target_vm in running_vms:
            print("Failed to rollback a snapshot because the Target VM is running\n")
            return
        
        is_error = VBoxManage.rollback_vm(self.target_vm, snapshot_name)
        if is_error:
            print("Failed to rollback snapshot. Please try again\n")
        else:
            print("Success to rollback snapshot: {}\n".format(snapshot_name))
    
    def start_analyze(self):
        if self.target_vm == "None":
            print("Target VM is not setting. Cannot start analyzing\n")
            return
        if self.target_malware == "None":
            print("Target Malware path is not setting. Cannot start analyzing\n")
            return
        if self.analyzing:
            print("Analysis is already in progress. Please try again after finishing\n")
            return
        
        interface_type = ''
        option = input("Do you want to run a virtual machine with a gui type? <yes/no(default)>: ")
        option = option.lower()
        if option == 'yes' or option == 'y':
            interface_type = 'gui'
        else:
            interface_type = 'headless'
            
        is_error = VBoxManage.start_vm(self.target_vm, interface_type)
        if is_error:
            print("Failed to start VM. Please try again\n")
            return
        
        print("Start VM...")
        
        # 1. upload malware to vm
        # 2. start sysmon & event log collector (guest, host)
        # 3. execute malware
        
        self.analyzing = True
        print("Everything is ready. The analysis begins\n")
    
    def stop_analyze(self):
        if not self.analyzing:
            print("There is no analysis in progress\n")
            return
        
        # 1. rollback to initial snapshot
        # 2. stop log view (host)
        
        is_error = VBoxManage.stop_vm(self.target_vm)
        if is_error:
            print("Failed to stop VM. Please try again\n")
            return
        
        self.analyzing = False
        print("Analysis has been stopped. All states are reset\n")


if __name__ == "__main__":
    main = Main()
    main.start()