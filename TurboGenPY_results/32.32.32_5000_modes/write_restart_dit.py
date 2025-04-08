import numpy as np

with open("u_cbc.txt", "r") as file:
  second_line = file.readlines()[1].strip()
  ng = [int(num) for num in second_line.split()]
u1d = np.loadtxt("u_cbc.txt", skiprows=2)
v1d = np.loadtxt("v_cbc.txt", skiprows=2)
w1d = np.loadtxt("w_cbc.txt", skiprows=2)
u = np.zeros((ng[0]+2,ng[1]+2,ng[2]+2))
v = np.zeros((ng[0]+2,ng[1]+2,ng[2]+2))
w = np.zeros((ng[0]+2,ng[1]+2,ng[2]+2))

u[0:ng[0]  ,1:ng[1]+1,1:ng[2]+1] = np.reshape(u1d,(ng[0],ng[1],ng[2]),order='F')
v[1:ng[0]+1,0:ng[1]  ,1:ng[2]+1] = np.reshape(v1d,(ng[0],ng[1],ng[2]),order='F')
w[1:ng[0]+1,1:ng[1]+1,0:ng[2]  ] = np.reshape(w1d,(ng[0],ng[1],ng[2]),order='F')
u[ng[0],1:ng[1]+1,1:ng[2]+1] = u[0,1:ng[1]+1,1:ng[2]+1]
v[1:ng[0]+1,ng[1],1:ng[2]+1] = v[1:ng[0]+1,0,1:ng[2]+1]
w[1:ng[0]+1,1:ng[1]+1,ng[2]] = w[1:ng[0]+1,1:ng[1]+1,0]

data = np.zeros([ng[0],ng[1],ng[2],4])
data[:,:,:,0] = u[1:ng[0]+1,1:ng[1]+1,1:ng[2]+1]
data[:,:,:,1] = v[1:ng[0]+1,1:ng[1]+1,1:ng[2]+1]
data[:,:,:,2] = w[1:ng[0]+1,1:ng[1]+1,1:ng[2]+1]
data[:,:,:,3] = 0.0

offset     = 0
disp       = np.prod(ng)
fldinfo    = np.zeros([2])
fldinfo[0] = 0.0 # time
fldinfo[1] = 0.0 # step
with open('fld.bin','wb') as f:
  for p in range(4):
    f.seek(offset)
    fld = np.reshape(data[:,:,:,p], (disp,), order='F')
    fld.tofile(f)
    offset += 8*disp
  f.seek(offset)
  fldinfo.tofile(f)