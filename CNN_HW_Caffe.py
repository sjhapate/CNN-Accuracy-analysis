import os
import numpy as np
import csv
import pdb
import xlwt
import itertools
import xlsxwriter
import pandas as pd
import matplotlib.pyplot as plt
    
#to find rms value between hardware output results(HIL) and caffe deep learning framework    
def rms(hw,caffe):
    result.append(e)
    result.append(f)
    result.append(np.sqrt(((hw-caffe)**2).mean()))
    result.append(np.std(hw-caffe))
    result.append(np.mean(abs(hw-caffe)))
    result.append(np.min(hw))
    result.append(np.max(hw))  
    result.append(np.min(caffe))
    result.append(np.max(caffe))  
    result.append(abs(np.max(hw)-np.max(caffe)))
    print (abs(np.max(hw)-np.max(caffe)))

# to store output results in excel sheet        
def save_xcl():
    col = 0
    header_filename = hw_file + '-' + caffe_file
    worksheet.write(row, col,str(header_filename))
    rsl = rms(hw,caffe)
    for res in result:
        worksheet.write(row, col+1,res)
        col = col + 1
    del result[:]

# to store all layer's channels output 
def each_ch():   
    #w = 0
    for y in range(e):
        rms_each = np.sqrt(((hw[0][y]-caffe[0][y])**2).mean())
        mean_each=(np.mean(abs(hw[0][y]-caffe[0][y])))
        rms_min_max.append(rms_each)
        mean_for_each.append(mean_each)
        y += 1
    sheet1.write(0, col_each,hw_file,style)
    i=0
    for n in rms_min_max:
        #print n
        i = i+1
        sheet1.write(i,col_each, n)
    sheet2.write(0, col_each,hw_file,style)
    j=0
    for g in mean_for_each:
        #print n
        j = j+1
        sheet2.write(j,col_each, g)

        
each_cha_need= []
mean_for_each=[]
rms_min_max = []
result = []
firstfile = []
file_name = []
newlist = []
index = 0
frac_po = [12,10,10,10] #fraction positions of CNN network 


hw_npy= "/media/sf_SVN/bias_add/new_xml_12_10_10_10/with_bias/new_out_image0_16bit/output_sim/4/hw_npy"
caffe_npy = '/media/sf_SVN/bias_add/caffe_result_studpid_8channels/caffe_numpy/' # caffe output results of all layer in numpy format

rms_std_mean='/media/sf_SVN/inkalll/exel_png out _from_script/RMS.xlsx'
rms_value_each_layer=  '/media/sf_SVN/inkalll/exel_png out _from_script/test.xlsx'
combi_each_rms_max_min= '/media/sf_SVN/inkalll/exel_png out _from_script/each_ch.xlsx'
each_layer_csv= "/media/sf_SVN/bias_add/new_xml_12_10_10_10/with_bias/new_out_image0_16bit/output_sim/4/csv" # SIL or HIL output results for all layer as a inputs

folder_csv = os.listdir (each_layer_csv)
cwd = os.getcwd()
print "folder_csv ________________",folder_csv
for filename in folder_csv:
    newlist = []
    del file_name [:]
    del firstfile [:]
    print "filename _____________________",filename
    check_dir_or_file = each_layer_csv + '/' + filename 
    print "check_dir_or_file __________________",check_dir_or_file
    if os.path.isdir(check_dir_or_file):
        all_file_list = os.listdir(check_dir_or_file)
        for file1 in all_file_list:
            h = check_dir_or_file + '/' + file1
            file_name.append(h)  
        file_name.sort(key=lambda f: int(filter(str.isdigit, f)))
        for fFile in file_name:
            #print (len(file_name))
            file2 = open(fFile,'r')
            #this is to ignore first line
            file2.readline()
            for row in file2:
                #tmp- to make array of array
                tmp = []
                col = str(row).split(",")
                #Add this line to remove last element
                for val in col:
                    newval = val.strip()
                    if (newval != "" and newval != ","):
                        tmp.append(int(val,0))
                        #print tmp
        
                firstfile.append(tmp)
        
        npArr =np.asarray(firstfile).astype("float32")
        npArr =npArr.astype(np.float)
        #print npArr
        flt = npArr/2**frac_po[index]
        #print flt
        print frac_po[index]
        newlist.append(flt)
        
        index += 1
    # to reshape list
    newlist = np.asarray(newlist).reshape(1,len(file_name),len(firstfile[0]),len(firstfile[0]))
    # to create npy files from eacy layer 
    
    for t in range(len(folder_csv)):
        if not os.path.exists(hw_npy):
            os.makedirs(hw_npy)
        layer_file = os.path.join(hw_npy ,filename)
        np.save(layer_file, newlist)
for p in each_cha_need:
    print p
#to save RMS,Mean and STS values in exel sheet      
workbook = xlsxwriter.Workbook(rms_std_mean)
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})

header = ['Layer-Caffe-Hw','I/P channels','Frac_po','Root mean square(hw-caffe)','Standard deviation(hw-caffe)','MEAN(hw-caffe)','HW_MIN','HW_MAX','CAFFE_MIN','CAFFE_MAX','Max vlaue diff (hw-caffe)']
row = 0
col = 0
for item in header:
    worksheet.write(row, col,item,bold)
    col = col + 1
    
# Initialize a workboo1      
book1 = xlwt.Workbook()
#style0 = xlwt.easyxf('font: name Times New Roman, color-index blue, bold on',height 280;')
style = xlwt.easyxf('font: bold 1,height 200;')
exel_filename = rms_value_each_layer
# Add a sheet to the workbook 
sheet1 = book1.add_sheet("each_channels")
sheet2 = book1.add_sheet("each_Mean")


hw_npy_filenames = os.listdir(hw_npy)
caffe_npy_filenames = os.listdir(caffe_npy)

frac = 0
for hw_file in hw_npy_filenames:
    hw = np.load(hw_npy + '/' + hw_file)
    row = row + 1
    frac = frac + 0
    for caffe_file in caffe_npy_filenames:
        caffe = np.load(caffe_npy + caffe_file)
        if(hw_file == "conv1.npy" and caffe_file == "pool1.npy"):
            del rms_min_max[:]
            del mean_for_each[:]
            f = frac_po[frac]
            e = 8
            col_each = 0
            save_xcl()
            #hist_plot(hw_npy + '/' + hw_file,e,hw_file)
            each_ch()
            frac += 1

        elif(hw_file == "conv2.npy" and caffe_file == "pool2.npy"):
            del rms_min_max[:]
            del mean_for_each[:]
            f = frac_po[frac]
            e = 8
            col_each = 1
            save_xcl()
            #hist_plot(hw_npy + '/' + hw_file,e,hw_file)
            each_ch()
            frac += 1

        elif(hw_file == "conv3.npy" and caffe_file == "conv3.npy"):
            del rms_min_max[:]
            del mean_for_each[:]
            f = frac_po[frac]
            e = 8
            col_each = 2
            save_xcl()
            each_ch()
           #hist_plot(hw_npy + '/' + hw_file,e,hw_file)
            frac += 1

        elif(hw_file == "conv4.npy" and caffe_file == "conv4.npy"):
            del rms_min_max[:]
            del mean_for_each[:]
            e = 10
            f = frac_po[frac]
            col_each = 3
            save_xcl()
            each_ch()
           # hist_plot(hw_npy + '/' + hw_file,e,hw_file)
            frac += 1
book1.save(exel_filename)

workbook.close()



