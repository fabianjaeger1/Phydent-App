import socket

def check_port_open():

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 443)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        print("Port is open")
    else:
        print("Port is not open")

# Function to communicate with OPUS
def opusrequest(IP,port,command):
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
    #Close connection and provide answer as string    
    s.close()
    return(data.split("\n\r\n"))

# Instruction to the third argumetn of opusrequest can be found in OPUS Programming Chapter 10
# answer=OPUS.opusrequest("127.0.0.1", 80, "COMMAND_LINE LoadFile('/mnt/c/Users/G164.PHYTAX/Desktop/phydent/Leermessung.0', WARNING)")


# Hostname of PC
host = socket.gethostname()
print(host)

localhost = "127.0.0.1"
port = 80

#check_port_open()


# USEFUL FOR WHEN BUTTON TO OPEN OPUS (WITH HTTP CONNECTION)
# subprocess.Popen(['/mnt/c/Program Files/Bruker/OPUS_8.7.10/opus.exe','/Language=ENGLISH/OPUSPIPE=ON/HTTPSERVER=ON/HTTPPORT=80/DIRECTLOGINPASSWORD=Admin@OPUS'])

data = opusrequest(localhost, port, "GET_VERSION")

status = opusrequest(localhost, port, "DIAG_STATUS")
# print(data)
print(status)

path = opusrequest(localhost, port, "GET_OPUSPATH")
opus_path = path[1]
result = opusrequest(localhost, port, "TAKE_REFERENCE")
print(opus_path)
#reference=opusrequest("127.0.0.1", 80, "MeasureReference(0, {EXP='ATR_Di.XPM', XPP='/mnt/c/Users/G164.PHYTAX/Desktop/phydent/', NSR=10})")
#print(reference)
# XpmName = 'python.xpm'
# DefaultPrintout = 2
# hPipe = open("\\.pipe\OPUS", 'r+b', 0)

def main():
    # print("Start of Program")
    global hPipe
    global DefaultPrintout
    global XpmPath
    global XpmName
