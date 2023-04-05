
# Define dict for importing and integrating different data groups
data_groups = {
        'ILO_EM_status':

            {
                'ILO_EM_IFB':['dateTime','MCP_VM','MCP_CM','MCP_VSET','PAC_VSET','PAC_VM','PAC_CM','TEMP1','TEMP0','LV_TEMP','MCP_TEMP','PAC_TEMP','PAC_VM_volt'],
                'ILO_EM_RAW_CNT':['dateTime','START_A', 'START_C', 'STOP_B0', 'STOP_B3','TOF0','TOF1','TOF2','TOF3','SILVER','Eff_A','Eff_B','Eff_C','Eff_TRIP'],
                'ILO_EM_TOF_BD':['dateTime','AN_A_THR_REG','AN_B0_THR_REG','AN_B3_THR_REG','AN_C_THR_REG','TOF_MCP_VM']
            }
        }

# define dict with same keys as data_groups to setup plot groups of data
#   might want to move this to a different locaiton or combine somehow with data_groups
plt_groups = {
        'ILO_EM_status':
            {
            'single_rates [cts/s]':['START_A', 'START_C', 'STOP_B0', 'STOP_B3'],                 
            'tof_rate[cts/s]':['TOF0','TOF1','TOF2','TOF3','SILVER'],             
            'Efficiency':['Eff_A','Eff_B','Eff_C','Eff_TRIP'],      
           'Monitors':['MCP_VM','MCP_CM','MCP_VSET','PAC_VSET','PAC_VM','PAC_CM'],          
           'volts[V]':['TOF_MCP_VM','PAC_VM_volt'],  
           'Board Temp':['TEMP1','TEMP0','LV_TEMP','MCP_TEMP','PAC_TEMP'],        
           'Threshold register':['AN_A_THR_REG','AN_B0_THR_REG','AN_B3_THR_REG','AN_C_THR_REG'],                    
           } 
}