################
# Dependencies #
################
import pandas as pd
import os
import pymongo
import json
import matplotlib.pyplot as plt
import numpy as np

############################
# Create the db connection #
############################
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client["project2"]

##################################################
# Parse through Every .csv file for the database #
# and insert them into pymongo                   #
##################################################
for x in os.listdir("this_one"):
    df = pd.read_csv(f'this_one/{x}')
    x = x.replace(" ", "_")[:len(x)-4]
    collist = db.list_collection_names()
    records = json.loads(df.T.to_json()).values()
    if x not in collist:
        db[x].insert_many(records)

###########################################################
# Go through the database and convert them back into df's #
###########################################################
for x in db.list_collection_names():
    df = pd.DataFrame(list(db[x].find()))
    del df['_id']
df = pd.DataFrame(list(db["texas_combined_completed_data"].find()))
del df['_id']

#####################################
# Create the death/vaccination rate #
#####################################
death_rate = []
vaccinated_rate = []
for x in range(len(df["Deaths"]) - 1):
    death_rate.append(float(df["Deaths"].tolist()[x + 1] - df["Deaths"].tolist()[x]))
    vaccinated_rate.append(df["People_Fully_Vaccinated"].tolist()[x + 1] - df["People_Fully_Vaccinated"].tolist()[x])

#######################################
# Convert the rates into weekly rates #
#######################################
dr_weekly = []
vr_weekly = []
for x in range(0, 273, 7):
    dr = death_rate[x]
    vr = vaccinated_rate[x]
    for y in range(1, 7):
        dr += death_rate[x+y]
        vr += vaccinated_rate[x+y]
    dr_weekly.append(dr / 7)
    vr_weekly.append(vr / 7 / 100)

#################
# Plot the data #
#################
plt.plot(
    np.arange((len(vr_weekly))),
    vr_weekly
)
plt.plot(
    np.arange(len(dr_weekly)),
    dr_weekly
)
plt.show()
