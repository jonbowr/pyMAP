from sqlalchemy import create_engine,insert
from sqlalchemy import MetaData,event
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

def ssh_bind(ssh_host = "jill.sr.unh.edu"):
    # Function to initialize and setup ssh tunnel with port forwarding
    from sshtunnel import SSHTunnelForwarder
    from getpass import getpass
    server = SSHTunnelForwarder(
        ssh_host, 
        ssh_username=input('Jill Username: '),
        ssh_password = getpass(),
        remote_bind_address=('127.0.0.1',3306),
        local_bind_address=('127.0.0.1',3306)
        )
    server.start()
    return(server)

def initEngine(hostname="127.0.0.1:3306",
                dbname="IMAPlo",
                uname="loDB_user",
                pwd="cM2MhRu0C"):
    if uname == 'loDB_admin':
        from getpass import getpass
        pwd = getpass()
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                            .format(host=hostname, db=dbname, user=uname, pw=pwd),
                            pool_pre_ping=True,
                            pool_size=10,
                            max_overflow=20
                            )
    return(engine)

def drop_table(table_name, engine):
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        if table is not None:
            Base.metadata.drop_all(engine, [table], checkfirst=True)

def add_column(engine, table, column, col_type='TEXT'):
    """
    Add a column to a table if it doesn't already exist.
    
    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        Database engine connection
    table : str
        Name of the table to add column to
    column : str
        Name of the column to add
    col_type : str, optional
        SQL data type for the column (default: 'TEXT')
        Common types: 'INT', 'DOUBLE', 'TEXT', 'DATETIME', 'BOOLEAN'
    
    Returns
    -------
    bool
        True if column was added, False if it already existed
    """
    from sqlalchemy import inspect, text
    
    # Validate column type
    valid_types = ['INT', 'BIGINT', 'SMALLINT', 'TINYINT',
                   'FLOAT', 'DOUBLE', 'DECIMAL', 'NUMERIC',
                   'CHAR', 'VARCHAR', 'TEXT', 'TINYTEXT', 'MEDIUMTEXT', 'LONGTEXT',
                   'DATE', 'DATETIME', 'TIMESTAMP', 'TIME', 'YEAR',
                   'BOOLEAN', 'BOOL', 'BIT',
                   'BLOB', 'TINYBLOB', 'MEDIUMBLOB', 'LONGBLOB',
                   'BINARY', 'VARBINARY',
                   'ENUM', 'SET', 'JSON']
    
    # Extract base type (e.g., VARCHAR(255) -> VARCHAR)
    base_type = col_type.split('(')[0].strip().upper()
    
    if base_type not in valid_types:
        print(f"Invalid column type '{col_type}'. Valid types: {', '.join(valid_types)}")
        return False
    
    inspector = inspect(engine)
    
    # Check if table exists
    if table not in inspector.get_table_names():
        print(f"Table '{table}' does not exist")
        return False
    
    # Get existing columns
    existing_cols = {c['name'] for c in inspector.get_columns(table)}
    
    # Check if column already exists
    if column in existing_cols:
        print(f"Column '{column}' already exists in table '{table}'")
        return False
    
    # Add the column
    try:
        with engine.begin() as conn:
            conn.execute(text(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {col_type}"))
        print(f"Added column '{column}' ({col_type}) to table '{table}'")
        return True
    except Exception as e:
        print(f"Error adding column '{column}' to table '{table}': {e}")
        return False

def purgeDB(engine):
    # totally wipes data base lean of all tables
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    checker = input('Are you sure you want to purge the whole DB? [y/n]')
    if checker.lower() == 'y':
        for table_name in metadata.tables.keys():
            table = metadata.tables[table_name]
            if table is not None:
                Base.metadata.drop_all(engine, [table], checkfirst=True)

def get_table(table_name, engine):
    # returns sqlalchemy table struct taken from engine
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return(metadata.tables[table_name])

def importSQL(query="SELECT * FROM ILO_IFB WHERE dateTime BETWEEN '2022-12-22 16:09:00' AND '2023-01-15 16:20:00';"):
    import pandas as pd
    from sqlalchemy import text
    # Credentials to database connection
    engine = initEngine()
    conn = engine.connect()
    df = pd.read_sql(text(query),conn)#.set_index('dateTime')
    try:
        engine.dispose()
    except Exception:
        pass
    return(df)

def sqlCMD(query):
    from sqlalchemy import text
    # Credentials to database connection
    engine = initEngine()
    conn = engine.connect()
    df = pd.read_sql(text(query),conn)#.set_index('dateTime')
    engine.dispose()

def ingest_data(dataloc,dtype = 'ILO_IFB',to_table = 'test',
                        replace = False,bulk_combine = True,
                        admin_pwd = '',tag = ''):
    # Function to load raw data of a provided type and ingest it to a given table on jill


    from datetime import datetime as dt
    from .load import get_all_dfils,load
    import time
    from sqlalchemy import text
    import pandas as pd
    import numpy as np

    def uploader(dat,engine,to_table):
        print(dat.name)
        t = time.time()
        dat.to_sql(to_table, engine, index=True, if_exists='append',
                   method='multi', chunksize=5000)
        t_end = time.time()-t
        print('%d rows,%d cols, %.0f S: %.2f [R/S], %.2f [Elm/S]'%(len(dat),dat.shape[1],
                                                                     t_end,
                                                                     len(dat)/t_end,
                                                                      len(dat)*dat.shape[1]/t_end))

    print('Processing %s data from %s to add to %s'%(dtype,dataloc,to_table))
    if admin_pwd =='':
        admin_pwd = input('Input admin password')

    # connect to engine
    engine = initEngine(uname = 'loDB_admin',pwd = admin_pwd)
    # initialize connection
    metadata = MetaData()
    metadata.reflect(bind=engine)
    conn = engine.connect()

    # load data file locations from rawdatabase
    dfils = get_all_dfils(dataloc,dtype).reset_index()
    dfils['to_table'] = to_table
    # import ingestion log from server

    if not replace:
        if 'ingest_log' in metadata.tables:
            # drop files from ingest list if we are not replacing them 
            df_ingest = pd.read_sql(text('select * from ingest_log;'),conn)
            dfils = dfils.iloc[~np.in1d(dfils['name'].values,df_ingest['name'].values)]

    if bulk_combine:
        # bulk load and combine all data, should consider changing this to not load 
        #   files we arent ingesting 
        df = load(dataloc,dtype = dtype,
                          load_params = {'reduce':True})
        df['tag'] = tag

        #Drop all data from DB associated with the files being uploaded
        #       if we are replacing datt,
        if replace:
            if to_table in metadata.tables:
                table = metadata.tables[to_table]
                table_log = metadata.tables['ingest_log']
                for fRAW in np.unique(df['fRAW'].values):
                    conn.execute(table.delete().where(table.c.fRAW == fRAW))
                    con.commit()
                    conn.execute(table_log.delete().where(table.c.name == fRAW))
                    con.commit()
        else:
            # if replace is false, drop values to upload if the file has already been uploaded
            df = df.iloc[~np.in1d(df['fRAW'].values,df_ingest['name'].values)]
        print('=====================================')
        print('Bulk uploading %s data to table %s on Jill'%(dtype,to_table))
        df.name = tag
        uploader(df,engine,to_table)
    else:
        def load_up(lab):
            if replace:
                if to_table in metadata.tables:
                    table = metadata.tables[to_table]
                    table_log = metadata.tables['ingest_log']
                    conn.execute(table.delete().where(table.c.fRAW == lab))
                    con.commit()
                    conn.execute(table_log.delete().where(table.c.name == lab))
                    con.commit()
                    print('Scrubbing %s data from %s on Jill'%(fil,to_table))
            df = load(lab,dtype = dtype)
            df['tag'] = tag
            print('=====================================')
            print('Uploading %s data to table %s on Jill'%(dtype,to_table))
            t = time.time()
            df.name = tag
            uploader(df,engine,to_table)
        dfils['file_path'].apply(load_up)
    dfils['ingest_time'] = dt.now() 
    dfils.to_sql('ingest_log', engine, index=False, if_exists='append',
                 method='multi', chunksize=1000)
    try:
        engine.dispose()
    except Exception:
        pass

def ingest_asRunDataFiles(dfils,prop_tags = [],
                          replace = False,
                          admin_pwd = '',
                          purge = False,
                          add_missing_cols = True):
    """
    Ingest as-run test data files to the Jill SQL database.
    
    This function processes a DataFrame of file metadata, loads each file's data,
    and uploads it to the specified SQL tables. It includes intelligent features like
    duplicate detection, column schema management, and comprehensive logging.
    
    Parameters
    ----------
    dfils : pandas.DataFrame
        DataFrame containing file metadata with required columns:
        - 'name': Unique file identifier
        - 'file_path': Full path to the data file
        - 'dtype': Data type identifier for loading
        - 'inst_loader': Instrument loader library name
        - 'to_table': Target SQL table name
        Additional columns are preserved and can be logged via prop_tags
    prop_tags : list, optional
        List of column names from dfils to propagate as additional columns 
        in the uploaded data tables (default: [])
    replace : bool, optional
        If True, deletes existing entries from SQL tables before uploading.
        If False, skips files already present in ingest_log (default: False)
    admin_pwd : str, optional
        Admin password for database connection. If empty, prompts user (default: '')
    purge : bool, optional
        If True, prompts to drop all target tables before ingestion.
        Use with caution - this deletes all data in target tables (default: False)
    add_missing_cols : bool, optional
        If True, automatically adds missing columns to existing SQL tables.
        If False, filters DataFrame to only include existing columns (default: True)
    
    Returns
    -------
    None
        Updates ingest_log table with results. Sets dfils['pass_fail'] to True/False
        for each file based on upload success.
    
    Notes
    -----
    - Uses connection pooling (pool_size=10, max_overflow=20) for performance
    - Batch uploads with method='multi', chunksize=5000 for data
    - Automatically checks ingest_log to avoid duplicate uploads
    - Logs all ingestion attempts with timestamps and pass/fail status
    - Prints progress and performance metrics (rows/sec, elements/sec)
    
    Examples
    --------
    >>> # Basic usage - upload new files
    >>> dfils = find_data(source='path/to/data', dtype='System')
    >>> ingest_asRunDataFiles(dfils, admin_pwd='password')
    
    >>> # Replace existing data with propagated tags
    >>> ingest_asRunDataFiles(dfils, prop_tags=['run_tag', 'test_phase'],
    ...                       replace=True, admin_pwd='password')
    
    >>> # Purge and rebuild tables
    >>> ingest_asRunDataFiles(dfils, purge=True, admin_pwd='password')
    """
    # Function to load raw data of a provided type and ingest it to a given table on jill


    from datetime import datetime as dt
    from pyMAP.pyMAP.data.load import load
    import time
    from sqlalchemy import text
    import pandas as pd
    import numpy as np

    def uploader(dat,engine,to_table,add_cols=True):
        # print(dat.name)
        from sqlalchemy import inspect, text, Integer, Float, String, DateTime, Boolean
        
        # Check if table exists and get existing columns
        inspector = inspect(engine)
        if to_table in inspector.get_table_names():
            existing_cols = {c['name']: c for c in inspector.get_columns(to_table)}
            df_cols = set(dat.columns) | {dat.index.name} if dat.index.name else set(dat.columns)
            missing_cols = df_cols - existing_cols.keys()
            
            # Add missing columns to the table or filter DataFrame
            if missing_cols:
                if add_cols:
                    print(f'Adding {len(missing_cols)} missing columns to {to_table}: {missing_cols}')
                    for col in missing_cols:
                        # Infer SQL type from DataFrame dtype
                        if col == dat.index.name:
                            dtype = dat.index.dtype
                        else:
                            dtype = dat[col].dtype
                        
                        if 'int' in str(dtype):
                            sql_type = 'INT'
                        elif 'float' in str(dtype):
                            sql_type = 'DOUBLE'
                        elif 'datetime' in str(dtype):
                            sql_type = 'DATETIME'
                        elif 'bool' in str(dtype):
                            sql_type = 'BOOLEAN'
                        else:
                            sql_type = 'TEXT'
                        
                        add_column(engine, to_table, col, sql_type)
                else:
                    print(f'Ignoring {len(missing_cols)} missing columns: {missing_cols}')
                    # Filter DataFrame to only include existing columns
                    keep_cols = [col for col in dat.columns if col in existing_cols.keys()]
                    dat = dat[keep_cols]
        
        t = time.time()
        dat.to_sql(to_table, engine, index=True, if_exists='append', 
                   method='multi', chunksize=5000)
        t_end = time.time()-t
        print('%d rows,%d cols, %.0f S: %.2f [R/S], %.2f [Elm/S]'%(len(dat),dat.shape[1],
                                                                     t_end,
                                                                     len(dat)/t_end,
                                                                      len(dat)*dat.shape[1]/t_end))

    
    if admin_pwd =='':
        admin_pwd = input('Input admin password')

    # connect to engine
    engine = initEngine(uname = 'loDB_admin',pwd = admin_pwd)
    # initialize connection
    metadata = MetaData()
    metadata.reflect(bind=engine)
    conn = engine.connect()

    # import ingestion log from server and filter files
    if 'ingest_log' in metadata.tables:
        df_ingest = pd.read_sql(text('select * from ingest_log;'),conn)
        
        if not replace:        
            already_uploaded = np.in1d(dfils['name'].values, df_ingest['name'].values)
            print(f"Skipping {already_uploaded.sum()} files already in ingest_log")
            dfils = dfils.iloc[~already_uploaded]
        else:
            already_uploaded = np.in1d(dfils['name'].values, df_ingest['name'].values)
            print(f"Replacing {already_uploaded.sum()} files already in ingest_log")
    else:
        print("No ingest_log table found - all files will be uploaded")
        df_ingest = None
    
    if len(dfils) == 0:
        print("No files to process after filtering")
        try:
            engine.dispose()
        except Exception:
            pass
        return

    
    def load_up(fil_line):
        try:
            lab = fil_line['name']
            floc = fil_line['file_path']
            data_dtype = fil_line['dtype']
            inst_load_lib = fil_line['inst_loader']
            to_table = fil_line['to_table']

            if replace:
                if 'ingest_log' in metadata.tables:
                    table_log = metadata.tables['ingest_log']
                    conn.execute(table_log.delete().where(table_log.c.name == lab))
                    print('Scrubbing %s from ingest_log on Jill'%(lab))
                
                if to_table in metadata.tables:
                    table = metadata.tables[to_table]
                    conn.execute(table.delete().where(table.c.name == lab))
                    print('Scrubbing %s data from %s on Jill'%(lab,to_table))

            print('Processing %s data from %s to add to %s'%(data_dtype,lab,to_table))
            df = load(floc,dtype = data_dtype,instrument = inst_load_lib)
            
            df['name'] = lab
            for tag in prop_tags:
                df[tag] = fil_line[tag]
            print('=======')
            print('Uploading %s data to table %s on Jill'%(data_dtype,to_table))
            t = time.time()
            df.name = lab
            uploader(df,engine,to_table,add_cols=add_missing_cols)
            fil_line['pass_fail'] = True
        except:
            fil_line['pass_fail'] = False
            Warning('Failed to process file: %s' % fil_line['name'])
        
        try:
            # Write to ingest_log - only include columns that exist in ingest_log
            fil_line_copy = fil_line.copy()
            fil_line_copy['ingest_time'] = dt.now()
            if df_ingest is not None:
                # Filter to only columns that exist in ingest_log
                log_cols = [k for k in df_ingest.keys() if k in fil_line_copy.index]
                fil_line_to_log = fil_line_copy[log_cols].to_frame().T
            else:
                # First upload, write all columns
                fil_line_to_log = fil_line_copy.to_frame().T
            
            fil_line_to_log.to_sql('ingest_log', engine, index=False, if_exists='append',
                                method='multi', chunksize=1000)
            print('=====================================')
        except:
            Warning('Failed to Write to ingest_log for file: %s' % fil_line['name'])

    if purge:
        print('Purging tables %s' % dfils['to_table'].unique())
        res = input('y to continue')
        if res.lower() != 'y':
            print('Purge cancelled.')
            return
        else:
            for tab in dfils['to_table'].unique():
                drop_table(tab,engine)
            
            # Refresh metadata after dropping tables
            metadata.clear()
            metadata.reflect(bind=engine)
    dfils.apply(load_up, axis=1)
    
    try:
        engine.dispose()
    except Exception:
        pass