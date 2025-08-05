import numpy as np
import csv

#function to calculate the euclidean distance between two points
def euclidean_distance(x, y):
    diff = x - y
    squared = diff**2
    total = np.sum(squared)
    return np.sqrt(total)

#function to find the majority voted label of the  nearest neighbours
def majority_vote(labels):
    counts = {}
    for label in labels:
        if label in counts: #if the label is already in the dictionary, add a vote
            counts[label] += 1
        else: #if it's not already in the dictionary, add it to the dictionary
            counts[label] = 1

    max_count = 0
    majority_label = None
    #find the label with the most votes
    for label, count in counts.items():
        if count > max_count:
            max_count = count
            majority_label = label
    return majority_label

#function to load the dataset and read it as features and labels
def load_dataset(csv_path):
    labels = []
    features = []
    with open(csv_path, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            labels.append(row[0]) #the first value in each row is the label
            numeric_values = [float(value) for value in row[1:]] #takes all the coordinates and converts them to floats
            features.append(numeric_values) #those coordinates are stored in a feature list

    return np.asarray(features), np.asarray(labels) #change the lists to arrays

#a basic class for KNN
class KNN:
    def __init__(self, k=3): #constructor
        self.k = k

    def fit(self, training_data, training_labels): #stores training dataset inside the model
        self.X_train = np.asarray(training_data) #convert data to array
        self.y_train = np.asarray(training_labels) #convert labels to array

    #the method that predicts the next label using majority vote
    def predict(self, X_test):

        predictions = []

        for test_point in X_test:
            distances = []

            for x in self.X_train: #for each test point in the test set
                dist = euclidean_distance(test_point, x) #calculate the distance
                distances.append(dist) #store the distance

            distances = np.array(distances)
            k_indices = distances.argsort()[:self.k] #find indices of k nearest points
            k_nearest_labels = self.y_train[k_indices] #get the labels of those nearest points
            most_voted_label = majority_vote(k_nearest_labels) #use majority_vote function to find the most voted label
            predictions.append(most_voted_label) #add that most voted label to predictions array
        return predictions

