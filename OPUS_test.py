import socket as socket
import numpy as np
import os
import re
import time
import pandas as pd
import sys 

'''Serves as testing ground for the OPUS functions'''


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
                #print("data")
        #Close connection and provide answer as string    
        s.close()
        return(data.split("\n\r\n"))

# cwdir = os.getcwd()
# print(cwdir)
# workdir = re.escape(cwdir)
#reference=opusrequest("127.0.0.1", 80, "MeasureReference(0, {EXP='ATR_Di.XPM', XPP='/mnt/c/Users/G164.PHYTAX/Desktop', NSR=10})")
#answer=opusrequest("127.0.0.1", 80, "COMMAND_LINE LoadFile('/mnt/c/Users/G164.PHYTAX/Desktop/Leermessung.0', WARNING)")
#sample=opusrequest("127.0.0.1", 80, "MeasureSample(0, {EXP='ATR_Di.XPM', XPP='/mnt/c/Users/G164/Desktop', NSR=10})")
#command = opusrequest("127.0.0.1", 80,"MeasureSample(0, {{EXP='ATR_Di.XPM', XPP='{}\\XPM', NSR=10}})".format(workdir))
#command = opusrequest("127.0.0.1", 80,"MeasureSample(0, {EXP='ATR_Di.XPM', XPP='C:\\User\\G164.PHYTAX\\Desktop\\Phydent-App\\XPM\\', NSR#=10})")


def get_x_values(path_leermessung, host, port):



    """This function generates the x-values of a specific leermessung. 

    Returns:
        x_points: x values of the spectrum 
    """

    pfad_leermessung_spektrum = f'"{path_leermessung}":AB'
    file = opusrequest(host, port, "LOAD_FILE %s" % str(path_leermessung))
    time.sleep(1)
    compatible = opusrequest(host, port, "COMMAND_LINE MakeCompatible ([%s], [%s], {});" % (
        pfad_leermessung_spektrum, pfad_leermessung_spektrum))
    read2 = opusrequest(
        host, port, "READ_FROM_FILE %s;" % pfad_leermessung_spektrum)
    read3 = opusrequest(host, port, "READ_FROM_BLOCK AB")
    read4 = opusrequest(host, port, "READ_HEADER")
    read = opusrequest(host, port, "READ_DATA")

    data = np.array(read[1].splitlines()).astype("float64")
    nr_points, upperx, lowerx, data_processed = data[0], data[1], data[2], data[4:]
    delta_x = (upperx - lowerx)/(nr_points-1)
    x_points = list(
        reversed([lowerx + x*delta_x for x in range(int(nr_points))]))
    unload = opusrequest(
        host, port, "UNLOAD_FILE %s" % str(path_leermessung))

    return x_points, len(x_points), lowerx, delta_x



####################

def test():
    host = "127.0.0.1"
    port = 80
    path_leermessung = "K:\\Phydent\\V22celinetest\\Leermessungen\\Leermessung.0"

    pfad_leermessung_spektrum = f'"{path_leermessung}":AB'
    x_values_leer, _, lowerx_leer, deltax_leer = get_x_values(path_leermessung, host, port)
    answer= opusrequest("127.0.0.1", 80, "COMMAND_LINE LoadFile('/mnt/c/Users/G164.PHYTAX/Desktop/phydent/Leermessung.0', WARNING)")
    command = opusrequest("127.0.0.1", 80, "MeasureSample(0, {EXP='ATR_Di.XPM', XPP='C:\\Users\\G164\\Desktop', NSS=1)")
    #print(command)
    #Obtain information about selected/just measured spectrum
    filenames=opusrequest("127.0.0.1", 80,"GET_SELECTED")
    #Extract absolute path to file
    file_path =  '{}'.format(filenames[1])
    print(file_path)
    #spectrum_path = f'"{file_path}":AB'
    #Save the file into the appropriate Phydent Folder
    #save = opusrequest("127.0.0.1", 80, "SaveAs([%s], {SAN=%s, DAP='%s'})" % (file_path, new_file_name, target_path))
    compatible= opusrequest("127.0.0.1", 80,"COMMAND_LINE MakeCompatible ([%s], [%s], {});" % (pfad_leermessung_spektrum, file_path))
    print(compatible)


#test2()


def measuring():
    host = "127.0.0.1"
    port = 80
    target_path = 'C:\\Users\\G164\\Desktop'
    new_file_name = 'test'
    path_leermessung = "K:\\Phydent\\V22celinetest\\Leermessungen\\Leermessung.0"

    #Check Status of OPUS
    status =  opusrequest("127.0.0.1", 80, "DIAG_STATUS")

    #Get OPUS Path
    path =  opusrequest("127.0.0.1", 80, "GET_OPUSPATH")
    opus_path = path[1]
    #print(path[1])
    
    #Obtain the x-values from Leermessung
    x_values_leer, _, lowerx_leer, deltax_leer = get_x_values(path_leermessung, host, port)

    columns = ["Filename", "Product", "Dataset", "Augmented"]
    columns = [columns.append(i) for i in x_values]
    data1 = pd.DataFrame(columns=["Filename", "Product", "Dataset", "Augmented"])
    data = data1.join(pd.DataFrame(columns=x_values))

    #Perform a Measurement
    command = opusrequest("127.0.0.1", 80, "MeasureSample(0, {EXP='ATR_Di.XPM', XPP='C:\\Users\\G164\\Desktop', NSS=1, XPM = 'Test'})")
    print(command)
    'Obtain information about selected/just measured spectrum'
    filenames=opusrequest("127.0.0.1", 80,"GET_SELECTED")
    'Extract absolute path to file'
    file_path =  '{}'.format(filenames[1])
    #Save the file into the appropriate Phydent Folder
    save = opusrequest("127.0.0.1", 80, "SaveAs([%s], {SAN=%s, DAP='%s'})" % (file_path, new_file_name, target_path))

    #Read Raw Spectrum Data
    # read2 = opusrequest("127.0.0.1", 80, "READ_FROM_FILE %s;" % file_path)
    # read3 = opusrequest("127.0.0.1", 80, "READ_FROM_BLOCK AB")
    # read4 = opusrequest("127.0.0.1", 80, "READ_HEADER")
    # read = opusrequest("127.0.0.1", 80, "READ_DATA")

    # #Split Data from read array (raw data)
    # data = np.array(read[1].splitlines()).astype("float64")
    # nr_points, upperx, lowerx, data_processed = data[0], data[1], data[2], data[4:]
    # delta_x = (upperx - lowerx)/(nr_points-1)
    # x_points = list(reversed([lowerx + x*delta_x for x in range(int(nr_points))]))

    filename_raw = f"out_raw_measurement.txt"
    filename_pre = f"out_pre_measurement.txt"
    product =  "test"
    # measurement_data_raw = [filename_raw, product, "original"]

    #Split Data from read array 
    derivative = opusrequest(host, port, "COMMAND_LINE Derivative ([%s], {QSP=13, QOD=1});" % file_path)
    normalization = opusrequest(host, port, "COMMAND_LINE  Normalize ([%s], {NME=2, NFX=4000.000000, NLX=400.000000, NWR=1});" % file_path)
    time.sleep(2)
    read2 = opusrequest(host, port, "READ_FROM_FILE %s;" % file_path)
    read3 = opusrequest(host, port, "READ_FROM_BLOCK AB/1.Der.")
    read4 = opusrequest(host, port, "READ_HEADER")
    read = opusrequest(host, port, "READ_DATA")

    data = np.array(read[1].splitlines()).astype("float64")
    nr_points, upperx, lowerx, data_processed = data[0], data[1], data[2], data[4:]
    delta_x = (upperx - lowerx)/(nr_points-1)
    x_points = list(reversed([lowerx + x*delta_x for x in range(int(nr_points))]))
    measurement_data_dernorm = [filename_pre, product, "classification", "original"]

    # if len(data_processed) < len(x_points):
    #     pointsatbeginning = round(
    #                         np.abs(lowerx- ) // delta_x)
    #                     for i in range(pointsatbeginning):
    #                         measurement_data_dernorm.append(np.nan)
    
    #measurement_data_dernorm = [filename_raw, product, mode, "original"]

    #data_processed: y-values of spectrum
    #x_points: x-values of spectrum
    print(x_points)
    print(len(data_processed))
    print(nr_points)
    # print(x_points[400], data_processed[400])
    # print(x_points[600], data_processed[600])

    # Loads into CSV File
    columns = ["Filename", "Product", "Dataset", "Augmented"]
    columns = [columns.append(i) for i in x_points]
    data1 = pd.DataFrame(columns=["Filename", "Product", "Dataset", "Augmented"])
    csvlist_pre = data1.join(pd.DataFrame(columns=x_points))

  
    #Ignore raw since we don't need it

    #Unload File
    #unload = opusrequest("127.0.0.1", 80, "UNLOAD_FILE %s" % str(file_name))
    ####################

command = opusrequest("127.0.0.1", 80, "MeasureSample(0, {NSS=24,EXP='ATR_Di_Phydent.XPM', XPP='C:\\Users\\G164\\Desktop\\Phydent-App\\XPM\\ATR_Di_Phydent.XPM')")
#derivative = opusrequest("127.0.0.1", 80, "COMMAND_LINE Derivative ([%s], {QSP=13, QOD=1});" % file_path)
#normalization = opusrequest("127.0.0.1", 80, "COMMAND_LINE  Normalize ([%s], {NME=2, NFX=4000.000000, NLX=400.000000, NWR=1});" % file_path)
# print(file_name)
# print(filenames)
#opusrequest("127.0.0.1", 80, "SaveAs(0, {SAN='test.0', DAP='C:\\Users\\G164\\Desktop'})")



#read6 = opusrequest("127.0.0.1", 80, "READ_DATA")
#data = np.array(read6[1].splitlines()).astype("float64")
#nr_points, upperx, lowerx, data_processed = data[0], data[1], data[2], data[4:]
#delta_x = (upperx - lowerx)/(nr_points-1)
#x_points = list(reversed([lowerx + x*delta_x for x in range(int(nr_points))]))

#print(data)



#sample=opusrequest("127.0.0.1", 80, "MeasureSample(0, {EXP='ATR_Di.XPM', XPP='/mnt/c/Users/G164.PHYTAX/Desktop/phydent/', NSR=10})")