import numpy as np

data = np.loadtxt("geometry.out", comments = "!", max_rows = 2)
ng = data[0,:].astype('int')
l  = data[1,:]

offset     = 0
disp       = np.prod(ng)
data       = np.zeros([ng[0],ng[1],ng[2],4])
fldinfo    = np.zeros([2])
with open('fld_0001.bin', 'rb') as f:
  for p in range(4):
    f.seek(offset)
    fld = np.fromfile(f, dtype=np.float64, count=disp)
    data[:,:,:,p] = np.reshape(fld, (ng[0], ng[1], ng[2]), order='F')
    offset += 8 * disp
  f.seek(offset)
  fldinfo = np.fromfile(f, dtype=np.float64, count=2)

u = np.zeros((ng[0]+2,ng[1]+2,ng[2]+2))
v = np.zeros((ng[0]+2,ng[1]+2,ng[2]+2))
w = np.zeros((ng[0]+2,ng[1]+2,ng[2]+2)) 
u[1:ng[0]+1,1:ng[1]+1,1:ng[2]+1] = data[:,:,:,0]
v[1:ng[0]+1,1:ng[1]+1,1:ng[2]+1] = data[:,:,:,1] 
w[1:ng[0]+1,1:ng[1]+1,1:ng[2]+1] = data[:,:,:,2]
u[0,1:ng[1]+1,1:ng[2]+1] = u[ng[0],1:ng[1]+1,1:ng[2]+1]
v[1:ng[0]+1,0,1:ng[2]+1] = v[1:ng[0]+1,ng[1],1:ng[2]+1]
w[1:ng[0]+1,1:ng[1]+1,0] = w[1:ng[0]+1,1:ng[1]+1,ng[2]]

u1d = np.reshape(u[0:ng[0],1:ng[1]+1,1:ng[2]+1], -1, order='F')
v1d = np.reshape(v[1:ng[0]+1,0:ng[1],1:ng[2]+1], -1, order='F')
w1d = np.reshape(w[1:ng[0]+1,1:ng[1]+1,0:ng[2]], -1, order='F')

with open("u.txt", "w") as file:
  file.write("FlAT\n")
  file.write(" ".join(map(str, ng)))
  file.write("\n")
  for num in u1d:
    file.write(str(num) + "\n")
with open("v.txt", "w") as file:
  file.write("FlAT\n")
  file.write(" ".join(map(str, ng)))
  file.write("\n")
  for num in v1d:
    file.write(str(num) + "\n")
with open("w.txt", "w") as file:
  file.write("FlAT\n")
  file.write(" ".join(map(str, ng)))
  file.write("\n")
  for num in w1d:
    file.write(str(num) + "\n")