# -*- coding: utf-8 -*-
"""
Created on Thu May 26 16:25:20 2016
@author: Vijay Yevatkar
"""

'''
Function to extract the follwing information from a given xbrl.idx file.
['Filename','CIK','Company Name','Form Type']
Input = xbrl.idx File to be parsed.
Output = Returns a DataFrame with the above information
Parameters = Input File Path and Output File Path (both absolute)
'''

import pandas as pd

def ConvLinks(inp_file,out_file):
    inp = open(inp_file,"r")
    parse_file = open(out_file,"w+")

    #Remove the junk from the idx file
    for line in inp:
        if "|" in line:
            parse_file.write(line)
    inp.close()
    parse_file.close()

    #As the delimiter is "|", directly read it into the Dataframe
    df = pd.read_csv(out_file,"|")
    l = df['Filename']
    prefix = "ftp://ftp.sec.gov/"
    links = []

    #So the idea is the append the above preix to the 'Filename' column.
    #Also, need to remove all the "-" from the filename, but keep the original name, then append at last.
    #This will give us the path of the zip file to download
    for i in l:
        y = (str(i).split(".")[0])
        j = len(y)-1
        last = ''
        while True:
            if(y[j]=="/"):
                last = y[(j+1):(len(y))]
                break
            j=j-1
        x = (y.replace("-","")).split("/")
        links.append(prefix+y[0:j+1]+x[len(x)-1]+"/"+last+"-xbrl.zip")

    #The modified names are stored in a list and then added to the dataframe properly. Return the Dataframe
    final_links = pd.DataFrame(links)
    final_links.columns = ['Filename']
    df['Filename'] = final_links['Filename']

    return df
