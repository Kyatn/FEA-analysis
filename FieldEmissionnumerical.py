#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:47:55 2024

@author: caio
"""

# In[import packages]
import numpy as np
import matplotlib.pyplot as plt

#plt.style.available
plt.style.use('seaborn-v0_8')

# In[defining function: Fowler-Nordheim function]

def J_FN(F,W):
    aFN = 1.54
    bFN = 6.83
    result = aFN * F**2/W * np.exp(-bFN * W**(3/2)/F)
    return result

Fd = np.arange(0, 100, 0.1)
Wd = np.arange(0, 30, 0.1)

J_FN_fW1 = J_FN(Fd, 4)
J_FN_fW2 = J_FN(Fd, 4.5)
J_FN_fW3 = J_FN(Fd, 5)
J_FN_fW4 = J_FN(Fd, 10)
J_FN_fW5 = J_FN(Fd, 11.5)
J_FN_fW6 = J_FN(Fd, 12)
J_FN_fW7 = J_FN(Fd, 15)


J_FN_fF10 = J_FN(2, Wd)
J_FN_fF11 = J_FN(4, Wd)
J_FN_fF9 = J_FN(6, Wd)
J_FN_fF1 = J_FN(8, Wd)
J_FN_fF2 = J_FN(15, Wd)
J_FN_fF3 = J_FN(20, Wd)
J_FN_fF4 = J_FN(25, Wd)
J_FN_fF5 = J_FN(30, Wd)
J_FN_fF6 = J_FN(50, Wd)
J_FN_fF7 = J_FN(75, Wd)
J_FN_fF8 = J_FN(100, Wd)


# In[fixed W plots]

plt.figure(dpi=200)

plt.plot(Fd, J_FN_fW1, label = 'W = 4')
plt.plot(Fd, J_FN_fW2, label = 'W = 4.5')
plt.plot(Fd, J_FN_fW3, label = 'W = 5')
plt.plot(Fd, J_FN_fW4, label = 'W = 10')
plt.plot(Fd, J_FN_fW5, label = 'W = 11.5')
plt.plot(Fd, J_FN_fW6, label = 'W = 12')
plt.plot(Fd, J_FN_fW7, label = 'W = 15')

plt.xlim(4, 10)
plt.ylim(0, 0.2)
plt.yscale("linear")

plt.title('fixed W plot')
plt.xlabel('F (V/nm)')
plt.ylabel('J_FN (uA/V^2)')

plt.legend()

plt.show()

# In[fixed F plots]

plt.figure(dpi=200)

plt.plot(Wd, J_FN_fF10, label = 'F = 2')
plt.plot(Wd, J_FN_fF11, label = 'F = 4')
plt.plot(Wd, J_FN_fF9, label = 'F = 6')
plt.plot(Wd, J_FN_fF1, label = 'F = 8')
plt.plot(Wd, J_FN_fF2, label = 'F = 15')
plt.plot(Wd, J_FN_fF3, label = 'F = 20')


plt.xlim(3, 10)
plt.ylim(0, 0.50)

plt.title('fixed W plot')
plt.xlabel('W (eV)')
plt.ylabel('J_FN (uA/V^2)')

plt.legend()

plt.show()














































