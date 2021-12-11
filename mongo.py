import pandas as pd
import os
import pymongo
import json

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client["project2"]

for x in os.listdir("../this_one"):
    df = pd.read_csv(f'this_one/{x}')
    x = x.replace(" ", "_")[:len(x)-4]
    collist = db.list_collection_names()
    records = json.loads(df.T.to_json()).values()
    if x not in collist:
        db[x].insert_many(records)

