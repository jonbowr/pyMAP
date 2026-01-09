

import os



test_db = {
            'T001':{
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv1\EMv1_T001-ToF First Light Princeton',
                    'asrun':r'EMv1_ToF_FirstLight_PSPL_AsRun.xlsx',
                    'testTitle':'EMv1_T001-ToF_First_Light_Princeton',
                    'asrun_pages':['Global','ETU_tof','ETU_sensor','Princeton_SPL'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\csv',
                    'instrument': 'EMv1'
                    },
            'T002': {
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv1\EMv1_T002-ToF First Light UNHSPLAT',
                    'asrun':r'EMv1_UNHSPLAT_FirstLight-AsRun.xlsx',
                    'testTitle':'EMv1_T002-ToF_First_Light_UNHSPLAT',
                    'asrun_pages':['Global','M145_beam','M145_system','ETU_tof'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\csv',
                    'instrument': 'EMv1'
                    },
            'T003': {
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv1\EMv1_T003-ToF Cal Beam Test UNHSPLAT',
                    'asrun':'EMv1_ToFcal_Beam_Test_AsRun.xlsx',
                    'testTitle':'EMv1_T003-ToF_Cal_Beam_Test_UNHSPLAT',
                    'asrun_pages':['Global','M145_beam','M145_system','ETU_tof'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\csv',
                    'instrument': 'EMv1'
                    },
            'T004': {
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv1\EMv1_T004-ToF Cal Beam Test 2 UNHSPLAT',
                    'asrun':'EMv1_ToF_Cal_Beam_Test2_AsRun.xlsx',
                    'testTitle':'EMv1_ToF_Cal_Beam_Test2_UNHSPLAT',
                    'asrun_pages':['Global','M145_beam','M145_system','EM_tof'],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor\csv',
                    'instrument': 'EMv1'
                    },
            'T005': {
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv1\EMv1_T005_PSPL_ToFCal3',
                    'asrun':'EMV1_T005_PSPL_ToFCal3_AsRun.xlsx',
                    'testTitle':'EMV1_T005_PSPL_ToFCal3',
                    'asrun_pages':['Global','EM_tof','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor\csv',
                    'instrument': 'EMv1'
                    },
            'T006':{
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv2\EMV2_T006_PSPL_FirstLight',
                    'asrun':'EMv2_T006_PSPL_FirstLight_AsRun.xlsx',
                    'testTitle':'EMv2_T006_PSPL_FirstLight',
                    'asrun_pages':['Global','EM_tof','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor',
                    'instrument': 'EMv2'
                    },
            'T007':{
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv2\EMV2_rev2_T007_PSPL_FirstLight',
                    'asrun':'',
                    'testTitle':'EMv2_rev2_T007_PSPL_FirstLight',
                    'asrun_pages':[],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor',
                    'instrument': 'EMv2'
                    },
            'T011':{
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv2\EMv2c_T011_PSPL_FirstLight_20230424',
                    'asrun':'EMv2c_T011_PSPL_FirstLight_20230424_AsRun.xlsx',
                    'testTitle':'EMv2c_T011_PSPL_FirstLight_20230424',
                    'asrun_pages':['Global','EM_optics','EM_tof','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sensor\csv',
                    'eboxDB':r'',
                    'instrument': 'EMv2c'
                    },
            'T012':{
                    'testDB':r'C:\Users\Jonny Woof\Box\IMAP-Lo-box (1)\Science\Testing\IMAP_lo\EMv2\EMv2c_T012_PSPL_20230516',
                    'asrun':'EMv2c_T012_PSPL_20230515_AsRun.xlsx',
                    'testTitle':'EMv2c_T012_PSPL_20230516',
                    'asrun_pages':['Global','EM_optics','EM_tof','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sensor\csv',
                    'eboxDB':r'',
                    'instrument': 'EMv2c'
                    },
            'T101':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_FM_CAL\FMv1a_T101_PSPL_ToF_Cal',
                    'asrun':'FMv1a_T101_PSPL_ToF_Cal_AsRun.xlsx',
                    'testTitle':'FMv1a_T101_PSPL_ToF_Cal',
                    'asrun_pages':['Global','FM_tof','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor',
                    'instrument': 'FMv1a'
                    },
            'T102':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_FM_CAL\FMv2_T102_PSPL_PreCal1',
                    'asrun':'FMv2_T102_PSPL_PreCal1_AsRun.xlsx',
                    'testTitle':'FMv2_T102_PSPL_PreCal1',
                    'asrun_pages':['Global','FM_tof','FM_optics','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor',
                    'instrument': 'FMv2'
                    },
        #     'T103':{
        #             'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_FM_CAL\FMv3_T103_PSPL_PreCal2',
        #             'asrun':'FMv3_T103_PSPL_PreCal2_AsRun.xlsx',
        #             'testTitle':'FMv3_T103_PSPL_PreCal2',
        #             'asrun_pages':['Global','TOF','FM_optics','Princeton_PSPL'],
        #             'snifferDB':r'\Test Data\Sniffer',
        #             'eboxDB':r'\Test Data\Sensor',
        #             'instrument': 'FMv3'
        #             },
            'T104':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_FM_CAL\FMv3_T104_PSPL_PreCal2',
                    'asrun':'FMv3_T104_PSPL_PreCal2_AsRun.xlsx',
                    'testTitle':'FMv3_T104_PSPL_PreCal2',
                    'asrun_pages':['Global','TOF','FM_optics','Princeton_PSPL'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\Sensor',
                    'instrument': 'FMv3'
                    },
            'T105':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_FM_CAL\FMv3_T105_PSPL_FinalCal',
                    'asrun':'FMv3_T105_PSPL_FinalCal_AsRun.xlsx',
                    'testTitle':'FMv3_T105_PSPL_FinalCal',
                    'asrun_pages':['Global','TOF','FM_optics','Princeton_PSPL'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\Instrument Data',
                    'instrument': 'FMv3'
                    },
            'T106':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_FM_CAL\FMv3_T106_LANL_CrossCal',
                    'asrun':'FMv3_T106_LANL_CrossCal_AsRun_cew.xlsx',
                    'testTitle':'FMv3_T106_LANL_CrossCal',
                    'asrun_pages':['Global','TOF','FM_optics','LANL_beam'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\Instrument Data',
                    'instrument': 'FMv3'
                    },
            }


def get_asruns(instrument = ''):
    def get_runrs(x):
        from pyMAP.pyMAP.data import asRunr
        runtab = os.path.join(x['testDB'],x['asrun'])
        db = os.path.join(x['testDB'],'Test Data/')
        pages = x['asrun_pages']
                        
        return(asRunr(runtab,db,pages,instrument = 'imap_lo_fm'))

    from pandas import DataFrame
    test_df = DataFrame(test_db).T
    tests = test_df.loc[test_df['instrument'].str.contains(instrument)]
    tests['df'] = tests.apply(get_runrs,axis =1)
    return(tests)

def verify_asrun_pages(instrument='', verbose=True):
    """
    Verify that all pages listed in asrun_pages exist in the Excel files.
    
    Parameters:
    -----------
    instrument : str
        Filter by instrument name (default: '' for all instruments)
    verbose : bool
        If True, print detailed information for each test
    
    Returns:
    --------
    dict : Dictionary with test IDs as keys and verification results as values
    """
    from pandas import DataFrame, ExcelFile
    import os
    
    test_df = DataFrame(test_db).T
    if instrument:
        tests = test_df.loc[test_df['instrument'].str.contains(instrument)]
    else:
        tests = test_df
    
    results = {}
    all_valid = True
    
    for test_id, test_info in tests.iterrows():
        # Skip tests without AsRun files
        if not test_info['asrun']:
            if verbose:
                print(f"\n{test_id}: No AsRun file specified - SKIPPED")
            results[test_id] = {'status': 'skipped', 'reason': 'No AsRun file'}
            continue
        
        file_path = os.path.join(test_info['testDB'], test_info['asrun'])
        
        # Check if file exists
        if not os.path.exists(file_path):
            if verbose:
                print(f"\n{test_id}: AsRun file NOT FOUND")
                print(f"  Path: {file_path}")
            results[test_id] = {'status': 'error', 'reason': 'File not found', 'path': file_path}
            all_valid = False
            continue
        
        try:
            # Get actual sheet names from Excel file
            xl_file = ExcelFile(file_path)
            actual_sheets = xl_file.sheet_names
            expected_sheets = test_info['asrun_pages']
            
            # Find missing and extra sheets
            missing_sheets = [sheet for sheet in expected_sheets if sheet not in actual_sheets]
            extra_sheets = [sheet for sheet in actual_sheets if sheet not in expected_sheets]
            
            if missing_sheets:
                all_valid = False
                status = 'FAILED'
            else:
                status = 'PASSED'
            
            results[test_id] = {
                'status': status,
                'expected': expected_sheets,
                'actual': actual_sheets,
                'missing': missing_sheets,
                'extra': extra_sheets
            }
            
            if verbose:
                print(f"\n{test_id} ({test_info['testTitle']}): {status}")
                print(f"  Expected pages: {expected_sheets}")
                
                if missing_sheets:
                    print(f"  ❌ MISSING pages: {missing_sheets}")
                else:
                    print(f"  ✓ All expected pages found")
                
                if extra_sheets:
                    print(f"  ℹ️  Additional pages in file: {extra_sheets}")
        
        except Exception as e:
            if verbose:
                print(f"\n{test_id}: ERROR reading file")
                print(f"  Error: {str(e)}")
            results[test_id] = {'status': 'error', 'reason': str(e), 'path': file_path}
            all_valid = False
    
    if verbose:
        print("\n" + "="*80)
        if all_valid:
            print("✓ All verifications PASSED")
        else:
            print("❌ Some verifications FAILED - check details above")
        print("="*80)
    
    return results
