#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 09:58:11 2024

@author: caio
"""

# Set of functions for csv reading and analysis

from datetime import datetime
import os
from datetime import timedelta
import shutil
import pandas as pd
import numpy as np
import csv
import zipfile
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# function to convert timestamp to time
def timestampTotime(df):
    timestamps = df['timestamp']
    folder = []
    folder_full = []
    for stamp in timestamps:
        time = datetime.fromtimestamp(stamp)
        #strtime = time.strftime('%H:%M:%S')
        strtime = time.strftime('%y/%m/%d-%H:%M:%S')
        strtimee = datetime.strptime(strtime, '%y/%m/%d-%H:%M:%S')
        folder.append(strtime)
        folder_full.append(strtimee)
    return folder, folder_full

# function to calculate the average of the baseline from the data that starts at t_start and ends at t_stop
def baseline_correction_val(df, t_start, t_stop):
    try:
        idx_start = df[df.timestamp == t_start].index[0]
    except IndexError:
        delta = timedelta(seconds=1)
        date = datetime.strptime(t_start, '%y/%m/%d-%H:%M:%S')
        #print(date)
        new_date = date + delta
        new_t_start = new_date.strftime('%y/%m/%d-%H:%M:%S')
        #print(new_t_start)
        try:
            idx_start = df[df.timestamp == new_t_start].index[0]
        except IndexError:
            delta = timedelta(seconds=1)
            date2 = datetime.strptime(new_t_start, '%y/%m/%d-%H:%M:%S')
            new_date2 = date2 + delta
            new_t_start2 = new_date2.strftime('%y/%m/%d-%H:%M:%S')
            #print(new_t_start2)
            idx_start = df[df.timestamp == new_t_start2].index[0]
    #print(idx_start)
    try:
        idx_stop = df[df.timestamp == t_stop].index[0]
    except IndexError:
        delta = timedelta(seconds=1)
        date = datetime.strptime(t_stop, '%y/%m/%d-%H:%M:%S')
        #print(date)
        new_date = date + delta
        new_t_stop = new_date.strftime('%y/%m/%d-%H:%M:%S')
        #print(new_t_stop)
        try:
            idx_stop = df[df.timestamp == new_t_stop].index[0]
        except IndexError:
            delta = timedelta(seconds=1)
            date = datetime.strptime(new_t_stop, '%y/%m/%d-%H:%M:%S')
            new_date = date + delta
            new_t_stop = new_date.strftime('%y/%m/%d-%H:%M:%S')
            #print(new_t_stop2)
            idx_stop = df[df.timestamp == new_t_stop].index[0]
    #print(df_ch2_corr.iloc[idx_start-1:idx_stop]['current'])
    charge = sum(df.loc[idx_start-1:idx_stop]['IMON'])
    mean_current = charge/len(df['timestamp'].loc[idx_start-1:idx_stop])
    return mean_current

# corrected current
def baselineShift(df, start, end):
    mean_current = baseline_correction_val(df,start,end)
    df.iloc[:, 1] -= mean_current
    return mean_current

# separate caen1 and caen2 files
def sep_caen1_caen2(directory):
    path_list_1 = []
    path_list_2 = []
    delta = timedelta(days = 1)
    today = datetime.today()

    try:
        # List all files in the specified directory
        files = os.listdir(directory)
        #print(files)

        # Check each file name
        for file in files:
            today_str = today.strftime('%Y-%m-%d')
            if "tem" in file:
                continue
            if "~" in file:
                continue
            if "save" in file:
                continue
            if "caen1" in file:
                path_list_1.append(os.path.abspath(directory + file))
            if "caen2" in file:
                path_list_2.append(os.path.abspath(directory + file))

    except FileNotFoundError:
        print(f"The directory {directory} was not found.")
        return False
    except PermissionError:
        print(f"Permission denied to access the directory {directory}.")
        return False

    return path_list_1, path_list_2

# integration of the current
def total_charge(df, t_start, t_end):
    current = df.IMON
    delta_t = 2
    voltage = df.VMON
    charge = 0
    time = df['timestamp']
    caen = df.caen
    channel = df.ch
    RUP = df.RAMPINGUP
    RDW = df.RAMPINGDOWN
    VSET = df.VSET
    ISET = df.ISET
    #print(voltage)
    data = {'timestamp': time,'IMON': current, 'VMON': voltage, 'VSET':VSET, 'ISET':ISET, 'caen':caen, 'ch':channel, 'RUP':RUP, 'RDW':RDW,}
    new_df = pd.DataFrame(data)
    new_df
    #print(new_df.iloc[0:,1])
    mean_current = baselineShift(new_df, t_start, t_end)
    print(f'current used to baseline correction is {mean_current}')
    return charge, mean_current, new_df

# import data from remote PC
def import_data_from_storage(FEA_test_dir, FEA_data, cols, OS):
    df_caen1 = []
    df_caen2 = []
    df_ctc = []
    scope_files = []
    #FEA_test = '240827_4FEA_vac_test'
    if OS == 'linux':
        if FEA_test_dir == FEA_data:
            os.system(f"scp -r caio@xegpu:/mnt/xedisk02/FEA/{FEA_test_dir} /home/caio/data/")
        else:
            os.system(f"scp -r caio@xegpu:/mnt/xedisk02/FEA/{FEA_test_dir}/{FEA_data} /home/caio/data/")
        logfolder = f'/home/caio/data/{FEA_data}/'
    elif OS == 'windows':
        if FEA_test_dir == FEA_data:
            os.system(f"scp -r caio@xegpu:/mnt/xedisk02/FEA/{FEA_test_dir} D:/data/{FEA_test_dir}")
        else:
            os.system(f"scp -r caio@xegpu:/mnt/xedisk02/FEA/{FEA_test_dir}/{FEA_data} D:/data/{FEA_test_dir}")
        logfolder = f'D:/data/{FEA_test_dir}/'
    logfiles = os.listdir(logfolder)
    for folder in logfiles:
        if "datalogs" in folder:
            with zipfile.ZipFile(logfolder + folder) as zf:
                txt_files = zf.namelist()
                txt_files.sort()
                for filename in txt_files:
                    if "tem" in filename:
                        continue
                    if "~" in filename:
                        continue
                    if "save" in filename:
                        continue
                    if "caen1" in filename:
                        with zf.open(filename) as file:
                            df = pd.read_csv(file, sep=',', usecols=cols) # this depends highly in the data we are dealing with
                            #print(len(df[cols[0]]))
                            time, date = timestampTotime(df)
                            df['timestamp'] = time
                            caen = [1 for i in range(len(df[cols[0]]))]
                            #new_column_names = df.iloc[1] 
                            #df.columns = new_column_names 
                            df['caen'] = caen
                            df_caen1.append(df)
                    if "caen2" in filename:
                        with zf.open(filename) as file:
                            df = pd.read_csv(file, sep=',', usecols=cols) # this depends highly in the data we are dealing with
                            caen = [2 for i in range(len(df[cols[0]]))]
                            time, date = timestampTotime(df)
                            df['timestamp'] = time
                            #new_column_names = df.iloc[1] 
                            #df.columns = new_column_names 
                            df['caen'] = caen
                            df_caen2.append(df)
                    if "ctc100" in filename:
                        with zf.open(filename) as file:
                            df = pd.read_csv(file, sep=',')
                            time, date = timestampTotime(df)
                            df['timestamp'] = time
                            df_ctc.append(df)
        #elif "datascope" in folder:
        #    with zipfile.ZipFile(logfolder + folder) as zf:
        #        folder_scope = zf.namelist()
        #        print(folder_scope)
        #        for scopefolder in folder_scope:
        #            scope_filenames = zf.namelist()
        #            for filename in scope_filenames:
        #                if 'csv' in filename:
        #                    with zf.open(filename) as file:
        #                        df = pd.read_csv(file, sep=',')
        #                        scope_files.append(df)
        #os.system(f'rm -r /home/caio/data/{FEA_test}')
    if OS == 'linux':
        os.system(f"rm -r /home/caio/data/{FEA_data}")
    return df_caen1, df_caen2, df_ctc#, scope_files

# import caen files and separate each channel data in different data frames
def import_caen_data(FEA_test_dir, FEA_data, cols, OS):
    df1, df2, df3 = import_data_from_storage(FEA_test_dir, FEA_data, cols, OS)
    

    # concat files
    df_caen1 = pd.concat(df1, ignore_index=True)
    df_caen2 = pd.concat(df2, ignore_index=True)
    df_ctc = pd.concat(df3, ignore_index=True)

    #df_caen1.sort()
    #df_caen2.sort()

    # caen1 df per channel
    df_caen1HV0 = df_caen1.loc[df_caen1["ch"] == 0]
    df_caen1HV1 = df_caen1.loc[df_caen1['ch'] == 1]
    df_caen1HV2 = df_caen1.loc[df_caen1["ch"] == 2]
    df_caen1HV3 = df_caen1.loc[df_caen1['ch'] == 3]

    # caen2 df per channel
    df_caen2HV0 = df_caen2.loc[df_caen2["ch"] == 0]
    df_caen2HV1 = df_caen2.loc[df_caen2['ch'] == 1]
    df_caen2HV2 = df_caen2.loc[df_caen2["ch"] == 2]
    df_caen2HV3 = df_caen2.loc[df_caen2['ch'] == 3]

    all_df_caen1 = [df_caen1HV0, df_caen1HV1, df_caen1HV2, df_caen1HV3]
    all_df_caen2 = [df_caen2HV0, df_caen2HV1, df_caen2HV2, df_caen2HV3]

    return all_df_caen1, all_df_caen2, df_ctc#, scope_files

# integration of only one period of time
def partial_charge(df, t_start, t_end, t_start_b, t_end_b):
    current = df.IMON
    delta_t = 2
    voltage = df.VMON
    charge = 0
    caen = df['caen'].iloc[0]
    channel = df['ch'].iloc[0]
    try:
        time_start = df[df['timestamp'] == t_start].index[0]
        new_t_start = t_start
    except IndexError:
            delta = timedelta(seconds=1)
            date = datetime.strptime(t_start, '%y/%m/%d-%H:%M:%S')
            new_date = date + delta
            new_t_start = new_date.strftime('%y/%m/%d-%H:%M:%S')
            #print(new_t_stop2)
            try:
                time_start = df[df['timestamp'] == new_t_start].index[0]
            except IndexError:
                delta = timedelta(seconds=1)
                date = datetime.strptime(new_t_start, '%y/%m/%d-%H:%M:%S')
                new_date = date + delta
                new_t_start = new_date.strftime('%y/%m/%d-%H:%M:%S')
                time_start = df[df['timestamp'] == new_t_start].index[0]
    #print(df['timestamp'])
    try:
        time_end = df[df['timestamp'] == t_end].index[0]
        new_t_end = t_end
    except IndexError:
            delta = timedelta(seconds=1)
            date = datetime.strptime(t_end, '%y/%m/%d-%H:%M:%S')
            new_date = date + delta
            new_t_end = new_date.strftime('%y/%m/%d-%H:%M:%S')
            #print(new_t_stop2)
            try:
                time_end = df[df['timestamp'] == new_t_end].index[0]
            except IndexError:
                delta = timedelta(seconds=1)
                date = datetime.strptime(new_t_end, '%y/%m/%d-%H:%M:%S')
                new_date = date + delta
                new_t_end = new_date.strftime('%y/%m/%d-%H:%M:%S')
                time_end = df[df['timestamp'] == new_t_end].index[0]
    time = df['timestamp'].loc[time_start:time_end].tolist()
    #print(time)
    current = df.IMON.loc[time_start:time_end].tolist()
    voltage = df.VMON.loc[time_start:time_end].tolist()
    caen = df.caen.loc[time_start:time_end].tolist()
    channel = df.ch.loc[time_start:time_end].tolist()
    RUP = df.RUP.loc[time_start:time_end].tolist()
    RDW = df.RDW.loc[time_start:time_end].tolist()
    VSET = df.VSET.loc[time_start:time_end].tolist()
    ISET = df.ISET.loc[time_start:time_end].tolist()
    FEA = df.FEA.loc[time_start:time_end].tolist()
    #OVC = df.OVC.loc[time_start:time_end].tolist()
    #time = df.loc[time_start:time_end]['timestamp']
    #print(time)
    #print(voltage)
    data = {'timestamp': time, 'IMON': current, 'VMON': voltage, 'caen':caen, 'ch':channel, 'RUP':RUP, 'RDW':RDW, 'VSET':VSET, 'ISET':ISET}
    new_df = pd.DataFrame(data)
    #print(new_df.iloc[0:,1])
    mean_current = baselineShift(df, t_start_b, t_end_b)
    print(f'current used to baseline correction is {mean_current}')
    #cumulative_charge = []
    for i in range(0, len(new_df['VMON'])-1):
        #print(i)
        if new_df.RUP.iloc[i] == 'no' and new_df.RDW.iloc[i] == 'no':
            charge += new_df.loc[i]['IMON']
        #    print(charge)
    #print(f'charge of caen {caen} ch {channel} is {charge} uC \nperiod: {new_t_start} to {new_t_end}')
    return new_df

def LXe_volume(FEA_test_dir, FEA_data, pressure):
    cols = ['timestamp','ch', 'VMON','IMON']
    all_df_caen1, all_df_caen2, df_ctc = import_caen_data(FEA_test_dir, FEA_data, cols)
    for i in range(0, len(df_ctc['AIO4'])):
        if df_ctc.loc[i, 'AIO4'] < 0:
              df_ctc.loc[i,'AIO4'] = 0
    y = df_ctc[df_ctc['AIO4'] > 0]
    yy = y[y['AIO4'] < 1.01]
    yyy = yy['AIO4']/30
    x = yy['timestamp']
    xx = []
    for el in x:
        xx.append(datetime.strptime(el, '%y/%m/%d-%H:%M:%S'))
    v = np.sum(yyy)/pressure
    print(f"the volume of GXe is: {v}")
    plt.plot(xx,yyy)

def cumulated_charge(df):
    current_list = df.IMON
    delta_t = 2
    cum_charge = []
    charge = 0
    for current in current_list:
        charge += current*delta_t
        cum_charge.append(charge)
    
    df['cumulatedCharge'] = cum_charge
    return df