import signal
import sys

def SignalHandler_SIGINT(SignalNumber, Frame):
    sys.exit(0)

class Main:
    def __init__(self):
        self.target_vm = ""
        self.target_malware = ""
        self.analyzing = False

    def start(self):
        signal.signal(signal.SIGINT, SignalHandler_SIGINT)

        self.print_welcome()

        while True:
            command = input(">>> ").split(" ")
            if command[0] == "":
                pass

            elif command[0] == "exit":
                break

            elif command[0] == "help":
                self.help()

            elif command[:2] == ["set", "vm"]:
                if len(command) < 3:
                    print("set vm: invalid command\n")
                    self.help()
                    continue
                
                vm_name = " ".join(command[2:])
                self.target_vm = vm_name
                print("The analyze target VM is set to", self.target_vm)

            elif command[:2] == ["set", "malware"]:
                if len(command) < 3:
                    print("set malware: invalid command\n")
                    self.help()
                    continue

                malware_path = " ".join(command[2:])
                self.target_malware = malware_path
                print("The analyze target malware is set to", self.target_malware)

            elif command[:2] == ["list", "vm"]:
                print("list vm")

            elif command[:2] == ["list", "snapshot"]:
                print("list snapshot")
            
            elif command[:2] == ["save", "snapshot"]:
                if len(command) < 4:
                    print("save snapshot: invalid command\n")
                    self.help()
                    continue

                vm_name = " ".join(command[2:4])
                snapshot_name = command[3]
                print(vm_name, snapshot_name)

            elif command[0] == "rollback":
                if len(command) < 3:
                    print("rollback: invalid command\n")
                    self.help()
                    continue

                vm_name = command[1]
                snapshot_name = command[2]
                print(vm_name, snapshot_name)
                
            elif command[:2] == ["start", "analyze"]:
                print("start analyze")

            elif command[:2] == ["stop", "analyze"]:
                print("stop analyze")

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

    def help(self):
        help = {
            "set vm [vm name]": "Set target Virtual Machine's name",
            "set malware [exe path]": "Set target malware execution file's path",
            "list vm": "List available Virtual Machine",
            "list snapshot": "List saved snapshot",
            "save snapshot [vm name] [new snapshot name]": "Take snapshot of current status",
            "rollback [vm name] [snapshot name]": "Rollback to specific snapshot",
            "start analyze": "Start analyze based on set information(vm, malware)",
            "stop analyze": "Stop analyze based on set information(vm, malware)",
            "exit": "Exit shell"
        }

        print("usage:", end="\n\n")
        for command in help.keys():
            print("{0:40s}\t{1:s}".format(command, help[command]))
        print()


if __name__ == "__main__":
    main = Main()
    main.start()