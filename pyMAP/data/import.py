from sqlalchemy import create_engine

# Credentials to database connection
hostname="127.0.0.1:3306"
dbname="test"
uname="jsx54"
pwd="dlu.841"

# # Create SQLAlchemy engine to connect to MySQL Database
engine = create_engine("mysql+pymysql://@{host}/{db}"
                .format(host=hostname, 
                        db=dbname, 
#                         user=uname, 
#                         pw=pwd
                       ))

# # Convert dataframe to sql table                                   
# df.to_sql('users', engine, index=False)

# Import data from sql database
df = pd.read_sql('ILO_IFB',engine)