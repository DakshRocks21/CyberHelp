import os, sys
from datetime import datetime

cwd = os.getcwd()


class Logger(): 
    log_count = 0
    error_count = 0
    applicationIdentifier = "root"
    level = 0
    logging_path = os.path.expandvars(f'{cwd}/logs')
    def __init__(self):
        if self.level == None:return "Pls set a level"
        if not os.path.exists(self.logging_path):
            os.makedirs(self.logging_path)
        if self.applicationIdentifier == None:
            logging_file = os.path.join(self.logging_path, f"[{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}].log")
            open(logging_file, 'a').close()
        else:
            logging_file = os.path.join(self.logging_path, f"{self.applicationIdentifier}_[{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}].log")
            open(logging_file, 'a').close()
        self.logging_file = logging_file

    def config(self, level, name = None):
        if name == None:self.warn("Please set an applicationIdentifier")
        else: self.applicationIdentifier = name
        if level == "DEBUG":
            self.level = 0
        elif level == "INFO":
            self.level = 10
        elif level == "WARN":
            self.level = 20
        elif level == "ERROR":
            self.level = 30
        elif level == "CRITICAL":
            self.level = 40
        else:
            self.warn("Looging level Set as DEBUG")
            self.level = 0

    def debug(self, item):
        if self.level > 0:
            pass
        else:
            with open(self.logging_file, "a") as file:
                file.write(f"[{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}] [{self.applicationIdentifier}/DEBUG]: {item}\n")
            print(f"[DEBUG]: {item}")
            self.log_count += 1

    def info(self, item):
        if self.level > 10:
            pass
        else:
            with open(self.logging_file, "a") as file:
                file.write(f"[{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}] [{self.applicationIdentifier}/INFO]: {item}\n")
            print(f"[INFO]: {item}")
            self.log_count += 1

    def warn(self, item):
        if self.level > 20:
            pass
        else:
            with open(self.logging_file, "a") as f:
                f.write(f"[{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}] [{self.applicationIdentifier}/WARN]: {item}\n")
            print(f"[WARN]: {item}")
            self.error_count += 1

    def error(self, item):
        if self.level > 30:
            pass
        else:
            with open(self.logging_file, "a") as f:
                f.write(f"[{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}] [{self.applicationIdentifier}/ERROR]: {item}\n")
            print(f"[ERROR]: {item}")
            self.error_count += 1

    def critical(self, item):
        if self.level > 40:
            pass
        else:
            with open(self.logging_file, "a") as file:
                file.write(f"[{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}] [{self.applicationIdentifier}/CRITICAL]: {item}\n\n\n")
            input(f"[CRITICAL]: {item}\n\n[LOGS]: {self.logging_file}\n{self.get_logs()}\n\n[Enter to Shutdown]")
            sys.exit(-1)

    def summary(self):
        text = f"[SUMMARY]: Logs = {self.log_count} | Error = {self.error_count}"
        with open(self.logging_file, "a") as f:
            f.write(f"[{datetime.now().strftime('%d-%b-%y_%H:%M:%S')}] {text} \n")
        print(f"{info}")
        return text

    def get_logs(self):
        with open(self.logging_file, "r") as f:
            logs = f.read()
        return logs



