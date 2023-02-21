import numpy as np
import pandas
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

DF= pandas.read_csv('data/preprocessed_data.csv')
cols = list(DF.columns.values)
DFmatrix = DF.to_numpy()

X = DFmatrix[:,1:-2]
Y = DFmatrix[:,-1]

RF_model = RandomForestClassifier(random_state=42)

RF_model.fit(X, Y.astype(int))

Selected_FT = RF_model.feature_importances_

Sorted_Features_ind = np.argsort(Selected_FT)

FT_importance = [[cols[i+2], Selected_FT[i]] for i in reversed(Sorted_Features_ind)]
features = pandas.DataFrame(FT_importance, columns=["features", "importance_score"])
features.to_csv("reports/feature_importances.csv", index=False)

