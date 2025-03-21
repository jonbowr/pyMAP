from numpy import dtype

dtypes = {
    'ILO_IFB':{'SHCOARSE': dtype('int64'),
         'IF_COMMAND_ERROR': dtype('int64'),
         'IF_TRANSMITTING': dtype('int64'),
         'IF_READY': dtype('int64'),
         'IF_STATE': dtype('int64'),
         'COMMAND_ADDRESS': dtype('int64'),
         'COMMAND_DATA': dtype('int64'),
         'REG_IF_STATUS_PKT_RCVD': dtype('int64'),
         'REG_IF_STATUS_TO_ERR': dtype('int64'),
         'REG_IF_STATUS_ID_ERR': dtype('int64'),
         'REG_IF_STATUS_FRM_ERR': dtype('int64'),
         'FPGA_VERSION': dtype('int64'),
         'HV_DIS_HK_N': dtype('int64'),
         'HV_LIM_N': dtype('int64'),
         'BOARD_ID': dtype('int64'),
         'COMMAND_COUNT': dtype('int64'),
         'INT_MUX': dtype('int64'),
         'ADC_CLK_DIS': dtype('int64'),
         'OSCOPE_ENB': dtype('int64'),
         'STAR_SYNC_SEL': dtype('int64'),
         'DATA_ENB': dtype('int64'),
         'DATA_INTERVAL': dtype('float64'),
         'SYNC_CLK_DIS_1': dtype('int64'),
         'PAC_ENB[0]': dtype('int64'),
         'PAC_ENB[1]': dtype('int64'),
         'PAC_ENB_1': dtype('int64'),
         'MCP_ENB[0]': dtype('int64'),
         'MCP_ENB[1]': dtype('int64'),
         'MCP_ENB_1': dtype('int64'),
         'LV_ENB[0]': dtype('int64'),
         'LV_ENB[1]': dtype('int64'),
         'LV_ENB_1': dtype('int64'),
         'SYNC_CLK_DIS_2': dtype('int64'),
         'PAC_ENB_2': dtype('int64'),
         'MCP_ENB_2': dtype('int64'),
         'LV_ENB_2': dtype('int64'),
         'HVPS_CTRL': dtype('int64'),
         'PAC_VSET': dtype('float64'),
         'PAC_OCP': dtype('float64'),
         'MCP_VSET': dtype('float64'),
         'MCP_OCP': dtype('float64'),
         'STAR_SENSOR_OFFSET_ADJUST': dtype('float64'),
         'OSCOPE_CH1': dtype('int64'),
         'OSCOPE_CH0': dtype('int64'),
         'ADC_IF_STATUS_SS_UN': dtype('int64'),
         'ADC_IF_STATUS_SS_OV': dtype('int64'),
         'ADC_IF_STATUS_SS_FF': dtype('int64'),
         'ADC_IF_STATUS_SS_HF': dtype('int64'),
         'ADC_IF_STATUS_SS_FE': dtype('int64'),
         'ADC_IF_STATUS_PKT_RCVD': dtype('int64'),
         'ADC_IF_STATUS_TO_ERR': dtype('int64'),
         'ADC_IF_STATUS_ID_ERR': dtype('int64'),
         'ADC_IF_STATUS_FRM_ERR': dtype('int64'),
         'STAR': dtype('float64'),
         'TEMP1': dtype('float64'),
         'TEMP0': dtype('float64'),
         'V5P0_VM': dtype('float64'),
         'V3P3_VM': dtype('float64'),
         'V12P0_VM': dtype('float64'),
         'V12N0_VM': dtype('float64'),
         'LV_CM': dtype('float64'),
         'LV_VM': dtype('float64'),
         'LV_TEMP': dtype('float64'),
         'MCP_CM': dtype('float64'),
         'MCP_VM': dtype('float64'),
         'MCP_TEMP': dtype('float64'),
         'PAC_CM': dtype('float64'),
         'PAC_VM': dtype('float64'),
         'PAC_TEMP': dtype('float64'),
         'V5P0ANA_VM': dtype('float64'),
         'V2P5_VM': dtype('float64'),
         'STAR_MON': dtype('float64'),
         'PAC_VSET_MON': dtype('float64'),
         'PAC_OCP_MON': dtype('float64'),
         'MCP_VSET_MON': dtype('float64'),
         'MCP_OCP_MON': dtype('float64'),
         'REG_PEEK': dtype('int64'),
         }
         }