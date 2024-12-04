#!/usr/bin/env python
# coding: utf-8


######################
# import pacakge
######################
import pandas as pd
from datetime import datetime


##########################
#folder definition
##########################


def read_line(line, param_dict=None):
    line_s = line.split(' ')
    dateascii = line_s[0][1:-2]
    date = datetime.strptime(dateascii,'%Y-%m-%dT%H:%M:%S')
    measurement_name = line_s[1][1:-1]
    channel = int(line_s[5][1:-1])
    param = line_s[7][1:-1]
    param_val = line_s[9][1:-2]
    if (param == "Pw" or param == 'ImonRange'):
        if param_val == 'true':
            param_val = 1
        else:
            param_val = 0
    else:
        param_val = float(param_val)
    return [date, channel, param, param_val]


now = datetime.now()
def get_HV_df(filename):
    param_dict_0 = {"date":[now], "channel":[2],"IMon":[0], "VMon":[0],"Pw":[0],"ChStatus":[0],"IMonRange":[0]}
    param_dict_2 = {"date":[now], "channel":[3],"IMon":[0], "VMon":[0],"Pw":[0],"ChStatus":[0],"IMonRange":[0]}
    with open(filename, 'r') as f:
            lines = f.readlines()
            df = pd.DataFrame()
            for l in lines:
                [date, channel, param, param_val] = read_line(l)
                if date == 0:
                    print(date)
                if channel == 2:
                    for p in param_dict_0:
                        if p == param:
                            param_dict_0[p].append(param_val)
                            param_dict_2[p].append(param_dict_2[p][-1])
                        elif p == 'date':
                            param_dict_0["date"].append(date)
                            param_dict_2["date"].append(date)
                        elif p == 'channel':
                            param_dict_0["channel"].append(2)
                            param_dict_2["channel"].append(3)
                        else:
                           param_dict_0[p].append(param_dict_0[p][-1])
                           param_dict_2[p].append(param_dict_2[p][-1])
                elif channel == 3:
                    for p in param_dict_2:
                        if p == param:
                            param_dict_2[p].append(param_val)
                            param_dict_0[p].append(param_dict_0[p][-1])
                        elif p == 'date':
                            param_dict_0["date"].append(date)
                            param_dict_2["date"].append(date)
                        elif p == 'channel':
                            param_dict_0["channel"].append(2)
                            param_dict_2["channel"].append(3)
                        else:
                            param_dict_0[p].append(param_dict_0[p][-1])
                            param_dict_2[p].append(param_dict_2[p][-1])
                    
            print(param_dict_0)
            print(param_dict_2)
                
    df_0 = pd.DataFrame.from_dict(param_dict_0)
    df_2 = pd.DataFrame.from_dict(param_dict_2)
    df = df_0
    df= pd.concat([df,df_2], ignore_index=True)
    return df


def filter_date(df,d1,d2):
    mask = (df['date'] > d1) & (df['date'] <=d2)
    df_f = df.loc[mask]
    return df_f
    




