import numpy as np
import pandas as pd
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from django.shortcuts import render
from django.conf import settings
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load the dataset
data_path = os.path.join(settings.MEDIA_ROOT, 'data', 'Sleep_health_and_lifestyle_dataset.csv')
df = pd.read_csv(data_path)

# Fill missing values in 'Sleep Disorder' column with 'None'
df['Sleep Disorder'] = df['Sleep Disorder'].fillna('None')

# Encode categorical features
encoder = LabelEncoder()
categorical_features = ['Gender', 'Occupation', 'BMI Category', 'Sleep Disorder', 'Blood Pressure']
for feature in categorical_features:
    df[feature] = encoder.fit_transform(df[feature])

# Features and target variable
x = df[['Age', 'Sleep Duration', 'Physical Activity Level', 'Heart Rate', 'Daily Steps']]
y = df['Sleep Disorder']

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=39)

# Function to train model and evaluate performance
def train_and_evaluate_model(model, x_train, y_train, x_test, y_test, model_name):
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions)
    # print(f"Classification Report for {model_name}:\n{report}")
    return accuracy, predictions

# Function to plot and save confusion matrix
def plot_confusion_matrix(y_test, predictions, model_name, cmap, save_path):
    cm = confusion_matrix(y_test, predictions)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap=cmap)
    plt.title(f'Confusion Matrix for {model_name}')
    plt.savefig(save_path)
    plt.close()

def Model_Evaluation_View(request):
    models = {
        'SVC': SVC(),
        'DecisionTree': DecisionTreeClassifier(),
        'RandomForest': RandomForestClassifier(),
        'KNeighbors': KNeighborsClassifier()
    }

    accuracies = {}
    reports = {}
    for name, model in models.items():
        accuracies[name], predictions = train_and_evaluate_model(model, x_train, y_train, x_test, y_test, name)
        reports[name] = classification_report(y_test, predictions)
        plot_confusion_matrix(y_test, predictions, name, plt.cm.Blues, os.path.join(settings.MEDIA_ROOT, f'{name}.png'))

    context = {
        'accuracy_svc': accuracies['SVC'],
        'accuracy_rf': accuracies['RandomForest'],
        'accuracy_knn': accuracies['KNeighbors'],
        'accuracy_dt': accuracies['DecisionTree'],
        'rf_report': reports['RandomForest'],
        'svc_report': reports['SVC'],
        'knn_report': reports['KNeighbors'],
        'dt_report': reports['DecisionTree']
    }
    return render(request, 'analysis/model_evaluation.html', context)

def ModelPrediction(request):
    if request.method == 'POST':

        age = float(request.POST['age'])
        sleep_duration = float(request.POST['sleep'])
        physical_activity_level = float(request.POST['activity'])
        heart_rate = float(request.POST['heartrate'])
        daily_steps = float(request.POST['dailysteps'])

        input_data = [[age, sleep_duration, physical_activity_level, heart_rate, daily_steps]]

        rf = RandomForestClassifier()
        rf.fit(x_train, y_train)

        pred_idx = rf.predict(input_data)[0]
        proba = rf.predict_proba(input_data)[0]
        max_proba = max(proba) * 100

        pred_map = {
            0: 'Insomnia',
            1: 'No Sleep Disorder',
            2: 'Sleep Apnea'
        }

        prediction = pred_map.get(pred_idx, 'Unknown')

        return render(request, 'analysis/predictionpage.html', {'pred': prediction, 'accuracy': f"{max_proba:.2f}%"})

    return render(request, 'analysis/predictionpage.html')
