# -*- coding: utf-8 -*-
"""
Created on Tue May 24 12:36:13 2016

@author: Vijay Yevatkar
"""
import pandas as pd
from bs4 import BeautifulSoup
import os

'''
Function to extract the follwing information from a given 10K Form.
['elementId','contextId','unitId','fact','decimals','scale','sign','factId','ns','cik','companyName','formType']
Input = XML File to be parsed.
Output = Returns a DataFrame and also writes it to a csv file to the given path.
Parameters = Input File Path and Output File Path (both absolute)
'''

def ExtractID(inpName, outpName, cik, cname, form_type):

    #check if file exists
    try:
        f = open(inpName)
        f.close()
    except IOError:
        print

    #beautifulsoup object
    inp = BeautifulSoup(open(inpName))

    #columns that need to be extracted (3 more will be added later)
    columns = ['elementId','contextId','unitId','fact','decimals','scale','sign','factId','ns']
    #Empty DataFrame. We will return this finally.
    df = pd.DataFrame([],columns=columns)

    #Elements that need to be extracted are those which are specified in the xmlns values.
    ns = inp.xbrl.attrs

    #corresponding id's
    check ='contextref'
    un = 'unitref'
    dec = 'decimals'
    ns_val = ''
    #iterate over each tag in the file
    for i in inp.find_all():
        rows = []

        #Check the name of the tag.
        ns_check = i.name.split(":")[0]

        #If the name exists in the list, we need to parse it else continue.
        if check in i.attrs:

            #name is the elementid
            rows.append(i.name)

            #contextid is "contextref"
            rows.append(i[check])

            #un is the unitref corresponding to the unitid
            if un in i.attrs:
                rows.append(i[un])
            else:
                rows.append('')

            #text corresponds to the fact. Ignoring all the whitespace characters inside the tag.
            act_text = i.text.encode("utf-8")
            #"".join((act_text).split())
            rows.append(str(act_text))

            #dec is the decimals attribute
            if dec in i.attrs:
                rows.append(i[dec])
            else:
                rows.append('')

            #empty for now, need to be replaced by the corresponding scale, sign, factId, etc.
            rows.append("")
            rows.append("")
            rows.append("")

            #ns_val, as the name suggests, is the ns attribute
            for k in ns.keys():
                if ns_check in k:
                    ns_val = ns[k]
                    break

            rows.append(ns_val)

            #These values are appended to the dataframe created earlier.
            f_rows = [rows]
            df2 = pd.DataFrame(f_rows,columns=columns)
            frames = [df,df2]
            x = pd.concat(frames)
            df = x

    #Indices are made proper.
    indices = pd.DataFrame(range(0,df['elementId'].count()),columns=['index'])
    df = df.set_index(indices['index'])

    #Append the company name, form type and cik
    df['cik'] = cik
    df['companyName'] = cname
    df['formType'] = form_type

    #Output the created DataFrame to csv and return the DataFrame
    if not os.path.exists(outpName):
        df.to_csv(outpName,"|")
    else:
        with open(outpName, 'a') as f:
            df.to_csv(f, sep="|", header=False)
    return df
