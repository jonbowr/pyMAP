from tools.sql import *

class jill:
    
    def __init__(self):
        self.server = ssh_bind()
        self.engine = initEngine()
        self.connection = self.engine.connect()
        self.metadata = MetaData()
        self.metadata.reflect(bind = self.engine)
        self.tables = self.metadata.tables

    def queryDF(self, sql_query):
        from sqlalchemy import text
        # Credentials to database connection
        df = pd.read_sql(text(sql_query),self.connection)
        return(df)

    def __del__(self):
        self.connection.close()
        self.connection.dispose()
        self.server.stop()
        del(self)