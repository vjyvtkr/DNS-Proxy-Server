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

home_path = "C:\\Users\\u505123\\Documents\\Project\\Output\\full-index\\"
#print "Home path is",home_path

#Create the home path if it does not exist
if not os.path.exists(home_path):
    os.makedirs(home_path)

#Home directory of full-index of sec website
home = "ftp://ftp.sec.gov/edgar/full-index/"
valid_years = ['2011','2012','2013','2014','2015','2016']
valid_qtrs = ['1','2','3','4']
print "Please enter the following\n"

while True:
    ystart = raw_input("Start Year: ")
    yend = raw_input("End Year: ")

    if ystart in valid_years and yend in valid_years:
        break
    else:
        print "Please enter a Years between 2011 to 2016 (both inclusive)"

while True:
    qstart = raw_input("Start Quarter: ")
    qend = raw_input("End Quarter: ")
    if qstart in valid_qtrs and qend in valid_qtrs:
        break
    else:
        print "Please enter a Quarters between 1 and 4 (both inclusive)"

ix_start = valid_years.index(ystart)
ix_end = valid_years.index(yend)
if ix_start > ix_end:
    ystart, yend = yend, ystart
    ix_start, ix_end = ix_end, ix_start

df = []

#Navigate through the sec ftp tree.
for j in range(ix_start,ix_end+1):
    year = valid_years[j]
    cwd = home+year+"/"
    #print "\ncwd is",cwd
    if not os.path.exists(home_path+year):
        os.makedirs(home_path+year)
    qtr_range = 5
    if year=='2016':
        qtr_range=3
    sim_check = False

    #Check valid quarters and for each quarter
    if j==ix_start:
        qs = int(qstart)
        if qs>qtr_range:
            qs = qtr_range
        qe = qtr_range
        sim_check = True
    if j==ix_end:
        if not sim_check:
            qs = 1
        qe = int(qend)+1
        if qe>qtr_range:
            qe = qtr_range
    else:
        qs = 1
        qe = qtr_range

    for i in range(qs,qe):
        qtr = "QTR"+str(i)
        skip = False

        #First download the zip file and extract it. Inside will be an xbrl.idx file.
        direct = cwd+qtr+"/xbrl.zip"
        ccwd = home_path+year+"\\"+qtr
        inp_zip_file = ccwd+"\\xbrl.zip"

        if not os.path.exists(inp_zip_file):
            print "Downloading zip %s to %s\n"%(direct,ccwd)

            if not os.path.exists(ccwd):
                os.makedirs(ccwd)

            urllib.urlretrieve(direct,inp_zip_file)
            zip_r = zipfile.ZipFile((inp_zip_file),'r')
            zip_r.extractall(ccwd)

        else:
            print "Zip file exists, checking files."

        if not os.path.exists(ccwd):
            os.makedirs(ccwd)
        inp_file = ccwd+"\\xbrl.idx"
        out_file = ccwd+"\\xbrl.csv"

        #Call the ConvLinks method to formulate the absolute path of the files inside the xbrl.idx file. Store it in a dataframe, links.
        links = cv.ConvLinks(inp_file,out_file)

        count=0

        #Now for each file in the dataframe, each will be a zip file, extract the contents and you will get an xml file.
        for files,cik,cname,ftype in zip(links['Filename'],links['CIK'],links['Company Name'], links['Form Type']):
            #file text is, how you want to name the files inside.
            file_text = "d_"
            print "Details\n%s, %s" % (year,qtr)
            print files
            print cname

            count=count+1
            temp = files.split("/")
            fname = temp[len(temp)-1].replace(".zip","")
            fwd = ccwd+'\\xbrl_idx\\'+file_text+str(count)+"_"+str(fname)

            if not os.path.exists(fwd):
                os.makedirs(fwd)
            if os.path.exists(fwd+".zip"):
                print "File exists. Skipping."
                continue

            print "\nRetrieving...%s to directory %s.zip" % (files, fwd)
            urllib.urlretrieve(files,(fwd+".zip"))
            print "\nComplete!\n"
            zip_ref = zipfile.ZipFile((fwd+".zip"),'r')
            zip_ref.extractall(fwd)
            only_files = [f for f in os.listdir(fwd) if os.path.isfile(os.path.join(fwd, f))]

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
