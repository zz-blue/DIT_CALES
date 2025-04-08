# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 13:27:48 2015

@author: tsaad
"""
from fileformats import FileFormats
import multiprocessing as mp
import time

#------------------------------------------------------------------------------

def writefileparallel(u, v, w, dx, dy, dz, fileformat):
  print ('Writing to disk. This may take a while...')
  writeufile = mp.Process(target=writefile, args=('u.txt','x',dx,dy,dz,u, fileformat))
  writeufile.start()
  
  writevfile = mp.Process(target=writefile, args=('v.txt','y',dx,dy,dz,v, fileformat))
  writevfile.start()
  
  writewfile = mp.Process(target=writefile, args=('w.txt','z',dx,dy,dz,w, fileformat))
  writewfile.start()
  
  writeufile.join()
  writevfile.join()
  writewfile.join()
  
#------------------------------------------------------------------------------
  
def writefile(filename, velcomponent, dx, dy, dz, velarray, fileformat):
  t0 = time.time()  

  nx = len(velarray[:,0,0])
  ny = len(velarray[0,:,0])
  nz = len(velarray[0,0,:])  
  
  f = open(filename , 'w')
  zo=[0,0,0]
  if(velcomponent=='x'):
    zo=[0,1,1]
  elif(velcomponent=='y'):
    zo=[1,0,1]
  else:
    zo=[1,1,0]
    
  # loop over the velocity fields generated by each thread
  if (fileformat == FileFormats.XYZ):    
    f.write('%s \n' % 'XYZ')
    xlo = zo[0]*dx/2.0
    ylo = zo[1]*dy/2.0
    zlo = zo[2]*dz/2.0
    for k in range(0,nz):
      for j in range(0,ny):
        for i in range(0,nx):
          x = xlo + i*dx
          y = ylo + j*dy
          z = zlo + k*dz
          u = velarray[i,j,k]              
          f.write('%.16f %.16f %.16f %.16f \n' % (x,y,z,u))        
  elif (fileformat == FileFormats.IJK):
    f.write('%s \n' % 'IJK')    
    for k in range(0,nz):
      for j in range(0,ny):
        for i in range(0,nx):
          u = velarray[i,j,k]              
          f.write('%d %d %d %.16f \n' % (i,j,k,u))
  else:
    f.write('%s \n' % 'FLAT')
    f.write('%d %d %d \n' % (nx, ny, nz))
    for k in range(0,nz):
      for j in range(0,ny):
        for i in range(0,nx):
          u = velarray[i,j,k]              
          f.write('%.16f\n' % u)        
  f.close()
  t1 = time.time()
  print ('Done writing to disk in ', t1 - t0, 's')

#------------------------------------------------------------------------------