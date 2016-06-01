# -*- coding: utf-8 -*-
"""
Created on Wed Jun 01 14:23:16 2016

@author: Vijay Yevatkar
"""

import pandas as pd
import re
import Parse10K as pk


df = pk.ExtractID('C:\\Users\\u505123\\Documents\\Project\\Dataset\\hrl-20151025.xml', 'C:\\Users\\u505123\\Documents\\Project\\Output\\hormel.csv', '1234', 'HORMEL FOOD CORPS', '10K')

text = []
for i in df['fact']:
    text.append(i)

sales = []
revenue = []

for i in text:
    if 'sales' in i:
        sales.append(i.replace('&nbsp;',' '))
    elif 'revenue' in i:
        revenue.append(i.replace('&nbsp;',' '))

s_dict = {}
r_dict = {}
for i in sales:
    s_dict[i] = (i.find('sales'))
for i in revenue:
    r_dict[i] = (i.find('revenue'))
