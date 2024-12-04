#!/usr/bin/env python
# coding: utf-8

# In[1]:

import matplotlib.pyplot as plt
import numpy as np


# In[2]:


y = np.array([10.4, 15.0, 17.0, 22.4])

x = np.array([-5.268, -5.385, -5.420, -5.560])


# In[3]:

# plot of the raw data
fig = plt.figure()

ax = fig.add_subplot(1,1,1, title='temp. calibration (w/o Xe)', ylabel='AIO3 (V)', xlabel='temperature(C)')
ax.scatter(x,y)


# In[4]:

# fitting linear model to the data
coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef) 
# poly1d_fn is now a function which takes in x and returns an estimate for y

plt.plot(x,y, 'yo', x, poly1d_fn(x), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
plt.xlabel('temperature(C)')
plt.ylabel('AIO3 (V)')
plt.title('temp. calibration')


print(coef)


# In[pressure calibration data raw plot]
# x: pressure screen, y: AIO1, y2:AIO3

y_p = np.array([-0.032, -0.021, -0.012, -0.001, 0.046, 0.094, 0.146, 0.193, 0.249, 0.274, 0.299])
y2_p = np.array([-0.101, -0.058, -0.039, -0.032, -0.021, -0.012, -0.001, 0.046, 0.094, 0.146, 0.193, 0.249, 0.274, 0.299])

x_p = np.array([-1.179, -1.055, -0.955, -0.829, -0.303, 0.269, 0.868, 1.405, 2.078, 2.376, 2.667])

x2_p = np.array([0.009, 0.350, 0.499, 0.566, 0.658, 0.733, 0.824, 1.208, 1.616, 2.049, 2.441, 2.908, 3.116, 3.324])

fig2 = plt.figure()
ax1 = fig2.add_subplot(1,1,1,title='pressurecalibration AIO1', xlabel='pressure', ylabel='AIO1')
ax1.scatter(x_p,y_p)

fig3 = plt.figure()
ax2 = fig3.add_subplot(1,1,1,title='pressurecalibration AIO2', xlabel='pressure', ylabel='AIO2')
ax2.scatter(x2_p,y2_p)

# In[pressure calibration fitting]

# fitting linear model to the data
coef2 = np.polyfit(x_p,y_p,1)
coef3 = np.polyfit(x2_p,y2_p,1)
poly1d_fn2 = np.poly1d(coef2) 
poly1d_fn3 = np.poly1d(coef3)
# poly1d_fn is now a function which takes in x and returns an estimate for y

plt.figure()
plt.plot(x_p,y_p, 'yo', x_p, poly1d_fn2(x_p), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
plt.ylabel('MPa')
plt.xlabel('AIO1(V)')
plt.title('pressure calibration AIO1')

plt.show()

plt.plot(x2_p,y2_p, 'yo', x2_p, poly1d_fn3(x2_p), '--k') #'--k'=black dashed line, 'yo' = yellow circle marker
plt.xlabel('MPa')
plt.ylabel('AIO2(V)')
plt.title('pressure calibration AIO2')


print("AIO1 coefficient is:", coef2)
print("AIO2 coefficient is:", coef3)







































