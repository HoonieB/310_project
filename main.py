from knn_model import KNN, load_dataset
from sklearn.model_selection import KFold
import numpy as np


X, Y = load_dataset('dataset.csv') #load the dataset

kfold = KFold(n_splits=10, shuffle=True, random_state=42) #split data into training/test sets (5 by default)
accuracies = []
precisions = []
recalls = []
specificities = []

positive_class = 'gun' #evaluating with respect to gun

for train_index, test_index in kfold.split(X):
    X_train = X[train_index]
    X_test = X[test_index]
    Y_train = Y[train_index]
    Y_test = Y[test_index]

    knn = KNN(k=5) #the default value is 3, but could be changed
    knn.fit(X_train, Y_train)
    Y_pred = knn.predict(X_test)

    Y_pred = np.array(Y_pred)
    Y_test = np.array(Y_test)

    TP = np.sum((Y_pred == positive_class) & (Y_test == positive_class))
    TN = np.sum((Y_pred != positive_class) & (Y_test != positive_class))
    FP = np.sum((Y_pred == positive_class) & (Y_test != positive_class))
    FN = np.sum((Y_pred != positive_class) & (Y_test == positive_class))

    accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0

    precisions.append(precision)
    recalls.append(recall)
    specificities.append(specificity)
    accuracies.append(accuracy)

print("GUN: ")

print("Precisions: ", precisions)
print ("Avg Precision: ", np.mean(precisions))

print("Recalls: ", recalls)
print ("Avg Recall: ", np.mean(recalls))

print("Specificities: ", specificities)
print ("Avg Specificity: ", np.mean(specificities), "\n")

print("Accuracies: ", accuracies)
print ("Avg Accuracy: ", np.mean(accuracies), "\n")

accuracies = []
precisions = []
recalls = []
specificities = []

positive_class = 'fist' #evaluating with respect to fist

for train_index, test_index in kfold.split(X):
    X_train = X[train_index]
    X_test = X[test_index]
    Y_train = Y[train_index]
    Y_test = Y[test_index]

    knn = KNN(k=5) #the default value is 3, but could be changed
    knn.fit(X_train, Y_train)
    Y_pred = knn.predict(X_test)

    Y_pred = np.array(Y_pred)
    Y_test = np.array(Y_test)

    TP = np.sum((Y_pred == positive_class) & (Y_test == positive_class))
    TN = np.sum((Y_pred != positive_class) & (Y_test != positive_class))
    FP = np.sum((Y_pred == positive_class) & (Y_test != positive_class))
    FN = np.sum((Y_pred != positive_class) & (Y_test == positive_class))

    accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0

    precisions.append(precision)
    recalls.append(recall)
    specificities.append(specificity)
    accuracies.append(accuracy)

print("FIST: ")

print("Precisions: ", precisions)
print ("Avg Precision: ", np.mean(precisions))

print("Recalls: ", recalls)
print ("Avg Recall: ", np.mean(recalls))

print("Specificities: ", specificities)
print ("Avg Specificity: ", np.mean(specificities), "\n")

print("Accuracies: ", accuracies)
print ("Avg Accuracy: ", np.mean(accuracies))
