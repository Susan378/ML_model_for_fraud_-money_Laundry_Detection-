import pandas as pd
import numpy as np
import json
import csv
from random import randint

DF = pd.read_csv("data/TR_data.csv")
DF = DF.to_numpy()

OriginalCol = 3
DestinCol = 6
Origin = []
dest = []
nameCount = {}
mm = []


for name in X[:,OriginalCol]:
	if nameCount.get(name,-1) == -1:
		Origin.append(name)

		nameCount[name] = 1

	else:
		nameCount[name] += 1
		mm.append(name)

for name in X[:,DestinCol]:
	if nameCount.get(name,-1) == -1:
		dest.append(name)

		nameCount[name] = 1

	else:
		nameCount[name] += 1
		mm.append(name)

countArr = []
count = 0
for z, value in nameCount.items():
	if value>40:
		countArr.append(value)
		count += 1


G_data = []

for i in range(X.shape[0]):
	if nameCount.get(X[i,3],-1) > 40 or nameCount.get(X[i,6],-1) > 40:
		G_data.append(X[i,:])


with open("data_processed/filtered_data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerows(G_data)



DF = pd.read_csv("processed.csv")
DF = DF.to_numpy()


DF_Pri = []
step = 0
trans_type = 1
amount = 2
nameOrig = 3
oldbalanceOrg = 4
nameDest = 6
oldbalanceDest = 7
accountType = 8
isFraud = 9
isFlaggedFraud = 10

transfer = ["WIRE_IN", "WIRE_OUT"]
for i in range(X.shape[0]):
	arr = []
	arr.append(X[i,step])
	if X[i,trans_type] =="PAYMENT":
		arr.append("CREDIT")
	elif X[i,trans_type] =="TRANSFER":
		arr.append(transfer[randint(0,1)])
	else:
		arr.append(X[i,trans_type])
	arr.append(X[i,amount])
	arr.append(X[i,nameOrig])
	arr.append(X[i,oldbalanceOrg])
	arr.append(X[i,nameDest])
	arr.append(X[i,oldbalanceDest])
	if X[i,trans_type] == "TRANSFER":
		arr.append("FOREIGN")
	else:
		arr.append("DOMESTIC")

	arr.append(X[i,isFraud])
	arr.append(X[i,isFlaggedFraud])

	DF_Pri.append(arr)

columns=['step','trans_type','amount','nameOrig','oldbalanceOrg',
        'nameDest','oldbalanceDest','accountType','isFraud','isFlaggedFraud']

data_primary = pd.DataFrame(DF_Pri, columns=columns)

data_primary.to_csv('data_processed/filtered_data_2.csv', index=False)

