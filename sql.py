################
# Dependencies #
################
import pandas as pd
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

############################
# Create the db connection #
############################
engine = sqlalchemy.create_engine('sqlite://', echo=False)
for x in os.listdir("this_one"):
    df = pd.read_csv(f'this_one/{x}')
    x = x.replace(" ", "_")[:len(x)-4]
    df.to_sql(x, con=engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
inspector = inspect(engine)

