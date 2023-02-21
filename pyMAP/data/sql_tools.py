from sqlalchemy import create_engine

def importSQL(query = ''):
        import pandas as pd
        # Credentials to database connection
        hostname="127.0.0.1:3306"
        dbname="IMAPlo"
        uname="loDB_user"
        pwd="cM2MhRu0C"

        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                                .format(host=hostname, db=dbname, user=uname, pw=pwd))

        return(pd.read_sql(query,engine).set_index('dateTime'))