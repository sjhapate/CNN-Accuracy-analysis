import re
import numpy as np
import os
import csv
import pdb
import xlwt

def csv2npy_file(csvFile, frac_pos):
    firstfile=[]
    #print Fpath
    file1 = open( csvFile, 'r' )
    # this is to ignore first line
    file1.readline()
    for row in file1:
        # tmp- to make array of array
        tmp = []
        col = str( row ).split( "," )
        # Add this line to remove last element
        # col = col[:-1]

        for val in col:
            newval = val.strip()
            if (newval != ""):
                if len(newval)==6:
                    uint_newval = int(newval,16)
                    int_newval = -(uint_newval & 0x8000) | (uint_newval & 0x7fff)
                elif len(newval)==4:
                    uint_newval = int(newval,8)
                    int_newval = -(uint_newval & 0x80) | (uint_newval & 0x7f)
                else:
                    print(csvfile + ": unknown hex format detected in CSV file ")
                tmp.append( int_newval )
                #print(int(val,0))
        firstfile.append( tmp )
    # convert array of array(list of list) to numpy array
    npArr = np.array( firstfile )
    npArr = npArr/2**frac_pos
    return npArr

def csv2npy_folder(pathCSV, frac_pos, key_word=None):
    file_name=[]
    for fFile in os.listdir( pathCSV ):
        if len(fFile.split("."))==2:
            if fFile.split( "." )[1] == "csv" and (key_word in fFile.split(".")[0]):
                file_name.append( fFile )
            #print(fFile)
    file_name.sort( key=lambda f: int(re.findall(r'ch(\d+)', f)[0]) )
    npy_folder=[]
    for csvfile in file_name:
        filecsv = os.path.join(pathCSV,csvfile)
        npy_file = csv2npy_file(filecsv,frac_pos)
        npy_file=npy_file.reshape(1,1,npy_file.shape[0],npy_file.shape[1])
        if npy_folder==[]:
            npy_folder=npy_file
        else:
            npy_folder = np.concatenate((npy_folder, npy_file), axis=1)
    return npy_folder
    
pathcsv="/media/sf_SVN/rms/hw/0"
frac_pos = 12
key_word = "conv1_rp"
npy_folder = csv2npy_folder(pathcsv, frac_pos, key_word)
print(npy_folder)