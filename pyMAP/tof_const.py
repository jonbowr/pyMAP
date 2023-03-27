
# delay line values determined through cal data analysis 
tof3_peaks_ns = {'lables':['Q3','Q2','Q1','Q0'],
                # IBEX-lo Tof3 quadrant values, determined through flight data analysis
                'ibex_lo_flt':[0.6900568049562702, 4.018218774092078, 7.277728085556459, 11.991842880356202],
                # IMAP-lo em quadrant values, determined through spectra analysis of EMv1 Data
                'imap_lo_em': [ 1.92932145,  4.81973704,  7.84855093, 12.6265124 ],
                }

# electron flight time [nS] determined through simulation
t_elec_ns = {1:4.375828,2:4.097131}

# Dimension of TOF in cm
tof_dims_cm = {'TOF0':50,'TOF1':22.5,'TOF2':27.7}

# electron mass
m_elec_amu = .00055 #AMU

# Conversion factors used in tof calculations
# AMU to kG
amu_c = 1.660539*10**-27#Kg/AMU
# cm/ns to m/s
cm_c = 10**6 #ns/cm*m/s
#convert V[V]*q
qv = 1.6*10**-19#kg*m^2/s^2/e
