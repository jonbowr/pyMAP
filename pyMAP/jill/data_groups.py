
# Define dict for importing and integrating different data groups
data_groups = {
        'ILO_EM_status':
            {
                'ILO_EM_IFB':['MCP_VM','MCP_CM','MCP_VSET','PAC_VSET','PAC_VM','PAC_CM','TEMP1','TEMP0','LV_TEMP','MCP_TEMP','PAC_TEMP']
                'ILO_EM_RAW_CNT':['START_A', 'START_C', 'STOP_B0', 'STOP_B3','TOF0','TOF1','TOF2','TOF3','SILVER','Eff_A','Eff_B','Eff_C','Eff_TRIP']
                'ILO_EM_TOF_BD':['AN_A_THR_REG','AN_B0_THR_REG','AN_B3_THR_REG','AN_C_THR_REG']
            }
        }

# define dict with same keys as data_groups to setup plot groups of data
#   might want to move this to a different locaiton or combine somehow with data_groups
plt_groups = {
        'ILO_EM_status':
            {'single_rates [cts/s]':{'yplt':['START_A', 'START_C', 'STOP_B0', 'STOP_B3'],
                                   'logy':True},
                'tof_rate[cts/s]':{'yplt':['TOF0','TOF1','TOF2','TOF3','SILVER'],
                                   'logy':True},
                    'Efficiency':{'yplt':['Eff_A','Eff_B','Eff_C','Eff_TRIP'],
                                   'logy':True},
           'Monitors':{'yplt':['MCP_VM','MCP_CM','MCP_VSET','PAC_VSET','PAC_VM','PAC_CM'],
                                   'logy':True},
           'volts[V]':{'yplt':['TOF_MCP_VM','PAC_VM_volt'],
                                'logy':True
                      },
           'Board Temp':{'yplt':['TEMP1','TEMP0','LV_TEMP','MCP_TEMP','PAC_TEMP'],
                                   'logy':True},
           'Threshold register':{'yplt':['AN_A_THR_REG','AN_B0_THR_REG','AN_B3_THR_REG','AN_C_THR_REG'],
                                   'logy':True},
           } 
}