class Log:
    def __init__(self):
        self.log_file = open("C:\\Users\\user\\Documents\\agent\\agent.log.txt", "w")
    
    def write(self, msg):
        try:
            self.log_file.write(msg+"\n")
        except Exception as e:
            return False
        return True
    
    def close(self):
        try:
            self.log_file.close()
        except Exception as e:
            return False
        return True