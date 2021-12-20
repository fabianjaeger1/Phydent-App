import socket

def check_port_open():

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = ("127.0.0.1", 443)
    result_of_check = a_socket.connect_ex(location)

    if result_of_check == 0:
        print("Port is open")
    else:
        print("Port is not open")


def opusrequest_fireandforget(IP,port,command):
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
    s.close()

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
    part = s.recv(1048576)
    if (part != b''):
        data += part.decode("windows-1252 ")
    # while True:
    #     part = s.recv(1048576)  # 2^20 bytes = 1 MByte        
    #     if (part == b''):
    #        break;
    #     else:
    #         data += part.decode("windows-1252")
    #Close connection and provide answer as string    
    s.close()
    return(data.split("\n\r\n"))