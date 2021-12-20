#from PyQt5.QCore import QObject, QThread, pyqtSignal
from PyQt5.QtCore import *
import socket

#Worker Thread in most cases
class OPUS_coms(QThread):
    #For tracking the state of the worker thread
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    IP = "127.0.0.1"
    port = 80
    path = ""

    def __init__(self):
        QThread.__init__(self)
        print("Thread created")

    def run(self):
        command = "MeasureReference(0, {{EXP='ATR_Di.XPM', XPP={}, NSR=10}}".format(self.path)
        command=command.replace(" ", "%20")
        request="GET /OpusCommand.htm?" + command + "\r\n\r\n"
        # print(request)
        data = ""
        part = None

        #request to OPUS
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.IP,self.port))
        s.sendall(request.encode("windows-1252"))
        #construct answer partially from "byte stream"
        while True:
            part = s.recv(1048576)  # 2^20 bytes = 1 MByte        
            if (part == b''):
                break;  
            else:
                data += part.decode("windows-1252")
                print("data")
        #Close connection and provide answer as string    
        s.close()
        self.finished.emit()
        #return(data.split("\n\r\n")) 


    """Long running class method"""
    def opusrequest(self, IP,port,command):
    # print(socket.gethostbyname(socket.gethostname()))
        command=command.replace(" ", "%20")
        request="GET /OpusCommand.htm?" + command + "\r\n\r\n"
        # print(request)
        data = ""
        part = None

        #request to OPUS
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP,port))
        s.sendall(request.encode("windows-1252"))
        #construct answer partially from "byte stream"
        while True:
            part = s.recv(1048576)  # 2^20 bytes = 1 MByte        
            if (part == b''):
                break;  
            else:
                data += part.decode("windows-1252")
                print("data")
        #Close connection and provide answer as string    
        s.close()
        return(data.split("\n\r\n"))

    def opusrequest_fireandforget(self,IP,port,command):
        # print(socket.gethostbyname(socket.gethostname()))
        command=command.replace(" ", "%20")
        request="GET /OpusCommand.htm?" + command + "\r\n\r\n"
        # print(request)
        data = ""
        part = None

        #request to OPUS
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP,port))
        s.sendall(request.encode("windows-1252"))
        #construct answer partially from "byte stream"
        s.close()