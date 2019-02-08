import os
import numpy as np
import csv
import pdb
import xlwt
import itertools

def rms(hw,caffe):
    print('rms', np.sqrt(((hw-caffe)**2).mean()))
    print('mean', np.mean(abs(hw-caffe)))
    print('std:', np.std(hw-caffe))

firstfile = []
file_name = []
newlist = []
index = 0
frac_po = [12,12,8,8]
hw_npy_save_path = '/media/sf_SVN/inkalll/npy_ink/'   
caffe_npy_path = '/media/sf_SVN/inkalll/caffe_npy/'
filenames = os.listdir ("/media/sf_SVN/inkalll/exmple")
cwd = os.getcwd()
print "filenames ________________",filenames
for filename in filenames:
    newlist = []
    del file_name [:]
    del firstfile [:]
    print "filename _____________________",filename
    check_dir_or_file = '/media/sf_SVN/inkalll/exmple' + '/' + filename 
    print "check_dir_or_file __________________",check_dir_or_file
    if os.path.isdir(check_dir_or_file):
        all_file_list = os.listdir(check_dir_or_file)
        #print "all_file_list ____________",all_file_list
        for file1 in all_file_list:
            h = check_dir_or_file + '/' + file1
            file_name.append(h)
            #print h
#		for fFile in os.listdir( check_dir_or_file):
#			file_name.append(fFile)
        file_name.sort(key=lambda f: int(filter(str.isdigit, f)))
        for fFile in file_name:

            file2 = open(fFile,'r')
            #this is to ignore first line
            file2.readline()
            for row in file2:
                #tmp- to make array of array
                tmp = []
                col = str(row).split(",")
                #Add this line to remove last element
                for val in col:
                    #print val
                    newval = val.strip()
                    if (newval != "" and newval != ","):
                        tmp.append(int(val,0))
                        #print(int(val,0))
        
                firstfile.append(tmp)

        npArr =np.asarray(firstfile).astype("float32")
        npArr =npArr.astype(np.float)
        flt = npArr/2**frac_po[index]
        print frac_po[index]
        newlist.append(flt)
        index += 1
   
    newlist = np.asarray(newlist).reshape(1,len(file_name),len(firstfile[0]),len(firstfile[0]))

    for t in range(len(filenames)):
        #destPath = npy_save_path
        if not os.path.exists(hw_npy_save_path):
            os.makedirs(hw_npy_save_path)
        layer_file = os.path.join(hw_npy_save_path,filename)
        np.save(layer_file, newlist)
               
hw_npy_filenames = os.listdir(hw_npy_save_path)
caffe_npy_filenames = os.listdir(caffe_npy_path)

for hw_file in hw_npy_filenames:
    hw = np.load(hw_npy_save_path + hw_file)
    #print ('hw:',hw_file)
    for caffe_file in caffe_npy_filenames:
        caffe = np.load(caffe_npy_path + caffe_file)
        #print ('caffe:',caffe_file)
        if(hw_file == "conv1.npy" and caffe_file == "pool1.npy"):
            print hw_file
            print caffe_file
            rms(hw,caffe)
        elif(hw_file == "conv2.npy" and caffe_file == "pool2.npy"):
            print hw_file
            print caffe_file
            rms(hw,caffe)
        elif(hw_file == "conv3.npy" and caffe_file == "conv3.npy"):
            print hw_file
            print caffe_file
            rms(hw,caffe)
        elif(hw_file == "conv4.npy" and caffe_file == "conv4.npy"):
            print hw_file
            print caffe_file
            rms(hw,caffe)
    