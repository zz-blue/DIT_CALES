import numpy as np
from scipy.integrate import simps
import sys

with open("u_cbc_dns.txt", "r") as file:
  second_line = file.readlines()[1].strip()
  ng = [int(num) for num in second_line.split()]
  nx = ng[0]
  ny = ng[1]
  nz = ng[2]

filter_width = int(sys.argv[1])
offset = filter_width//2-1
nx_small = nx//filter_width
ny_small = ny//filter_width
nz_small = nz//filter_width

u = np.zeros((nx+filter_width, ny+2, nz+2))
v = np.zeros((nx+2, ny+filter_width, nz+2))
w = np.zeros((nx+2, ny+2, nz+filter_width))

# for i in range(1-filter_width//2,nx+filter_width//2+1):
#   for j in range(1,ny+1):
#     for k in range(1,nz+1):
#       u[i+offset,j,k] = (i-1)/nx+(j-0.5)/ny+(k-0.5)/nz


# for i in range(1,nx+1):
#   for j in range(1-filter_width//2,ny+filter_width//2+1):
#     for k in range(1,nz+1):
#       v[i,j+offset,k] = (i-0.5)/nx+(j-1)/ny+(k-0.5)/nz


# for i in range(1,nx+1):
#   for j in range(1,ny+1):
#     for k in range(1-filter_width//2,nz+filter_width//2+1):
#       w[i,j,k+offset] = (i-0.5)/nx+(j-0.5)/ny+(k-1)/nz

u1d = np.loadtxt("u_cbc_dns.txt", skiprows=2)
v1d = np.loadtxt("v_cbc_dns.txt", skiprows=2)
w1d = np.loadtxt("w_cbc_dns.txt", skiprows=2)
u[1:nx+1,1:ny+1,1:nz+1] = np.reshape(u1d,(nx,ny,nz),order='F')
v[1:nx+1,1:ny+1,1:nz+1] = np.reshape(v1d,(nx,ny,nz),order='F')
w[1:nx+1,1:ny+1,1:nz+1] = np.reshape(w1d,(nx,ny,nz),order='F')
for m in range(0,filter_width//2):
  u[-m+offset,:,:] = u[nx-m+offset,:,:]
  v[:,-m+offset,:] = v[:,ny-m+offset,:]
  w[:,:,-m+offset] = w[:,:,nz-m+offset]

uf = np.zeros((nx_small+2,ny_small+2,nz_small+2))
vf = np.zeros((nx_small+2,ny_small+2,nz_small+2))
wf = np.zeros((nx_small+2,ny_small+2,nz_small+2))
for i in range(1,nx_small+1):
  for j in range(1,ny_small+1):
    for k in range(1,nz_small+1):
      # filtered u
      ii = (i-1)*filter_width + 1
      u_local = u[ ii-filter_width//2+offset:ii+filter_width//2+1+offset,
                  (j-1)*filter_width+1:j*filter_width+1,
                  (k-1)*filter_width+1:k*filter_width+1
                 ]
      integral_z = np.mean(u_local, axis=2)
      integral_yz = np.mean(integral_z, axis=1)
      integral_xyz = np.trapz(integral_yz, dx=1./filter_width, axis=0)
      uf[i,j,k] = integral_xyz
      # filtered v
      jj = (j-1)*filter_width + 1
      v_local = v[(i-1)*filter_width+1:i*filter_width+1,
                  jj-filter_width//2+offset:jj+filter_width//2+1+offset,
                  (k-1)*filter_width+1:k*filter_width+1
                 ]
      integral_z = np.mean(v_local, axis=2)
      integral_yz = np.trapz(integral_z, dx=1./filter_width, axis=1)
      integral_xyz = np.mean(integral_yz, axis=0)
      vf[i,j,k] = integral_xyz
      # filtered w
      kk = (k-1)*filter_width + 1
      w_local = w[(i-1)*filter_width+1:i*filter_width+1,
                  (j-1)*filter_width+1:j*filter_width+1,
                  kk-filter_width//2+offset:kk+filter_width//2+1+offset
                 ]
      integral_z = np.trapz(w_local, dx=1./filter_width, axis=2)
      integral_yz = np.mean(integral_z, axis=1)
      integral_xyz = np.mean(integral_yz, axis=0)
      wf[i,j,k] = integral_xyz


ng_small = [nx_small,ny_small,nz_small]
u1d = np.reshape(uf[1:nx_small+1,1:ny_small+1,1:nz_small+1], -1, order='F')
v1d = np.reshape(vf[1:nx_small+1,1:ny_small+1,1:nz_small+1], -1, order='F')
w1d = np.reshape(wf[1:nx_small+1,1:ny_small+1,1:nz_small+1], -1, order='F')

with open("u_cbc.txt", "w") as file:
  file.write("FlAT\n")
  file.write(" ".join(map(str, ng_small)))
  file.write("\n")
  for num in u1d:
    file.write(str(num) + "\n")
with open("v_cbc.txt", "w") as file:
  file.write("FlAT\n")
  file.write(" ".join(map(str, ng_small)))
  file.write("\n")
  for num in v1d:
    file.write(str(num) + "\n")
with open("w_cbc.txt", "w") as file:
  file.write("FlAT\n")
  file.write(" ".join(map(str, ng_small)))
  file.write("\n")
  for num in w1d:
    file.write(str(num) + "\n")