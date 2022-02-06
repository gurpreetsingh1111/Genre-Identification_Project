# Import libraries.
import csv
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import classification_report

# This is the name of the training file.
training_filename = "../datasets/msd.csv"

# Read the csv file.
reader = pd.read_csv(training_filename)

# Drop the ID of song as it has no information.
reader.drop(reader.columns[[1, 2, 3]], axis=1, inplace=True)

# Some columns have string values in numerical columns.
# So cleaning that.
for i in range(1, reader.shape[1]):
	reader = reader[pd.to_numeric(reader[reader.columns[i]], errors='coerce').notnull()]

# Convert string values to float.
reader = reader.convert_objects(convert_numeric=True)

# LabelEncoder - assigns number 1-n
le = preprocessing.LabelEncoder()

# Extract the numerical features and perform normalization.
reader_numerical = reader.select_dtypes(exclude=[object])
reader_numerical = np.matrix(reader_numerical).astype("double")
reader_numerical = preprocessing.normalize(reader_numerical, norm='l2')

# Extract the categorical variables and perform one hot encoding.
reader_categorical = reader.select_dtypes(include=[object])
reader_label_transformed = reader_categorical.apply(le.fit_transform)

# Put the categorical and numerical features together.
reader = np.concatenate((reader_label_transformed, reader_numerical), axis=1)

# Randomly permute the data and select training and test sets.
indices = np.random.permutation(reader.shape[0])
training_idx, test_idx = indices[:500], indices[500:]
training, test = reader[training_idx,:], reader[test_idx,:]

# Initialize the decision tree classifier.
# clf = tree.DecisionTreeClassifier()
clf = RandomForestClassifier(n_estimators=304, min_samples_split=3, min_samples_leaf=6)

# Train on the model.
clf = clf.fit(training[:, 1:], training[:, 0])

# Predict on the test examples.
pred = clf.predict(test[:, 1:])

# Calculate the error and check for the accuracy.
total_error = np.sum(pred != test[:, 0])
accuracy = 1 - (total_error+0.0)/test.shape[0]
target_names = ['classic pop and rock', 'punk', 'folk', 'dance and electronica', 'metal', 'jazz and blues', 'classical', 'hip-hop', 'soul and reggae']
print f1_score(test[:, 0], pred, average='weighted')
print classification_report(test[:, 0], pred, target_names=target_names)
print accuracy