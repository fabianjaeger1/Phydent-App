localhost = "127.0.0.1"
port = 80

def main():
    print("Start of Program")
    global hPipe
    global DefaultPrintout
    global XpmPath
    global XpmName

    # Define Globals
    XpmName = 'python.xpm'
    DefaultPrintout = 2 # set bit 1 to print out the pipe commands, set bit 2 to print out the return strings (3 does both)
    print("hello")


def PipeCommand(cmd, show):
    if (show == -1) : show = DefaultPrintout
    if (show & 1) : print(cmd)

    hPipe.write(bytes(cmd + '\r\n', 'utf-8'))
    data = hPipe.read(1000)
    Mystr = data.decode('utf-8')
    total = Mystr
    if show & 2 : print(total)
    return total

if __name__ == "__main__":
    main()

host = socket.gethostname()
print(host)
