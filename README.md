# CaLES: DIT Case Instructions

This README provides step-by-step guidance for running the Decaying Isotropic Turbulence (DIT) case using the CaLES solver.

<p align="center"> <img src="figures/DIT_Q.png" width="60%" title="Cs = 0.18"> </p>

Here, we present results computed using LES with the Smagorinsky model as the subgrid-scale model. 
Simulations are performed with a grid resolution of N = 32, using Smagorinsky model constant Cs = 0.18.
The figure below shows the result :

<p align="center"> <img src="figures/32_Cs0.18.png" width="60%" title="Cs = 0.18"> </p>

---

## Step 1: Generate Initial Flow Field

Use [TurboGenPY](https://github.com/saadgroup/TurboGenPY) to generate the initial turbulence field.

**Command:**
```bash
python example.py -n 64 -m 5000 --output
```
- `-n`: grid resolution (e.g., 64³)
- `-m`: number of modes (e.g., 5000)
- `--output`: flag to write the result

This will generate initial velocity components (`u_cbc.txt`, `v_cbc.txt`, `w_cbc.txt`).

## Step 2: Create Restart File

Use the initial field files to generate a restart binary file (`fld.bin`) for CaLES.

**Command:**
```bash
python write_restart_dit.py
```
Ensure that `u_cbc.txt`, `v_cbc.txt`, and `w_cbc.txt` are present in the working directory.


## Step 3: Run the Simulation

Run the CaLES solver using the provided `input.nml` and generated `fld.bin`.

Monitor and compare the results at the nondimensional time steps:
- `t = 0.284`
- `t = 0.665`


## Step 4: Compute Energy Spectrum

Post-process the velocity field to compute the turbulent kinetic energy (TKE) spectrum.

1. Extract velocity components from the binary field:
```bash
python read_restart_dit.py
```
This will generate:
- `u.txt`, `v.txt`, `w.txt`: velocity distributions

2. Compute the energy spectrum:
```bash
python example_tkespec.py
```
This script will use `tkespec.py` to compute the TKE spectrum from the velocity fields and save it to:
- `tkespec.txt`

---

## Note:

The DNS and LES calculations follow the same workflow. The only differences lie in the configuration of the SGS (subgrid-scale) model and wall modeling. 

Additionally, DNS simulations require at least a 512-point grid to avoid energy pile-up and ensure numerical stability.