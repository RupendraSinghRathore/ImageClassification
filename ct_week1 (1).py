# -*- coding: utf-8 -*-
"""ct-week1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SU27rLBGBoqg_2C2n4L6uNp8CX4Lr5cn

#### Step 1: Data Preparation
"""

!pip install --pre pycaret -q

from pycaret.classification import setup, compare_models

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler

from google.colab import files
files.upload()

# !unzip /content/images.zip

# from google.colab import drive

# # Mount Google Drive
# drive.mount('/content/drive')

train_data = pd.read_csv("/content/train.csv")
train_data.head()

dossier = "/content/images/"
train_data['image_name'] = dossier + train_data['image_id']+'.jpg'
train_data.head()

train_data.shape

labels_cols = (train_data.drop(['image_id', 'image_name'], axis=1)).columns.values
labels_cols

print(train_data[labels_cols].isnull().sum())

print(train_data[labels_cols].sum())

X_cols = train_data[['image_id','image_name']]
X_cols.head()

y_cols = train_data[labels_cols].values
y_cols

from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state=42)
X_train, y_train = ros.fit_resample(X_cols, y_cols)

X_train.head()

labels_train = pd.DataFrame(y_train, columns=labels_cols)
labels_train.head()

label_names = labels_train[labels_train==1].stack().reset_index()['level_1']
label_names

labels_train["state"] = label_names
labels_train.head()

# Gather all data
train_data = pd.concat([X_train, labels_train], axis=1)
train_data.head()

train_data.shape

train_df = train_data[['image_name','state']]
train_df.head()

import os
import cv2
import numpy as np
import pandas as pd

# Load images and labels
def load_images(df):
    images = []
    labels = []
    for index, row in df.iterrows():
        img_path = os.path.join(row['image_name'])
        img = cv2.imread(img_path)
        if img is not None:
            img = cv2.resize(img, (128, 128))  # Resize images to 128x128
            images.append(img)
            labels.append(row['state'])  # 'labels' column with class names
    return np.array(images), np.array(labels)

images, labels = load_images(train_df)

"""### Step 2: Feature Extraction


"""

from skimage.feature import hog

def extract_hog_features(images):
    hog_features = []
    for image in images:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fd, _ = hog(gray_image, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualize=True)
        hog_features.append(fd)
    return np.array(hog_features)

features = extract_hog_features(images)

data = pd.DataFrame(features)
data['label'] = labels





# !pip install --pre pycaret -q

import pandas as pd
data = pd.read_csv('/content/train.csv')
data.head()

# !pip install --upgrade scikit-learn

from pycaret.classification import *
s = setup(data, target = 'label')



best = compare_models(include = ['svm','rf','gbc','xgboost','lightgbm'],n_select = 2)

# plot_model(best)
for model in best:
    plot_model(model)

evaluate_model(best[0])

