"""
This module implements the main functionalities of celoMine.

Author: Jean Bertin
Github: https://github.com/JeanBertinR
"""

__author__ = "Jean Bertin"
__email__ = "jeanbertin.ensam@gmail.com"
__status__ = "planning"

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

class AnalyseEventLog:
    def __init__(self, log_file):
        """
        Initialize the AnalyseEventLog class.

        Parameters:
        - log_file (str): Path to the log file.
        """
        self.log_file = log_file
        self.data = None
        self.encoder = LabelEncoder()
        self.model = DecisionTreeClassifier()

    def load_data(self):
        """
        Load the log file data into a pandas DataFrame.
        """
        self.data = pd.read_csv(self.log_file, sep=';')

    def preprocess_data(self):
        """
        Preprocess the log file data for machine learning.
        """
        # Perform any necessary preprocessing steps, such as data cleaning and feature engineering.
        # Here, we assume that the log file has a 'target' column representing the target variable.
        # Convert categorical variables to numerical using label encoding.
        self.data['target'] = self.encoder.fit_transform(self.data['target'])

    def train_model(self):
        """
        Train a machine learning model using the preprocessed data.
        """
        # Convertir la colonne 'timestamp' en format de date/heure
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])

        # Créer de nouvelles colonnes pour l'année, le mois, le jour, l'heure et les minutes
        self.data['year'] = self.data['timestamp'].dt.year
        self.data['month'] = self.data['timestamp'].dt.month
        self.data['day'] = self.data['timestamp'].dt.day
        self.data['hour'] = self.data['timestamp'].dt.hour
        self.data['minute'] = self.data['timestamp'].dt.minute

        # Drop the timestamp column
        X = self.data.drop(['timestamp', 'step', 'target'], axis=1)
        y = self.data['target']

        # Convert the variable to categorical
        le = LabelEncoder()
        y = le.fit_transform(y)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the decision tree classifier
        self.model = DecisionTreeClassifier()
        self.model.fit(X_train, y_train)

        # Predict the target variable for the test set
        y_pred = self.model.predict(X_test)

        # Calculate the accuracy of the model
        accuracy = accuracy_score(y_test, y_pred)
        print("Model Accuracy:", accuracy)

    def predict(self, new_data):
        """
        Make predictions using the trained machine learning model.

        Parameters:
        - new_data (DataFrame): New data for prediction.

        Returns:
        - predictions (array): Predicted target values.
        """
        # Preprocess the new data
        new_data = self.encoder.transform(new_data)

        # Make predictions
        predictions = self.model.predict(new_data)

        return predictions

class VisualizeEventLog:
    def __init__(self, log_file):
        """
        Initialize the VisualizeEventLog class.

        Parameters:
        - log_file (str): Path to the log file.
        """
        self.log_file = log_file
        self.data = None

    def load_data(self):
        """
        Load the log file data into a pandas DataFrame.
        """
        self.data = pd.read_csv(self.log_file, sep=';')

    def visualize_process(self):
        """
        Visualize the process graphically using the log file data.
        """
        # Convert timestamp column to datetime
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])

        # Create a directed graph
        G = nx.DiGraph()

        # Add nodes to the graph
        unique_steps = self.data['step'].unique()
        for step in unique_steps:
            G.add_node(step)

        # Add edges and processing time
        for i in range(len(self.data) - 1):
            current_step = self.data.loc[i, 'step']
            next_step = self.data.loc[i + 1, 'step']
            processing_time = self.data.loc[i + 1, 'timestamp'] - self.data.loc[i, 'timestamp']
            G.add_edge(current_step, next_step, processing_time=processing_time)

        # Set node positions for visualization
        pos = nx.spring_layout(G)

        # Draw nodes and edges
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos)

        # Add labels to nodes
        labels = {step: step for step in unique_steps}
        nx.draw_networkx_labels(G, pos, labels)

        # Add processing time labels to edges
        edge_labels = nx.get_edge_attributes(G, 'processing_time')
        nx.draw_networkx_edge_labels(G, pos, edge_labels)

        # Display the graph
        plt.title("Process Visualization")
        plt.axis("off")
        plt.show()