

import os



test_db = {
            'T001':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv1\EMv1_T001-ToF First Light Princeton',
                    'asrun':r'EMv1_ToF_FirstLight_PSPL_AsRun.xlsx',
                    'testTitle':'EMv1_T001-ToF_First_Light_Princeton',
                    'asrun_pages':['Global','ETU_tof','ETU_sensor','Princeton_SPL'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\csv',
                    'instrument': 'EMv1'
                    },
            'T002': {
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv1\EMv1_T002-ToF First Light UNHSPLAT',
                    'asrun':r'EMv1_UNHSPLAT_FirstLight-AsRun.xlsx',
                    'testTitle':'EMv1_T002-ToF_First_Light_UNHSPLAT',
                    'asrun_pages':['Global','M145_beam','M145_system','ETU_tof'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\csv',
                    'instrument': 'EMv1'
                    },
            'T003': {
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv1\EMv1_T003-ToF Cal Beam Test UNHSPLAT',
                    'asrun':'EMv1_ToFcal_Beam_Test_AsRun.xlsx',
                    'testTitle':'EMv1_T003-ToF_Cal_Beam_Test_UNHSPLAT',
                    'asrun_pages':['Global','M145_beam','M145_system','ETU_tof'],
                    'snifferDB':'',
                    'eboxDB':r'\Test Data\csv',
                    'instrument': 'EMv1'
                    },
            'T004': {
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv1\EMv1_T004-ToF Cal Beam Test 2 UNHSPLAT',
                    'asrun':'EMv1_ToF_Cal_Beam_Test2_AsRun.xlsx',
                    'testTitle':'EMv1_ToF_Cal_Beam_Test2_UNHSPLAT',
                    'asrun_pages':['Global','M145_beam','M145_system','EM_tof'],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor\csv',
                    'instrument': 'EMv1'
                    },
            'T005': {
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv1\EMv1_T005_PSPL_ToFCal3',
                    'asrun':'EMV1_T005_PSPL_ToFCal3_AsRun.xlsx',
                    'testTitle':'EMV1_T005_PSPL_ToFCal3',
                    'asrun_pages':['Global','EM_tof','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor\csv',
                    'instrument': 'EMv1'
                    },
            'T006':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv2\EMV2_T006_PSPL_FirstLight',
                    'asrun':'EMv2_T006_PSPL_FirstLight_AsRun.xlsx',
                    'testTitle':'EMv2_T006_PSPL_FirstLight',
                    'asrun_pages':['Global','EM_tof','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor',
                    'instrument': 'EMv2'
                    },
            'T007':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv2\EMV2_rev2_T007_PSPL_FirstLight',
                    'asrun':'',
                    'testTitle':'EMv2_rev2_T007_PSPL_FirstLight',
                    'asrun_pages':[],
                    'snifferDB':r'\Test Data\Sniffer',
                    'eboxDB':r'\Test Data\Sensor',
                    'instrument': 'EMv2'
                    },
            'T011':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv2\EMv2c_T011_PSPL_FirstLight_20230424',
                    'asrun':'EMv2c_T011_PSPL_FirstLight_20230424_AsRun.xlsx',
                    'testTitle':'EMv2c_T011_PSPL_FirstLight_20230424',
                    'asrun_pages':['Global','EM_optics','EM_tof','Princeton_PSPL'],
                    'snifferDB':r'\Test Data\Sensor\csv',
                    'eboxDB':r'',
                    'instrument': 'EMv2c'
                    },
            'T012':{
                    'testDB':r'C:\Users\Jonny Woof\OneDrive - USNH\IMAP-Lo_Cal_Science\IMAP-Lo_Cal_DB\IMAP-Lo_EM_CAL\EMv2\EMv2c_T012_PSPL_20230516',
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


def find_redundant_keys(tests, similarity_threshold=0.8, verbose=True, interactive_resolve=False):
    """
    Find potentially redundant column keys across all test DataFrames.
    Identifies keys that are similar but not identical between tables.
    
    Parameters:
    -----------
    tests : DataFrame
        Tests DataFrame with 'df' column containing asRunr objects
    similarity_threshold : float
        Threshold for string similarity (0-1), default 0.8
    verbose : bool
        If True, print detailed information
    interactive_resolve : bool
        If True, prompt user to resolve redundancies by renaming keys
    
    Returns:
    --------
    dict : Dictionary with similar key groups and their occurrences
    """
    from difflib import SequenceMatcher
    from collections import defaultdict
    import pandas as pd
    
    # Collect all unique keys from all DataFrames
    all_keys = {}  # {key: [(test_id, sheet_name), ...]}
    
    for test_id, test_row in tests.iterrows():
        if 'df' not in test_row or test_row['df'] is None:
            continue
            
        try:
            # Get the asRunr object
            asrun_obj = test_row['df']
            
            # Access the df attribute which contains the DataFrame
            if hasattr(asrun_obj, 'df') and asrun_obj.df is not None:
                df = asrun_obj.df
                for col in df.columns:
                    if col not in all_keys:
                        all_keys[col] = []
                    all_keys[col].append(test_id)
        except Exception as e:
            if verbose:
                print(f"Warning: Could not extract keys from {test_id}: {e}")
            continue
    
    if not all_keys:
        if verbose:
            print("No keys found in test DataFrames")
        return {}
    
    # Find similar but not identical keys
    keys_list = list(all_keys.keys())
    similar_groups = []
    processed = set()
    
    def string_similarity(a, b):
        """Calculate similarity ratio between two strings"""
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()
    
    for i, key1 in enumerate(keys_list):
        if key1 in processed:
            continue
            
        similar = [key1]
        for key2 in keys_list[i+1:]:
            if key2 in processed:
                continue
                
            # Check if keys are similar but not identical
            if key1 != key2:
                similarity = string_similarity(key1, key2)
                if similarity >= similarity_threshold:
                    similar.append(key2)
                    processed.add(key2)
        
        if len(similar) > 1:
            similar_groups.append(similar)
            processed.add(key1)
    
    # Build results
    results = {}
    for group in similar_groups:
        group_info = {}
        for key in group:
            group_info[key] = {
                'test_ids': all_keys[key],
                'count': len(all_keys[key])
            }
        results[f"Group_{len(results)+1}"] = group_info
    
    # Print results
    if verbose:
        print("\n" + "="*80)
        print("POTENTIALLY REDUNDANT KEYS ANALYSIS")
        print("="*80)
        
        if not results:
            print("\n✓ No redundant keys found")
        else:
            print(f"\nFound {len(results)} groups of similar keys:\n")
            
            for group_name, group_data in results.items():
                print(f"\n{group_name}:")
                for key, info in group_data.items():
                    print(f"  '{key}'")
                    print(f"    Used in tests: {info['test_ids']} ({info['count']} tests)")
                
                # Calculate similarity scores within group
                keys_in_group = list(group_data.keys())
                if len(keys_in_group) > 1:
                    print(f"    Similarity scores:")
                    for i in range(len(keys_in_group)-1):
                        sim = string_similarity(keys_in_group[i], keys_in_group[i+1])
                        print(f"      '{keys_in_group[i]}' ↔ '{keys_in_group[i+1]}': {sim:.2%}")
        
        print("\n" + "="*80)
    
    # Interactive resolution
    if interactive_resolve and results:
        print("\n" + "="*80)
        print("INTERACTIVE RESOLUTION")
        print("="*80)
        
        rename_map = {}  # {old_key: new_key}
        
        for group_name, group_data in results.items():
            keys_in_group = list(group_data.keys())
            print(f"\n{group_name}: Found {len(keys_in_group)} similar keys")
            for idx, key in enumerate(keys_in_group):
                print(f"  [{idx}] '{key}' (used in {group_data[key]['count']} tests)")
            
            print(f"\nOptions:")
            print(f"  [0-{len(keys_in_group)-1}]: Choose a key as canonical name")
            print(f"  [c]: Enter custom canonical name")
            print(f"  [s]: Skip this group")
            
            choice = input(f"\nYour choice for {group_name}: ").strip().lower()
            
            if choice == 's':
                print("  Skipped.")
                continue
            elif choice == 'c':
                canonical = input("  Enter canonical key name: ").strip()
                if not canonical:
                    print("  Invalid name. Skipped.")
                    continue
            else:
                try:
                    idx = int(choice)
                    if 0 <= idx < len(keys_in_group):
                        canonical = keys_in_group[idx]
                    else:
                        print(f"  Invalid index. Skipped.")
                        continue
                except ValueError:
                    print(f"  Invalid choice. Skipped.")
                    continue
            
            # Add to rename map
            for key in keys_in_group:
                if key != canonical:
                    rename_map[key] = canonical
            
            print(f"  ✓ Will rename {len(keys_in_group)-1} keys to '{canonical}'")
        
        # Apply renaming to all test DataFrames
        if rename_map:
            print(f"\n" + "="*80)
            print(f"APPLYING RENAMING ({len(rename_map)} keys to rename)")
            print("="*80)
            
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for test_id, test_row in tests.iterrows():
                if 'df' not in test_row or test_row['df'] is None:
                    continue
                    
                try:
                    asrun_obj = test_row['df']
                    if hasattr(asrun_obj, 'df') and asrun_obj.df is not None:
                        df = asrun_obj.df
                        cols_to_rename = {old: new for old, new in rename_map.items() if old in df.columns}
                        
                        if cols_to_rename:
                            df.rename(columns=cols_to_rename, inplace=True)
                            
                            # Record changes to asRunr.info
                            if hasattr(asrun_obj, 'info'):
                                for old_key, new_key in cols_to_rename.items():
                                    change_record = {
                                        'timestamp': timestamp,
                                        'action': 'key_rename',
                                        'test_id': test_id,
                                        'old_key': old_key,
                                        'new_key': new_key,
                                        'function': 'find_redundant_keys'
                                    }
                                    asrun_obj.info.append(change_record)
                            
                            print(f"  {test_id}: Renamed {len(cols_to_rename)} columns")
                except Exception as e:
                    print(f"  {test_id}: ERROR - {e}")
            
            print("\n✓ Renaming complete!")
            print(f"\nChanges recorded to asRunr.info for affected tests.")
        else:
            print("\nNo renaming performed.")
    
    return results


def compare_all_keys(tests, verbose=True):
    """
    Compare all column keys across test DataFrames and show statistics.
    
    Parameters:
    -----------
    tests : DataFrame
        Tests DataFrame with 'df' column containing asRunr objects
    verbose : bool
        If True, print detailed information
    
    Returns:
    --------
    DataFrame : Summary of all keys and their usage across tests
    """
    import pandas as pd
    from collections import Counter
    
    # Collect all keys with test information
    key_usage = {}  # {key: [test_ids]}
    
    for test_id, test_row in tests.iterrows():
        if 'df' not in test_row or test_row['df'] is None:
            continue
            
        try:
            asrun_obj = test_row['df']
            if hasattr(asrun_obj, 'df') and asrun_obj.df is not None:
                df = asrun_obj.df
                for col in df.columns:
                    if col not in key_usage:
                        key_usage[col] = []
                    key_usage[col].append(test_id)
        except Exception as e:
            if verbose:
                print(f"Warning: Could not extract keys from {test_id}: {e}")
            continue
    
    if not key_usage:
        if verbose:
            print("No keys found in test DataFrames")
        return pd.DataFrame()
    
    # Create summary DataFrame
    summary_data = []
    for key, test_ids in sorted(key_usage.items()):
        summary_data.append({
            'Key': key,
            'Used_In_Tests': ', '.join(test_ids),
            'Test_Count': len(test_ids),
            'Unique_Tests': len(set(test_ids))
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    if verbose:
        print("\n" + "="*80)
        print("ALL KEYS SUMMARY")
        print("="*80)
        print(f"\nTotal unique keys: {len(key_usage)}")
        print(f"Total tests analyzed: {len(tests)}")
        print("\nKey usage statistics:")
        print(summary_df.to_string(index=False))
        print("\n" + "="*80)
    
    return summary_df
