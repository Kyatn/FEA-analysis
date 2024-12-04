### PACKAGES
import pandas as pd
from datetime import datetime
from datetime import timedelta
import os

#definitions
delta_t = 2
today = datetime.today()

### functions #################################################################

def timestampTotime(df):
    timestamps = df['timestamp']
    folder = []
    folder_full = []
    for stamp in timestamps:
        print(type(stamp))
        if isinstance(stamp, str):
            print(stamp)
            stamp = float(stamp)
        if stamp > 10000000000000:
            stamp = stamp/1000
        time = datetime.fromtimestamp(stamp)
        #strtime = time.strftime('%H:%M:%S')
        strtime = time.strftime('%y/%m/%d-%H:%M:%S')
        strtimee = datetime.strptime(strtime, '%y/%m/%d-%H:%M:%S')
        folder.append(strtime)
        folder_full.append(strtimee)
    return folder, folder_full

def baseline_correction_val(df, t_start, t_stop):
    try:
        idx_start = df[df.date == t_start].index[0]
    except IndexError:
        delta = timedelta(seconds=1)
        date = datetime.strptime(t_start, '%y/%m/%d-%H:%M:%S')
        print(date)
        new_date = date + delta
        new_t_start = new_date.strftime('%y/%m/%d-%H:%M:%S')
        print(new_t_start)
        try:
            idx_start = df[df.date == new_t_start].index[0]
        except IndexError:
            delta = timedelta(seconds=1)
            date2 = datetime.strptime(new_t_start, '%y/%m/%d-%H:%M:%S')
            new_date2 = date2 + delta
            new_t_start2 = new_date2.strftime('%y/%m/%d-%H:%M:%S')
            print(new_t_start2)
            idx_start = df[df.date == new_t_start2].index[0]
    print(idx_start)
    try:
        idx_stop = df[df.date == t_stop].index[0]
    except IndexError:
        delta = timedelta(seconds=1)
        date = datetime.strptime(t_stop, '%y/%m/%d-%H:%M:%S')
        new_date = date + delta
        new_t_stop = new_date.strftime('%y/%m/%d-%H:%M:%S')
        try:
            idx_stop = df[df.date == new_t_stop].index[0]
        except IndexError:
            delta = timedelta(seconds=1)
            date = datetime.strptime(new_t_stop, '%y/%m/%d-%H:%M:%S')
            new_date = date + delta
            new_t_stop = new_date.strftime('%y/%m/%d-%H:%M:%S')
            idx_stop = df[df.date == new_t_stop].index[0]
    #print(df_ch2_corr.iloc[idx_start-1:idx_stop]['current'])
    charge = sum(df.loc[idx_start-1:idx_stop]['current'])
    mean_current = charge/len(df['date'].loc[idx_start-1:idx_stop])
    return mean_current

# corrected current
def baselineShift(df, start, end):
    mean_current = baseline_correction_val(df,start,end)
    df.iloc[:, 1] -= mean_current
    return mean_current

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

def total_charge(df, t_start, t_end):
    time, date = timestampTotime(df) # we have the date also in a list in case we need it
    #time = []
    #for timestamp in df['timestamp']:
    # corr_time = pd.Timestamp(timestamp)
    # time.append(corr_time)
    #print(time)
    current = df.IMON
    delta_t = 2
    voltage = df.VMON
    charge = 0
    #print(voltage)
    data = {'date': time,'current': current, 'voltage': voltage}
    new_df = pd.DataFrame(data)
    new_df
    #print(new_df.iloc[0:,1])
    mean_current = baselineShift(new_df, t_start, t_end)
    print(f'current used to baseline correction is {mean_current}')
    for i in range(0,len(new_df['voltage'])-1):
        if abs(new_df['voltage'].iloc[i+1] - new_df['voltage'].iloc[i]) < 1:
            charge += new_df['current'].iloc[i]*delta_t
            #print(charge)
    return charge, mean_current

##############################################################################

directory = '/home/caio/data/241119_4FEA_LXe/datalogsZip/'
path_list_1, path_list_2 = sep_caen1_caen2(directory)

path_list_1.sort()
path_list_2.sort()

###############################################################################
### separating channels #######################################################

# dataframe for caen1 and caen2 separately
df1 = [pd.read_csv(files, sep=',', usecols = ['timestamp','ch', 'VMON','IMON']) for files in path_list_1]
df2 = [pd.read_csv(files, sep=',', usecols = ['timestamp','ch', 'VMON','IMON']) for files in path_list_2]

# concat files
df_caen1 = pd.concat(df1, ignore_index=True)
df_caen2 = pd.concat(df2, ignore_index=True)

#df_caen1['timestamp'] = df_caen1['timestamp'].astype(datetime)
#df_caen2['timestamp'] = df_caen2['timestamp']

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

###############################################################################

# period to take as reference to calculate the correction current
t_start = '24/11/26-13:00:00'
t_end = '24/11/26-13:20:00'

#t_start2 = '24/08/28-11:40:01'
#t_end2 = '24/08/28-17:00:00'

#
all_df_caen1 = [df_caen1HV0, df_caen1HV1, df_caen1HV2, df_caen1HV3]
all_df_caen2 = [df_caen2HV0, df_caen2HV1, df_caen2HV2, df_caen2HV3]

result_caen1 = [total_charge(all_df_caen1[0], t_start, t_end), total_charge(all_df_caen1[1], t_start, t_end), total_charge(all_df_caen1[2], t_start, t_end), total_charge(all_df_caen1[3], t_start, t_end)]
result_caen2 = [total_charge(all_df_caen2[0], t_start, t_end), total_charge(all_df_caen2[1], t_start, t_end), total_charge(all_df_caen2[2], t_start, t_end), total_charge(all_df_caen2[3], t_start, t_end)]


charge_1 = [result_caen1[i][0] for i in range(0, len(all_df_caen1))]
charge_2 = [result_caen2[i][0] for i in range(0, len(all_df_caen2))]

charge = {'int_C1HV0':charge_1[0], 'int_C1HV1':charge_1[1], 'int_C1HV2':charge_1[2], 'int_C1HV3':charge_1[3], 'int_C2HV0':charge_2[0], 'int_C2HV1':charge_2[1], 'int_C2HV2':charge_2[2], 'int_C2HV3':charge_2[3]}

mean_current_1 = [result_caen1[i][1] for i in range(0, len(all_df_caen1))]
mean_current_2 = [result_caen2[i][1] for i in range(0, len(all_df_caen2))]


print(f'\ncharge of caen1 HV0 is {charge_1[0]} uC'
      f'\ncharge of caen1 HV1 is {charge_1[1]} uC'
      f'\ncharge of caen1 HV2 is {charge_1[2]} uC'
      f'\ncharge of caen1 HV3 is {charge_1[3]} uC\n'
      f'\ncharge of caen2 HV0 is {charge_2[0]} uC'
      f'\ncharge of caen2 HV1 is {charge_2[1]} uC'
      f'\ncharge of caen2 HV2 is {charge_2[2]} uC'
      f'\ncharge of caen2 HV3 is {charge_2[3]} uC\n'

      f'last updated {today}\n')

### update of the existing integration

import sys
import os
import importlib.util
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)
# directory reach
#directory = path.path(__file__).abspath()
import db_utils as db_utils
import time


import libABCD
libABCD.init('dblogger',publisher=True, listener=True, connect=True)


#ctc100_topic = 'sc/temp/ctc100/get'
caen1_topic = 'sc/hv/caen1/get'
caen2_topic = 'sc/hv/caen2/get'

measurement = 'fea'
run_name = 'continuous_run'
def get_source_from_topic(topic):
    stopic = topic.split('/')
    return stopic[-2]

#def logtodb(msg='', topic=''):
#    time = int(msg['timestamp']*1e9)
#    tags = {}
#    tags['run'] = run_name
#    source = get_source_from_topic(topic)
#    tags['source'] = source
#    global charge_1
#    global charge_2
#    db_utils.push_to_influx(measurement, time, charge, tags=tags)

def caen_integration(msg='', topic=''):
    time = int(msg['timestamp']*1e9)
    today = datetime.today()
    tags = {}
    tags['run'] = run_name
    source =  get_source_from_topic(topic)
    tags['source'] = source
    if 'caen1' in source:
        global charge_1
        charge_caen1 = {'int_C1HV0':charge_1[0], 'int_C1HV1':charge_1[1], 'int_C1HV2':charge_1[2], 'int_C1HV3':charge_1[3]}
        for l in msg['payload']:
            #print(l['tags']['channel'])
            current = l['data']['IMON']
            #print(current)
            ramp_up = l['data']['RAMPINGUP']
            ramp_down = l['data']['RAMPINGDOWN']
            channel = l['tags']['channel']
            if current >= 0:
                if ramp_up == 'no' and ramp_down == 'no':
                    charge_1[channel] += (current - mean_current_1[channel])*delta_t
            sc = msg['from']
            integration_val = charge_1[channel]
            print(f'charge of {sc} {channel} is {integration_val} uC')
        db_utils.push_to_influx(measurement, time, charge_caen1, tags=tags)
    elif 'caen2' in source:
        global charge_2
        charge_caen2 = {'int_C2HV0':charge_2[0], 'int_C2HV1':charge_2[1], 'int_C2HV2':charge_2[2], 'int_C2HV3':charge_2[3]}
        for l in msg['payload']:
            current = l['data']['IMON']
            #print(current)
            ramp_up = l['data']['RAMPINGUP']
            ramp_down = l['data']['RAMPINGDOWN']
            channel = l['tags']['channel']
            if current >= 0:
                if ramp_up == 'no' and ramp_down == 'no':
                    charge_2[channel] += (current - mean_current_2[channel])*delta_t
            sc = msg['from']
            integration_val = charge_2[channel]
            print(f'charge of {sc} {channel} is {integration_val} uC')
        db_utils.push_to_influx(measurement, time, charge_caen2, tags=tags)
    print(f'last updated {today}\n')



#libABCD.subscribe(ctc100_topic)
libABCD.subscribe(caen1_topic)
libABCD.subscribe(caen2_topic)

#libABCD.add_callback(ctc100_topic, logtodb)
libABCD.add_callback(caen1_topic, caen_integration)
libABCD.add_callback(caen2_topic, caen_integration)
libABCD.add_callback(caen1_topic, logtodb)
libABCD.add_callback(caen2_topic, logtodb)
