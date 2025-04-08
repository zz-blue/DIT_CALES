# -*- coding: utf-8 -*-
"""
Created on Thu May  8 20:08:01 2014

@author: Tony Saad
"""
# !/usr/bin/env python
import numpy as np
from numpy import pi
from tkespec import compute_tke_spectrum_flatarrays

lx = 9 * 2.0 * pi / 100.0
ly = 9 * 2.0 * pi / 100.0
lz = 9 * 2.0 * pi / 100.0

with open("u.txt", 'r') as file:
  lines = file.readlines()
  nx, ny, nz = map(int, lines[1].split())

with open("u.txt", 'r') as file:
  lines = file.readlines()
  data = [float(line.strip()) for line in lines[2:]]
  u = np.array(data)
with open("v.txt", 'r') as file:
  lines = file.readlines()
  data = [float(line.strip()) for line in lines[2:]]
  v = np.array(data)
with open("w.txt", 'r') as file:
  lines = file.readlines()
  data = [float(line.strip()) for line in lines[2:]]
  w = np.array(data)

knyquist, wavenumbers, tkespec = compute_tke_spectrum_flatarrays(u, v, w, nx, ny, nz, lx, ly, lz, False)
np.savetxt('tkespec.txt', np.transpose([wavenumbers, tkespec]))