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


def ingest_data(dataloc,
                    dtype = 'ILO_IFB',
                    to_table = 'test',
                    replace = False,
                    bulk_combine = True,
                    admin_pwd = '',
                    tag = ''
                                    ):
    from datetime import datetime as dt
    from .load import get_all_dfils,load
    import time

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


    engine = initEngine(uname = 'loDB_admin',pwd = admin_pwd)

    if replace: 
        drop_table(to_table,engine)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        if 'ingest_log' in metadata.tables:
            table = metadata.tables['ingest_log']
            conn = engine.connet()
            conn.execute(table.delete().where(table.c.dtype == dtype))
            con.commit()
    
    dfils = get_all_dfils(dataloc,dtype)
    dfils['to_table'] = to_table
    dfils['ingest_time'] = dt.now() 
    dfils.to_sql('ingest_log', engine, index=True,if_exists = 'append')

    if bulk_combine:
        df = load(dataloc,
                          dtype = dtype,
                          load_params = {'reduce':True})
        df['tag'] = tag
        print('=====================================')
        print('uploading data to server')
        df.name = tag
        uploader(df,engine)    
    else:
        def load_up(lab):
            df = load(lab,dtype = dtype)
            df[tag] = tag
            print('=====================================')
            print('uploading data to server')
            t = time.time()
            df.name = tag
            uploader(df,engine,to_table)
        dfils['file_path'].apply(load_up)
    engine.dispose()


def bulkInsert(dat,engine,useTable= 'ILO_RAW_DE',replace = True):
        # currently raw  code from stack exchange
        #load python script that batch loads pandas df to sql
        # from io import StringIO
        # connection = engine.connect()
        # cursor = connection.cursor()

        #df is the dataframe containing an index and the columns "Event" and "Day"
        #create Index column to use as primary key
        df = dat.reset_index()
        #create the table but first drop if we want
        if replace:
                drop_table(useTable,engine)
                #create new table 
                df.head(0).to_sql(useTable, engine,index = False)
        df.to_sql(useTable,engine,index = False,if_exists = 'append',
                                chunksize = 50000,
                                method = 'multi'
                                )
        return()

        #stream the data using 'to_csv' and StringIO(); then use sql's 'copy_from' function
        # output = StringIO()
        #ignore the index
        # df.to_csv(output, sep=',', header=False, index=False)
        #jump to start of stream
        # return(output)
        # output.seek(0)
        # contents = output.getvalue()
        # print(contents)

        metadata = MetaData()
        metadata.reflect(bind=engine)
        table = metadata.tables[useTable]
        # return(table)

        # stmt = insert(table, values = dat.reset_index().values.T)
        # engine.executemany(stmt)
        connection.execute(table.insert(),[tuple(r) for r in df.to_numpy().tolist()])
        connection.close()
        # engine.commit()





        # cur = connection.cursor()
        # cur.copy_from(output,useTable)    
        # connection.commit()
        # cur.close()

        # def bulkInsert():
        # from sqlalchemy import create_engine
        # import psycopg2 as pg
        # #load python script that batch loads pandas df to sql
        # import cStringIO

        # address = 'postgresql://<username>:<pswd>@<host>:<port>/<database>'
        # engine = create_engine(address)
        # connection = engine.raw_connection()
        # cursor = connection.cursor()

        # #df is the dataframe containing an index and the columns "Event" and "Day"
        # #create Index column to use as primary key
        # df.reset_index(inplace=True)
        # df.rename(columns={'index':'Index'}, inplace =True)

        # #create the table but first drop if it already exists
        # command = '''DROP TABLE IF EXISTS localytics_app2;
        # CREATE TABLE localytics_app2
        # (
        # "Index" serial primary key,
        # "Event" text,
        # "Day" timestamp without time zone,
        # );'''
        # cursor.execute(command)
        # connection.commit()

        # #stream the data using 'to_csv' and StringIO(); then use sql's 'copy_from' function
        # output = cStringIO.StringIO()
        # #ignore the index
        # df.to_csv(output, sep='\t', header=False, index=False)
        # #jump to start of stream
        # output.seek(0)
        # contents = output.getvalue()
        # cur = connection.cursor()
        # #null values become ''
        # cur.copy_from(output, 'localytics_app2', null="")    
        # connection.commit()
        # cur.close()
