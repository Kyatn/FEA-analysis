#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 18:24:36 2024

@author: caio
"""

#import influxdb_client
#from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
import pandas as pd
from datetime import datetime
import pytz
from datetime import timezone
from backports.zoneinfo import ZoneInfo
import time
#import config

# In[]
with open('/home/caio/remote-IPMU/Kamioka-data/CAEN_logs/CAENGECO2020240516-240524.log', 'r') as f:
    lines = f.readlines()
    invlines = lines[::-1]
    for l in invlines:
        l_s = l.split(' ')
        print(l_s)
        dateascii = l_s[0][1:-2]
        #date_log = date.replace(tzinfo=pytz.timezone('Japan'))
        try:
            date_log = datetime.strptime(dateascii,'%Y-%m-%dT%H:%M:%S')
        except ValueError:
            print("empty line here!")
            pass
        jp = ZoneInfo('Asia/Tokyo')
        date_log = date_log.replace(tzinfo= jp)
        date_log=date_log.astimezone(tz=pytz.timezone('UTC'))
#            print('datelog = ', date_log)
    print('ended the db update')