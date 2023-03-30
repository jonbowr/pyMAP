from .tools.sql import *

class jill:

    def __init__(self):
        self.server = ssh_bind()
        self.engine = initEngine()
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.metadata.reflect(bind = self.engine)
        self.tables = self.metadata.tables

    def __del__(self):
        self.connection.close()
        self.connection.dispose()
        self.server.stop()
        del(self)

    def query(self, sql_query):
        from sqlalchemy import text
        # Credentials to database connection
        df = pd.read_sql(text(sql_query),self.connection)
        if 'dateTime' in df:
            from .tools import time
            df['dateTime'] = df['dateTime'].apply(time.localize_to_tz)
            df.set_index('dateTime',inplace = True)

        return(df)

    def queryWhen(self,table= '',after = '', before = '',cols = '*'):
        # Query database in time
        #       if table is given as a list of table names, the tables are combined,
        #       and the measurement times not shared are interpolated
        if type(table) == list:
            tabs = []
            for t in table:
                tabs.append(self.query(\
                    'select %s from %s where dateTime between "%s" and "%s"'%(\
                                            cols,t,after,before)))
            return(pd.concat(tabs).sort_index().interpolate('time').drop_duplicates())
        elif type(table)==str:
            return(self.query(\
            'select %s from %s where dateTime between "%s" and "%s"'%(\
                                            cols,table,after,before)))

