#from PyQt5.QCore import QObject, QThread, pyqtSignal
from email.mime import base
from unittest import skip
from PyQt5.QtCore import *
import socket
import numpy as np
import os
import pandas as pd
import time
from pathlib import Path
from datetime import datetime


#from shutil import copyfile
from shutil import copy2

'''Define path relative to the project folder'''
basedir = os.path.dirname(__file__)

'''
os.path.join(basedir, "Icons", "phydent-logo-2x.png")
'''


def opusrequest(IP,port,command):
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


#  def obtain_x_values(host, port):

#         #pfad_leermessung_spektrum = f'"{path_leermessung}":AB'
#         #file = OPUS.opusrequest(host, port, "LOAD_FILE %s" % str(path_leermessung))
#         #time.sleep(1)
#         #compatible = OPUS.opusrequest(host, port, "COMMAND_LINE MakeCompatible ([%s], [%s], {});" % (pfad_leermessung_spektrum, pfad_leermessung_spektrum))
#         read2 = OPUS.opusrequest(host, port, "READ_FROM_FILE %s;" % pfad_leermessung_spektrum)
#         read3 = OPUS.opusrequest(host, port, "READ_FROM_BLOCK AB")
#         read4 = OPUS.opusrequest(host, port, "READ_HEADER")
#         read = OPUS.opusrequest(host, port, "READ_DATA")

#         data = np.array(read[1].splitlines()).astype("float64")
#         nr_points, upperx, lowerx, data_processed = data[0], data[1], data[2], data[4:]
#         delta_x = (upperx - lowerx)/(nr_points-1)
#         x_points = list(reversed([lowerx + x*delta_x for x in range(int(nr_points))]))
#         #unload = OPUS.opusrequest(host, port, "UNLOAD_FILE %s" % str(path_leermessung))

#         return x_points, len(x_points), lowerx, delta_x     

class OPUS_spectra_measurement(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    #settings = QSettings("Phytax", "Phydent")
    #path_measurement = settings.value("data_path")

    def __init__(self):
        QThread.__init__(self)
        print("Thread created")

class OPUS_measurement(QThread):


    finished = pyqtSignal()
    progress = pyqtSignal(int)

    #Defining Global Variables
    settings = QSettings("Phytax", "Phydent")
    spectra_save_path = settings.value("data_path")
    host = "127.0.0.1"
    port = 80
    #target_path = "C:\\Users\\G164\\Desktop"
    # target_path = path
    new_file_name = 'test.0'
    #path_leermessung = "C:\\Users\\G164\\Desktop\\Phydent-App\\Leermessung.0"
    path_leermessung = os.path.join(basedir, "app_resources", "Leermessung.0")
    XPM_path = os.path.join(basedir, "XPM", "ATR_Di_Phydent")


    #=======================================================
    #=======================================================

    def CheckInstrumentStatus(self):
        arr = str(self.opusrequest(self.host, self.port, "DIAG_STATUS")[0])[:-2]
        if (arr == "OK"):
            print("Instrument is connected")
            return True
            # number = int(arr[1])
            # if (number == -1):
            #     print("\nNo instrument connected. Check 'Measure/Setup optics and services'.")
            #     return False
            # if (number == 1):
            #     print("\nInstrument warnings present. Nevertheless measurements are possible")
            #     return True
            # if (number == 2):
            #     print("\nInstrument errors present. Measurement not possible")
            #     return False
            # # if (number == 0):
            #     print("\nConnection to instrument is ok")
            #     return True
        print("Command 'DIAG_STATUS' was not succesful.")
        return False

    def GetVersion(self):
        return (self.opusrequest(self.host, self.port, "GET_VERSION_EXTENDED") != "")

    def GetExperimentPath(self):
        arr = opusrequest(self.host, self.port, "GET_OPUSPATH")
        print(arr)
        if (arr[0] == 'OK'):
            return arr[1] + '\\XPM'
        return ''
 
    def get_x_values(self,path_leermessung, host, port):
        pfad_leermessung_spektrum = f'"{path_leermessung}":AB'
        file = (host, port, "LOAD_FILE %s" % str(path_leermessung))
        time.sleep(1)
        compatible = self.opusrequest(host, port, "COMMAND_LINE MakeCompatible ([%s], [%s], {});" % ( pfad_leermessung_spektrum, pfad_leermessung_spektrum))
        read2 = self.opusrequest(host, port, "READ_FROM_FILE %s;" % pfad_leermessung_spektrum)
        read3 = self.opusrequest(host, port, "READ_FROM_BLOCK AB")
        read4 = self.opusrequest(host, port, "READ_HEADER")
        read = self.opusrequest(host, port, "READ_DATA")

        data = np.array(read[1].splitlines()).astype("float64")
        print(data)
        nr_points, upperx, lowerx, data_processed = data[0], data[1], data[2], data[4:]
        delta_x = (upperx - lowerx)/(nr_points-1)
        x_points = list(reversed([lowerx + x*delta_x for x in range(int(nr_points))]))
        #x_points = list([lowerx + x*delta_x for x in range(int(nr_points))])
        


        with open(os.path.join(basedir, "spectra_csv", "x_points.txt"), 'w') as filehandle:
            for point in x_points:
                filehandle.write('%s\n' % point)

        # cwdir = os.getcwd()
        # with open('{}/spectra_csv/x_points.txt'.format(cwdir), 'w') as filehandle:
        #     for point in x_points:
        #         filehandle.write('%s\n' % point)

        unload = self.opusrequest(host, port, "UNLOAD_FILE %s" % str(path_leermessung))

        return x_points, len(x_points), lowerx, delta_x

    def load_preprocess_spectra(self, path_file, csvlist_raw, csvlist_pre, x_values, x_min, delta_x):
        path_leermessung = self.path_leermessung
        host = self.host
        port = self.port

        pfad_leermessung_spektrum = f'"{path_leermessung}":AB'

        #pfad_leermessung_spektrum = f'"{path_leermessung}":AB'

        filename_raw = f"out_raw_measurement.txt"
        filename_pre = f"out_pre_measurement.txt"
        product = 'test'

        reduced_path = path_file.strip('')
        normalized_spectrum_path = f'{reduced_path}/1.Der.'
        print(normalized_spectrum_path)

        compatible = self.opusrequest(host, port, "COMMAND_LINE MakeCompatible ([%s], [%s], {});" % (pfad_leermessung_spektrum, path_file))
        print("Compatible? {}".format(compatible[0]))
        time.sleep(1)
        read2 = self.opusrequest(host, port, "READ_FROM_FILE %s;" % path_file)
        read3 = self.opusrequest(host, port, "READ_FROM_BLOCK AB")
        read4 = self.opusrequest(host, port, "READ_HEADER")
        read = self.opusrequest(host, port, "READ_DATA")

        data = np.array(read[1].splitlines()).astype("float64")
        nr_points, upperx, lowerx, data_processed = data[0], data[1], data[2], data[4:]
        measurement_data_raw = [filename_raw, product, "classification", "original"]

        if len(data_processed) < len(x_values):
            pointsatbeginning = round(
                np.abs(lowerx-x_min) // delta_x)
            for i in range(pointsatbeginning):
                measurement_data_raw.append(np.nan)
            # pointsatend=nr_xpoints - len(data_processed) - pointsatbeginning

        for i in data_processed:
            measurement_data_raw.append(i)

        if len(data_processed) < len(x_values):
            diff = len(x_values) - len(measurement_data_raw)+4
            for i in range(diff):
                measurement_data_raw.append(np.nan)

        derivative2 = self.opusrequest(host, port, "COMMAND_LINE Derivative ([%s], {QSP=13, QOD=1});" % path_file)
        #time.sleep(5)
        normalization = self.opusrequest(host, port, "COMMAND_LINE  Normalize ([%s], {NME=2, NFX=4000.000000, NLX=400.000000, NWR=1});" % normalized_spectrum_path)
        #time.sleep(5)
        read2 = self.opusrequest(host, port, "READ_FROM_FILE %s;" % path_file)
        read3 = self.opusrequest(host, port, "READ_FROM_BLOCK AB/1.Der.")
        read4 = self.opusrequest(host, port, "READ_HEADER")
        read = self.opusrequest(host, port, "READ_DATA")

        data = np.array(read[1].splitlines()).astype("float64")
        nr_points, upperx, lowerx, data_processed = data[0], data[1], data[2], data[4:]
        measurement_data_dernorm = [filename_raw, product, "classification", "original"]

        if len(data_processed) < len(x_values):
            pointsatbeginning = round(
                np.abs(lowerx-x_min) // delta_x)
            for i in range(pointsatbeginning):
                measurement_data_dernorm.append(np.nan)
            # pointsatend=nr_xpoints - len(data_processed) - pointsatbeginning

        for i in data_processed:
            measurement_data_dernorm.append(i)

        if len(data_processed) < len(x_values):
            diff = len(x_values) - \
                len(measurement_data_dernorm)+4
            for i in range(diff):
                measurement_data_dernorm.append(np.nan)

        # file_raw = list(map(list, zip(x_values, measurement_data_raw[4:])))
        # file_pre = list(map(list, zip(x_values, measurement_data_dernorm[4:])))
        # save_to_txt(file_raw, path_product, filename_raw)
        # save_to_txt(file_pre, path_product, filename_pre)
        csvlist_pre.loc[len(csvlist_pre)] = measurement_data_dernorm
        csvlist_raw.loc[len(csvlist_raw)] = measurement_data_raw
        # unload = self.opusrequest(host, port, "UNLOAD_FILE %s" % str(path_file))
        unload = self.opusrequest(host, port, "UNLOAD_FILE %s" % str(path_leermessung))
        # unload = self.opusrequest(host, port, "UNLOAD_FILE %s" % str(normalized_spectrum_path))
        return csvlist_raw, csvlist_pre

    def obtain_filename(self):
        now = datetime.now()
        #dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
        dt_string = now.strftime("%Y%m%d__%H-%M-%S")
        productlabels = self.productlabel_array
        joined_productlabels = (' '.join(productlabels))
        joined_productlabels = '_'.join(joined_productlabels.split())
        print("Joined String: {}".format(joined_productlabels))
        filename = joined_productlabels + "_" + dt_string
        return filename
        
    def load_csvfile(self,x_values):
        """Loads a csv file if stated or else 
        creates a new one 

        Args:
            path_file (str): path to csv file with spectra
            x_values (df): x values of the leermessung

        Returns:
            data [dataframe]: initialized or loaded dataframe for spectra
        """
        columns = ["Filename", "Product", "Dataset", "Augmented"]
        columns = [columns.append(i) for i in x_values]
        data1 = pd.DataFrame(
            columns=["Filename", "Product", "Dataset", "Augmented"])
        data = data1.join(pd.DataFrame(columns=x_values))
        return data

    def __init__(self, productlabel_array):
        QThread.__init__(self)
        print("Thread created")
        self.productlabel_array = productlabel_array
        print("Productlabel Array: {}".format(productlabel_array))

    def run(self):
        XpmName = 'python.xpm'
        number_of_measurements = 3

        print("Start of measurement pipeline execution")

        # Check connection by getting the OPUS version
        if self.GetVersion() == False:
            print("Pipe connection failed")
            return
        
        # # Check if OPUS is connected to an instrument
        # if (self.CheckInstrumentStatus() == False): return

        # Read Opus Path from workspace
        xpm_path = self.GetExperimentPath()
        if (xpm_path == ''):
            print("Error on trying to evaluate the OPUS path")
            return
        else:
            print("\nMake sure you have a suitable experiment file defined in " + xpm_path)
            print("The experiment file must have the name" + XpmName + ".")

        # Obtain the x-values from the Leermessung
        x_values_leer, _, lowerx_leer, deltax_leer = self.get_x_values(self.path_leermessung, self.host, self.port)

        # Create CSV Files
        csvlist_pre = self.load_csvfile(x_values_leer)
        csvlist_raw = self.load_csvfile(x_values_leer)

        # answer= self.opusrequest("127.0.0.1", 80, "COMMAND_LINE LoadFile('/mnt/c/Users/G164.PHYTAX/Desktop/phydent/Leermessung.0', WARNING)")
        xpm_path = os.path.join(basedir, "XPM")
        #command = self.opusrequest("127.0.0.1", 80, "MeasureSample(0, {NSS=3, EXP='ATR_Di_Phydent.XPM', XPP='C:\\Users\\G164\\Desktop\\Phydent-App\\XPM')") 
        # command = self.opusrequest("127.0.0.1", 80, "MeasureSample(0, {NSS=3, EXP='ATR_Di_Phydent.XPM', XPP='C:\\Users\\G164\\Desktop\\Phydent-App\\XPM\\ATR_Di_Phydent.XPM')") 


        #CORRECT FORM BELOW
        command = self.opusrequest("127.0.0.1", 80, "MeasureSample(0, {NSS=%s, EXP='ATR_Di_Phydent.XPM', XPP='%s')" % (number_of_measurements, xpm_path))

        #print(command)
       
        #Obtain information about selected/just measured spectrum
        filenames= self.opusrequest("127.0.0.1", 80,"GET_SELECTED")

        #Extract absolute path to file
        file_path =  '{}'.format(filenames[1])
        print(f"The path to the selected spectra is {file_path}")
        path_file = file_path[:-6]
        print("Path file: {}".format(path_file))
        path_file = str(path_file[1:-1])

        #Save the file into the appropriate Phydent Folder
        #saving_path = "C:\\Users\\G164\\Desktop\\PathSpectra"

        #save =  self.opusrequest("127.0.0.1", 80, "SaveAs([%s], {OEX='1', SAN= 'spectrum', DAP='C:\\Users\\G164\\Desktop\\Phydent-App\\test'})" % file_path)
        #save = self.opusrequest("127.0.0.1", 80, "SaveAs(['C:\Users\G164\Desktop\Phydent-App\spectra_measurement\20220604-201043.0' 1 :AB], {SAN='test', DAP='C:\\Users\\G164\\Desktop\\'})")
        # print("Result from save: {}".format(save))
        #save = self.opusrequest("127.0.0.1", 80, "SaveAs([%s], {SAN=%s, DAP='%s'})" % (file_path, self.new_file_name, Path(self.target_path)))
        #save = self.opusrequest("127.0.0.1", 80, "SaveAs([%s], {SAN=%s, DAP='%s'})" % (file_path, self.new_file_name, saving_path))


        #save = self.opusrequest("127.0.0.1", 80, "SaveAs([%s], {SAN=%s, DAP='%s'})" % (file_path, self.new_file_name, saving_path))

        #Obtain filename
        spectra_save_filename = self.obtain_filename()
        print("Spectrum save filename: {}".format(spectra_save_filename))
        save = self.opusrequest("127.0.0.1", 80, "SaveAs([%s], {DAP = '%s', OEX = '1', SAN = %s.0, COF = 2, X64 = '1'})" % (file_path, self.spectra_save_path, spectra_save_filename))
        print("Result from save: {}".format(save))
        print("The spectrum file has been saved in the Path {}".format(Path(self.spectra_save_path)))

        spectra_raw, spectra_pre = self.load_preprocess_spectra(file_path,csvlist_raw, csvlist_pre, x_values_leer, lowerx_leer, deltax_leer)
        #spectra_raw, spectra_pre = self.load_preprocess_spectra(file_path,csvlist_raw, csvlist_pre, x_values_leer, lowerx_leer, deltax_leer)

        spectra_pre.to_csv(os.path.join(basedir, "spectra_csv", "spectra_pre.csv"), index = False)
        spectra_raw.to_csv(os.path.join(basedir, "spectra_csv", "spectra_raw.csv"), index = False)


        # ## ALTERNATIVE TO SaveAs Method from Opus is unloading, copying the file  and loading the file again
        # unload = self.opusrequest(self.host, self.port, "UNLOAD_FILE %s" % str(file_path))
        # copy2(path_file, self.path)
        # load = self.opusrequest(self.host, self.port, "LOAD_FILE %s" % str(path_file))

        # spectra_pre.to_csv('{}/spectra_csv/spectra_pre.csv'.format(cwdir), index=False)
        # spectra_raw.to_csv('{}/spectra_csv/spectra_raw.csv'.format(cwdir), index=False)

        self.progress.emit(1)
        #time.sleep(15)
        # spectra_pre.to_csv('{}/spectra_pre.csv'.format(self.target_path), index=False)
        # spectra_raw.to_csv('{}/spectra_raw.csv'.format(self.target_path), index=False)
  
        self.finished.emit()
        # spectra_pre.to_csv(self.target_path, index=False)
        # spectra_raw.to_csv(self.target_path, index=False)



        # """Perform Sample Measurement"""
        # command = self.opusrequest("127.0.0.1", 80, "MeasureSample(0, {EXP='ATR_Di.XPM', XPP='C:\\Users\\G164\\Desktop', NSS=1})")
        # filenames=self.opusrequest("127.0.0.1", 80,"GET_SELECTED")
        # #Extract absolute path to file
        # file_path =  '{}'.format(filenames[1])
        # #Save the file into the appropriate Phydent Folder
        # save = self.opusrequest("127.0.0.1", 80, "SaveAs([%s], {SAN=%s, DAP='%s'})" % (file_path, self.new_file_name, self.target_path))
        # #Unload the file from opus


        # unload = self.opusrequest("127.0.0.1", 80, "UNLOAD_FILE %s" % str(file_path))


    def opusrequest(self, IP,port,command):
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
                print(data)
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