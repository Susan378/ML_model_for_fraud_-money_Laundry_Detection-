import numpy as np
import pandas as pd
import pickle
import json
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, f1_score, recall_score, precision_score
from catboost import CatBoostClassifier

data_path = "data_processed/final_data.csv"
dataMat = pd.read_csv(data_path)
data = dataMat.to_numpy()

cat_feat = [i for i in dataMat.columns if dataMat[i].dtypes == 'O']

a = dict(dataMat.isnull().sum())
b = [[i, a[i]] for i in a.keys()]
missing = pd.DataFrame(b, columns=['features', 'null_values_count'])

encoder = LabelEncoder()
for i in cat_feat:
  dataMat[i] = encoder.fit_transform(dataMat[i])


X = dataMat.iloc[:, :-1]
y = dataMat['isFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


model = CatBoostClassifier(random_state=42, class_weights={0:1, 1:12}, silent=True)

model.fit(X_train, y_train)
y_pred_cat = model.predict(X_test)

model_path = "saved_models/model.pkl"
pickle.dump(model, open(model_path, 'wb'))

metric_file_path = "reports/performance.json"
with open(metric_file_path, "r") as f:
    data = json.load(f)

model_metric = {
    "time_stamp": datetime.now().strftime("%d-%m-%Y_%H:%M:%S"),
    "confusion_matrix": confusion_matrix(y_test, y_pred_cat).tolist(),
    "precision": precision_score(y_test, y_pred_cat),
    "recall": recall_score(y_test, y_pred_cat),
    "f1_score": f1_score(y_test, y_pred_cat)
}

data['model_metric'].append(model_metric)
with open(metric_file_path, "w") as f:
    json.dump(data, f, indent=4)

