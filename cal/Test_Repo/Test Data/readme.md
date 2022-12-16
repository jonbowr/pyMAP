IMAP-Lo ETU Background Thermal Vacuum Test Data
-----
Ryan Murphy
EoS Space Science Center, UNH
rjm1068@usnh.edu
9/22/2021
-----

Data taken during the ETU tests is created using the GSE and exported into .txt files using the GSEOS.
The exporting process will be described in a separate document.

1.) TC Data

2.) txt

Broken up into PHA and rate data depending on what was exported from the corresponding .rec file:

###PHA: The following items are exported
-EU("TOF_DE_.sample.TOF0") #
-TOF_DE_sample.ValidStart0 # 0 or 1 if TOF0 saw valid start signal
-TOF_DE_sample.ValidStop0 # 0 or 1 if TOF0 saw valid stop signal
-TOF_DE_sample.ValidTOF0 # 1 if ValidStart0 and ValidStop0 are both 1, 0 otherwise
-EU("TOF_DE_sample.TOF1") #
-TOF_DE_sample.ValidStart1 # 0 or 1 if TOF1 saw valid start signal
-TOF_DE_sample.ValidStop1 # 0 or 1 if TOF1 saw valid stop signal
-TOF_DE_sample.ValidTOF1 # 1 if ValidStart1 and ValidStop1 are both 1, 0 otherwise
-EU("TOF_DE_sample.TOF2") #
-TOF_DE_sample.ValidStart2 # 0 or 1 if TOF2 saw valid start signal
-TOF_DE_sample.ValidStop2 # 0 or 1 if TOF2 saw valid stop signal
-TOF_DE_sample.ValidTOF2 # 1 if ValidStart2 and ValidStop2 are both 1, 0 otherwise
-EU("TOF_DE_sample.TOF3") #
-TOF_DE_sample.ValidStart3 # 0 or 1 if TOF3 saw valid start signal
-TOF_DE_sample.ValidStop3 # 0 or 1 if TOF3 saw valid stop signal
-TOF_DE_sample.ValidTOF3 # 1 if ValidStart3 and ValidStop3 are both 1, 0 otherwise
-EU("TOF_IF.pac_vm") # Post acceleration voltage
-EU("TOF_HK.Vmon_MCP") # MCP monitor voltage
-RecBlockStatus.Time # Engineer time/ computer time
-TOF_HK.RateSilver # Rate of silver events
-TOF_HK.RateGold # Rate of gold events
-EU("TOF_IF.mcp_vm") # MCP voltage

###Rate: the following items are exported
-TOF_HK.Rate_Start_A #
-TOF_HK.Rate_Start_C #
-TOF_HK.Rate_Pos_B0 #
-TOF_HK.Rate_Pos_B3 #
-TOF_HK.Rate_TOF_0_AB #
-TOF_HK.Rate_TOF_1_CB #
-TOF_HK.Rate_TOF_2_AC #
-TOF_HK.Rate_TOF_3_Pos_B0B3 #
-EU("TOF_HK.Vmon_MCP") # MCP monitor voltage
-EU("TOF_HK.Imon_MCP") # MCP monitor current ???
-TOF_IF.MCP_VSET #
-EU("TOF_IF.MCP_VSET") #
-TOF_HK.RateSilver #
-TOF_HK.RateGold #
-EU("TOF_IF.PAC_VSET") #
-TOF_IF.PAC_VSET #
-TOF_IF.pac_vm #
-TOF_IF.mcp_vm #
-EU("TOF_IF.ifb_temp0") #
-EU("TOF_IF.ifb_temp1") #
-EU("TOF_IF.lv_temp") #
-EU("TOF_IF.mcp_temp") #
-EU("TOF_IF.pac_temp") #
-EU("TOF_HK.Imon") #
-EU("TOF_HK.Imon5") #
-RecStatTime.year # Year
-RecStatTime.month # Month
-RecStatTime.day # Day
-RecStatTime.hour # Hour
-RecStatTime.minute # Minute
-RecStatTime.second # Second
-RecBlockStatus.Time # Engineer time/ computer time

3.) recfils

Data recording files created by the GSE. When the recorder is started, a new .rec file will be generated
with the corresponding date and time using the computer's clock.

Example file name:

IBEX-Lo_ETU_EGSE_yyyymmdd_hhmmss.rec