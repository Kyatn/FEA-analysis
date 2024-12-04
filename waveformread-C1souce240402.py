#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 11:33:32 2024

@author: caio
"""

# In[Import libraries]

import numpy as np
import matplotlib.pyplot as plt
import os 

# In[read file]

            
all_files = os.listdir("/home/caio/Documents/rsync-bucket/obsidian-vault/Kamioka/Experiment/FEAtest-2403/waveform-trigCh1-240401/")   # imagine you're one directory above test dir
#print(all_files)  # won't necessarily be sorted
sorted_files = sorted(all_files)
print(sorted_files)

# In[organize files]
C1 = sorted(sorted_files[:909])
C2 = sorted(sorted_files[909:])
print(len(C1))
print(len(C2))
f1 = {}
f2 = {}
for i in range(0, len(C1)):
    f1[i] = np.genfromtxt('/home/caio/Documents/rsync-bucket/obsidian-vault/Kamioka/Experiment/FEAtest-2403/waveform-trigCh1-240401/'+C1[i],
                  dtype= None,delimiter=',',encoding='latin_1', usecols=(0,1)) # column0: time, column1: amplitude
    
for i in range(0, len(C2)):
    f2[i] = np.genfromtxt('/home/caio/Documents/rsync-bucket/obsidian-vault/Kamioka/Experiment/FEAtest-2403/waveform-trigCh1-240401/'+C2[i],
                  dtype= None,delimiter=',',encoding='latin_1', usecols=(0,1)) # column0: time, column1: amplitude
    

#print(f[1])

# In[separate the time and amplitude of each file]


X1 = {}
Y1 = {}

X2 = {}
Y2 = {}

for i in range(0, len(f1)): 
    x = np.zeros(len(f1[i])-4) # skipping the lines of the files which do not contain data
    y = np.zeros(len(f1[i])-4)
    for j in range(4, len(f1[i])):
        x[j-4] = f1[i][j][0]

    for k in range(4, len(f1[i])):
        y[k-4] = f1[i][k][1]
    X1[i] = x*1e9
    Y1[i] = y*1e3


for i in range(0, len(f2)): 
    x = np.zeros(len(f2[i])-4)
    y = np.zeros(len(f2[i])-4)
    for j in range(4, len(f2[i])):
        x[j-4] = f2[i][j][0]

    for k in range(4, len(f2[i])):
        y[k-4] = f2[i][k][1]
    
    X2[i] = x*1e9
    Y2[i] = y*1e3

print(Y1)


# In[sum of amplitudes]

sumY1 = np.zeros(len(Y1))
sumY2 = np.zeros(len(Y2))

for i in range(0, len(Y1)):
    sumY1[i] = sum(Y1[i])
    
print(max(sumY1))

sumY2 = np.zeros(len(Y2))
for i in range(0, len(Y2)):
    sumY2[i] = sum(Y2[i])
    
print(max(sumY2))


# In[graph function] 

def ampMaxDependent(threshold):
    for i in range(0, len(f1)): #f11 and f2 have the same length
            if sum(Y1[i]) >= threshold or sum(Y2[i]) >= threshold:
                plt.figure(dpi=200, figsize=[10,7])
                #plt.text(0.9, 0.9, 'text', fontsize=5, transform=plt.gcf().transFigure)
                
                plt.subplot(2,2,1)
                plt.title('plot of:'+C1[i]+" greater than %i mV" % threshold)
                plt.plot(X1[i],Y1[i], 'o', markersize=1.5)
                plt.xlabel('time (ns)')
                plt.ylabel('voltage (mV)')
            
                plt.subplot(2,2,2)
                plt.title('amplitude hist')
                plt.hist(Y1[i], bins = 100)
                plt.xlabel('amplitude (mV)')
                plt.ylabel('events')
            
                plt.subplot(2,2,3)
                plt.title('plot of:'+C2[i]+" greater than %i mV" % threshold)
                plt.plot(X2[i],Y2[i], 'o', markersize=1.5, color='purple')
                plt.xlabel('time (ns)')
                plt.ylabel('voltage (mV)')
            
                plt.subplot(2,2,4)
                plt.title('amplitude hist')
                plt.hist(Y2[i], bins = 100, color='purple')
                plt.xlabel('amplitude (mV)')
                plt.ylabel('events')

                plt.tight_layout()
                plt.show()
                
def ampMinDependent(threshold):
    for i in range(0, len(f1)): #f11 and f2 have the same length
            if sum(Y1[i]) <= threshold or sum(Y2[i]) <= threshold:
                plt.figure(dpi=200, figsize=[10,7])#, figsize=[15,10])
               
                plt.subplot(2,2,1)
                plt.title('plot of:'+C1[i]+" smaller than %i mV" % threshold)
                plt.plot(X1[i],Y1[i], 'o', markersize=1.5)
                plt.xlabel('time (ns)')
                plt.ylabel('voltage (mV)')
            
                plt.subplot(2,2,2)
                plt.title('amplitude hist')
                plt.hist(Y1[i], bins = 100)
                plt.xlabel('amplitude (mV)')
                plt.ylabel('events')
            
                plt.subplot(2,2,3)
                plt.title('plot of:'+C2[i]+" smaller than %i mV" % threshold)
                plt.plot(X2[i],Y2[i], 'o', markersize=1.5, color='purple')
                plt.xlabel('time (ns)')
                plt.ylabel('voltage (mV)')
            
                plt.subplot(2,2,4)
                plt.title('amplitude hist')
                plt.hist(Y2[i], bins = 100, color='purple')
                plt.xlabel('amplitude (mV)')
                plt.ylabel('events')

                plt.tight_layout()
                plt.show()
            
            


def histOfAmpMax():
    maxY1 = np.zeros(len(Y1))
    maxY2 = np.zeros(len(Y2))
    for i in range(0, len(f1)):
        maxY1[i] = max(Y1[i])
    for i in range(0, len(f2)):
        maxY2[i] = max(Y2[i])
    plt.figure(dpi=200)
    plt.subplot(2,1,1)
    plt.title('amplitude max value histogram (ch.1)')
    plt.hist(maxY1, bins=50)
    plt.xlabel('amplitude (mV)')
    plt.ylabel('events')
    plt.subplot(2,1,2)
    plt.title('amplitude max value histogram (ch.2)')
    plt.hist(maxY2, bins=50, color='purple')
    plt.xlabel('amplitude (mV)')
    plt.ylabel('events')
    
    plt.tight_layout()
    plt.show()

def histOfAmpMin():
    minY1 = np.zeros(len(Y1))
    minY2 = np.zeros(len(Y2))
    for i in range(0, len(f1)):
        minY1[i] = min(Y1[i])
    for i in range(0, len(f2)):
        minY2[i] = min(Y2[i])
        
    plt.figure(dpi=200)
    plt.subplot(2,1,1)
    plt.title('amplitude min value histogram (ch.1)')
    plt.hist(minY1, bins=50)
    plt.xlabel('amplitude (mV)')
    plt.ylabel('events')
    
    plt.subplot(2,1,2)
    plt.title('amplitude min value histogram (ch.2)')
    plt.hist(minY2, bins=50, color='purple')
    plt.xlabel('amplitude (mV)')
    plt.ylabel('events')
    
    plt.tight_layout()
    plt.show()
    
def individualWaveform(event):
    plt.figure(dpi=200)
    
    plt.subplot(2,1,1)
    plt.title('plot of:'+C1[event])
    plt.plot(X1[event],Y1[event], 'o', markersize=1)
    plt.xlabel('time (ns)')
    plt.ylabel('voltage (mV)')
    plt.subplot(2,1,2)
    plt.title('plot of:'+C2[event])
    plt.plot(X2[event],Y2[event], 'o', markersize=1, color='purple')
    plt.xlabel('time (ns)')
    plt.ylabel('voltage (mV)')
    
    plt.tight_layout()
    plt.show()


# In[distribution of sum of amplitudes]


# histogram of the sum of amplitudes of each waveform
plt.figure(dpi=200)
plt.subplot(2,1,1)
plt.title('amp. sum histogram ch.1')
plt.hist(sumY1, bins=20)
plt.xlabel('amplitude sum (mV)')
plt.ylabel('events')
plt.ylim([0,50])

plt.subplot(2,1,2)
plt.title('amp. sum histogram ch.2')
plt.hist(sumY2, bins=20, color='purple')
plt.xlabel('amplitude sum (mV)')
plt.ylabel('events')
plt.ylim([0,50])

plt.tight_layout()
plt.show()


# In[distribution of amplitudes]

# distribution of the max amplitude value of each event
histOfAmpMax()
histOfAmpMin()

# In[plot depending on threshold]

gthanthreshold = 200000
lthanthreshold = -100000
ampMaxDependent(gthanthreshold)
ampMinDependent(lthanthreshold)

# In[Individual waveform plot]

event = 0 # must be greater than 32
individualWaveform(event) 

event2 = 77
individualWaveform(event2) 
  





























