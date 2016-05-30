# -*- coding: utf-8 -*-
"""
Created on Wed May 25 16:46:48 2016

@author: Vijay Yevatkar
"""

'''
Function to Download all the forms, of the years specified.
Input = List of Years.
Output = Creates a full-index of the files downloaded and stores the information in a csv file.
         For every 300 files/companies in the xbrl.idx file, the information is stored in a single csv file.
'''

import os
import sys
import urllib
import ConvertLinks as cv
import Parse10K as pk
import zipfile

#inp_test_file = 'C:\\Users\\u505123\\Documents\\Project\\Dataset\\2015_Q2_xbrl.idx'
#out_test_file = 'C:\\Users\\u505123\\Documents\\Project\\Output\\2015_Q2_xbrl.csv'

home_path = "C:\\Users\\u505123\\Documents\\Project\\Output\\full-index\\"
#print "Home path is",home_path

#Create the home path if it does not exist
if not os.path.exists(home_path):
    os.makedirs(home_path)

#Home directory of full-index of sec website
home = "ftp://ftp.sec.gov/edgar/full-index/"
years = ['2011']#,'2012','2013','2014','2015']
#all_links = [[]]
#all_files = [[]]
df = []

#Navigate through the sec ftp tree.
for year in years:
    cwd = home+year+"/"
    #print "\ncwd is",cwd
    if not os.path.exists(home_path+year):
        os.makedirs(home_path+year)
    qtr_range = 5
    if year=='2016':
        qtr_range=3
    #For each quarter
    for i in range(1,3):
        qtr = "QTR"+str(i)

        #First download the zip file and extract it. Inside will be an xbrl.idx file.
        #direct = cwd+qtr+"/xbrl.zip"
        ccwd = home_path+year+"\\"+qtr
        inp_zip_file = ccwd+"\\xbrl.zip"
        #urllib.urlretrieve(direct,inp_zip_file)
        zip_r = zipfile.ZipFile((inp_zip_file),'r')
        zip_r.extractall(ccwd)
        #print "\nccwd is",ccwd
        #print "\nurl is",direct
        if not os.path.exists(ccwd):
            os.makedirs(ccwd)
        inp_file = ccwd+"\\xbrl\\xbrl.idx"
        out_file = ccwd+"\\xbrl\\xbrl.csv"
        #print "\ninp file and output file"
        #print inp_file
        #print out_file

        #Call the ConvLinks method to formulate the absolute path of the files inside the xbrl.idx file. Store it in a dataframe, links.
        links = cv.ConvLinks(inp_file,out_file)
        #all_links.append(links)

        #file text is, how you want to name the files inside.
        count=0

        #Now for each file in the dataframe, each will be a zip file, extract the contents and you will get an xml file.
        for files,cik,cname,ftype in zip(links['Filename'],links['CIK'],links['Company Name'], links['Form Type']):
            file_text = "d_"
            print "Details\n%s, %s" % (year,qtr)
            print files
            print cname
            count=count+1
            temp = files.split("/")
            fname = temp[len(temp)-1].replace(".zip","")
            fwd = ccwd+'\\xbrl_idx\\'+file_text+str(count)+"_"+str(fname)
            #print "\nfwd is",fwd
            if not os.path.exists(fwd):
                os.makedirs(fwd)
            #urllib.urlretrieve(files,(fwd+".zip"))
            zip_ref = zipfile.ZipFile((fwd+".zip"),'r')
            zip_ref.extractall(fwd)
            only_files = [f for f in os.listdir(fwd) if os.path.isfile(os.path.join(fwd, f))]
            #all_files.append(only_files)
            min_len = sys.maxint
            file_to_parse = only_files[0]
            for temp_file in only_files:
                if temp_file.endswith('.xml') and len(temp_file)<min_len:
                    file_to_parse = temp_file
                    min_len=len(temp_file)
            print "Parsing: ",file_to_parse

            #Once you get the xml file, we need to parse it to the parser. The parser returns a dataframe and also creates the csv.
            #300 companies go into a single csv.
            if not count%300 or count==1:
                range_is = ((count/300)+1)*300
                csv_path = ccwd+'\\xbrl_idx\\'+str(range_is-299)+"_"+str(range_is)+".csv"
            tdf = pk.ExtractID(fwd+"\\"+file_to_parse, csv_path,cik,cname,ftype)
            df.append(tdf)
