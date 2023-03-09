from sqlalchemy import create_engine,insert
from sqlalchemy import MetaData,event
from sqlalchemy.ext.declarative import declarative_base

def initEngine(hostname="127.0.0.1:3306",
                dbname="IMAPlo",
                uname="loDB_user",
                pwd="cM2MhRu0C"):
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                            .format(host=hostname, db=dbname, user=uname, pw=pwd))
    return(engine)

def drop_table(table_name, engine):
    Base = declarative_base()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        if table is not None:
            Base.metadata.drop_all(engine, [table], checkfirst=True)

def purgeDB(engine):
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
    engine.dispose()
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
    # Function to load raw data from 
    from datetime import datetime as dt
    from .load import get_all_dfils,load
    import time
    from sqlalchemy import text

    def uploader(dat,engine,to_table):
        print(dat.name)
        t = time.time()
        dat.to_sql(to_table, engine, index=True,if_exists = 'append')
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

    # load data file locations from rawdatabase
    dfils = get_all_dfils(dataloc,dtype)
    dfils['to_table'] = to_table
    # import ingestion log from server
    df_ingest = pd.read_sql(text('select * from ingest_log;'),conn)

    # if replace: 
    #     drop_table(to_table,engine)
    #     if 'ingest_log' in metadata.tables:
    #         table = metadata.tables['ingest_log']
    #         conn.execute(table.delete().where(table.c.to_table == to_table))
    #         con.commit()
    if ~replace:
        # drop files from ingest list if we are not replacing them 
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
    dfils.to_sql('ingest_log', engine, index=True,if_exists = 'append')
    engine.dispose()

