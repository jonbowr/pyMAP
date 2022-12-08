IBEX-Lo ETU Direct Event Data
-----
Ryan Murphy
EoS Space Science Center, UNH
rjm1068@usnh.edu
9/22/2021
-----

Data taken during the ETU tests is created using the GSE and exported into .txt files using the GSEOS.
The exporting process will be described in a separate document.

##PHA: The following items are exported
- EU("TOF_DE_.sample.TOF0") #
- TOF_DE_sample.ValidStart0 # 0 or 1 if TOF0 saw valid start signal
- TOF_DE_sample.ValidStop0 # 0 or 1 if TOF0 saw valid stop signal
- TOF_DE_sample.ValidTOF0 # 1 if ValidStart0 and ValidStop0 are both 1, 0 otherwise
- EU("TOF_DE_sample.TOF1") #
- TOF_DE_sample.ValidStart1 # 0 or 1 if TOF1 saw valid start signal
- TOF_DE_sample.ValidStop1 # 0 or 1 if TOF1 saw valid stop signal
- TOF_DE_sample.ValidTOF1 # 1 if ValidStart1 and ValidStop1 are both 1, 0 otherwise
- EU("TOF_DE_sample.TOF2") #
- TOF_DE_sample.ValidStart2 # 0 or 1 if TOF2 saw valid start signal
- TOF_DE_sample.ValidStop2 # 0 or 1 if TOF2 saw valid stop signal
- TOF_DE_sample.ValidTOF2 # 1 if ValidStart2 and ValidStop2 are both 1, 0 otherwise
- EU("TOF_DE_sample.TOF3") #
- TOF_DE_sample.ValidStart3 # 0 or 1 if TOF3 saw valid start signal
- TOF_DE_sample.ValidStop3 # 0 or 1 if TOF3 saw valid stop signal
- TOF_DE_sample.ValidTOF3 # 1 if ValidStart3 and ValidStop3 are both 1, 0 otherwise
- EU("TOF_IF.pac_vm") # Post acceleration voltage
- EU("TOF_HK.Vmon_MCP") # MCP monitor voltage
- RecBlockStatus.Time # Engineer time/ computer time
- TOF_HK.RateSilver # Rate of silver events
- TOF_HK.RateGold # Rate of gold events
- EU("TOF_IF.mcp_vm") # MCP voltage

