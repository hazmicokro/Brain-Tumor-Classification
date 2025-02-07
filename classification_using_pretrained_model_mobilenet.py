# -*- coding: utf-8 -*-
"""Classification using Pretrained Model Mobilenet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Dp0x-muwTf6P3HNDJZqVAQrds7KEjXXC

**Dataset : [Brain MRI Dataset](https://www.kaggle.com/sartajbhuvaji/brain-tumor-classification-mri) dari Kaggle**

**Deskripsi Data :** \
Total Data Images MRI : 3160 Images

Alokasi ulang ke 80% Train 20% Val
> Training Data (2525 Images) \
> Validation Data (635 Images)

###Mount Gdrive serta Download dan Ekstrak Dataset
"""

from google.colab import drive
drive.mount('/content/drive')

import os
os.environ['KAGGLE_CONFIG_DIR'] = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235"

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/MyDrive/Dataset/Dataset Citra 240 - 235

from google.colab import files
files.upload()

!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!ls ~/.kaggle

!chmod 600 /root/.kaggle/kaggle.json

!kaggle datasets download -d sartajbhuvaji/brain-tumor-classification-mri

!mkdir 'Dataset Brain MRI'

import zipfile
ekstrak_zip = '/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/brain-tumor-classification-mri.zip'
out_zip = zipfile.ZipFile(ekstrak_zip, 'r')
out_zip.extractall('/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/Dataset Brain MRI')
out_zip.close()

print('Berhasil Ekstrak ke Dataset Brain MRI')

"""###Mengalokasikan ulang Data Train dan Test menjadi 1 kesatuan Dataset"""

!mkdir "raw dataset"

import shutil

source = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/glioma_tumor (1)"
destination = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/glioma_tumor"

files = os.listdir(source)

for file in files:
	new_path = shutil.copy(f"{source}/{file}", destination)
	print(new_path)

source = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/meningioma_tumor (1)"
destination = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/meningioma_tumor"

files = os.listdir(source)

for file in files:
	new_path = shutil.copy(f"{source}/{file}", destination)
	print(new_path)

source = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/no_tumor (1)"
destination = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/no_tumor"

files = os.listdir(source)

for file in files:
	new_path = shutil.copy(f"{source}/{file}", destination)
	print(new_path)

source = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/pituitary_tumor (1)"
destination = "/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/pituitary_tumor"

files = os.listdir(source)

for file in files:
	new_path = shutil.copy(f"{source}/{file}", destination)
	print(new_path)

import glob 
for path in glob.glob("/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/glioma_tumor (1)*"):
    shutil.rmtree(path)
for path in glob.glob("/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/meningioma_tumor (1)*"):
    shutil.rmtree(path)
for path in glob.glob("/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/no_tumor (1)*"):
    shutil.rmtree(path)
for path in glob.glob("/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset/pituitary_tumor (1)*"):
    shutil.rmtree(path)

"""###Split Dataset dengan Alokasi 80% 20%"""

!pip install split-folders

!mkdir "New Dataset"

import splitfolders
splitfolders.ratio('/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/raw dataset', output='/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/New Dataset',
                   seed=82, ratio=(.8, .2), group_prefix=None)

total_image = len(list(glob.iglob("/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/New Dataset/train/*/*.jpg*", recursive=True)))
print("Total Dataset Train    : ",total_image," JPG Image \n")

total_image = len(list(glob.iglob("/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/New Dataset/val/*/*.jpg*", recursive=True)))
print("Total Dataset Val    : ",total_image," JPG Image \n")

"""###Preprocessing"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2
import os

training_dir = r"/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/New Dataset/train/"
validation_dir = r"/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/New Dataset/val/"

categories = ["glioma_tumor","meningioma_tumor","no_tumor","pituitary_tumor"]

img_size = (150,150)

training_data = []

def create_training_data():
    for category in categories:
        path = os.path.join(training_dir,category)
        class_num = categories.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img))
                new_array = cv2.resize(img_array,img_size) 
                training_data.append([new_array,class_num])
            except Exception as e:
                pass
create_training_data()
print("Berhasil Create Training Data")

X_train = []
Y_train = []
for features,label in training_data:
    X_train.append(features)
    Y_train.append(label)
X_train = np.array(X_train).reshape(-1,150,150)
X_train = X_train.astype('float32')/255.0  
X_train = X_train.reshape(-1,150,150,3)
print(X_train.shape)

IMG_SIZE = 150

validation_data = []

def create_validation_data():
    for category in categories:
        path = os.path.join(validation_dir,category)
        class_num = categories.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img))
                new_array = cv2.resize(img_array,img_size) 
                validation_data.append([new_array,class_num])
            except Exception as e:
                pass
create_validation_data()
print("Berhasil Create Validation Data")

X_val = []
Y_val = []
for features,label in validation_data:
    X_val.append(features)
    Y_val.append(label)
X_val = np.array(X_val).reshape(-1,150,150)
X_val = X_val.astype('float32')/255.0  
X_val = X_val.reshape(-1,150,150,3)
print(X_val.shape)

Y_train = np.array(Y_train)
Y_val = np.array(Y_val)

from keras.utils.np_utils import to_categorical # convert to one-hot-encoding
Y_train = to_categorical(Y_train, num_classes = 4)
Y_val = to_categorical(Y_val, num_classes = 4)

print("x_train shape",X_train.shape)
print("x_test shape",X_val.shape)
print("y_train shape",Y_train.shape)
print("y_test shape",Y_val.shape)

"""#Rancangan Model 2
Model 2 = Mobilenet dengan weight imagenet dan penggunaan checkpoint serta early callbacks
"""

from keras.applications import MobileNet
import tensorflow as tf

base_model = MobileNet(include_top=False,weights='imagenet',input_shape=(150,150,3))

model_mobnet = Sequential([
                           base_model, 
                           Flatten(), 
                           Dense(1024,activation=('relu'),input_dim=150),
                           Dropout(0.5),                           
                           Dense(512,activation=('relu')),
                           Dense(256,activation=('relu')),
                           Dropout(0.5),     
                           Dense(4,activation=('softmax'))
])
model_mobnet.layers[0].trainable = False

model_mobnet.summary()

Adam(learning_rate=0.00146, name='Adam')
model_mobnet.compile(optimizer = 'Adam',loss = 'categorical_crossentropy',metrics = ['accuracy'])

epochs = 50  
batch_size = 32
datagen = ImageDataGenerator(
        rotation_range=0,
        zoom_range = 0,
        width_shift_range=0,  
        height_shift_range=0,  
        horizontal_flip=True,  
        vertical_flip=False)

from tensorflow.keras import callbacks
filepath="/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/model_1.h5"
checkpoint = callbacks.ModelCheckpoint(
                                       filepath,
                                       monitor='val_accuracy',
                                       verbose=1,
                                       save_best_only=True,
                                       mode='auto',
                                       )
earlystop = callbacks.EarlyStopping(monitor='val_loss',
                                    mode='auto',
                                    patience=4,
                                    restore_best_weights=True)

import time

start = time.time()
datagen.fit(X_train)
history2 = model_mobnet.fit_generator(datagen.flow(X_train,Y_train, batch_size=batch_size),
                              epochs = epochs, validation_data = (X_val,Y_val),
                              steps_per_epoch = X_train.shape[0] // batch_size,
                              callbacks=[checkpoint])
stop = time.time()

print(f" Waktu training {stop - start} s")

model_mobnet.save('model_2_brain.h5')
print("Berhasil menyimpan model_2_brain.h5")

model_mobnet = load_model('model_2_brain.h5')
print("Berhasil load model_2_brain.h5")

"""##Plot dan Evaluasi Pada Model 2"""

acc = history2.history["accuracy"]
val_acc = history2.history["val_accuracy"]
loss = history2.history["loss"]
val_loss = history2.history["val_loss"]

epochs = range(len(acc))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=[20, 5])
ax1.plot(epochs, acc, 'k')
ax1.plot(epochs, val_acc, 'm')
ax1.set_title('Model  accuracy')
ax1.legend(['Model accuracy','Model Val accuracy'])

ax2.plot(epochs, loss, 'k')
ax2.plot(epochs, val_loss, 'm')
ax2.set_title('Model loss')
ax2.legend(['Model loss','Model Val loss'])

plt.show()

"""Evaluasi Model 2"""

loss, acc = model_mobnet.evaluate(X_train,Y_train,verbose = 0)
print("Training Loss {:.5f} dan Training Accuracy {:.2f}%".format(loss,acc*100))

loss, acc = model_mobnet.evaluate(X_val,Y_val,verbose = 0)
print("Validation Loss {:.5f} dan Validation Accuracy {:.2f}%".format(loss,acc*100))

from sklearn.metrics import classification_report

# CR untuk Training Data
print("model 2")
pred = model_mobnet.predict(X_train)
labels = (pred > 0.5).astype(np.int)

print(classification_report(Y_train, labels, target_names = categories))

# CR untuk Validation Data
print("model 2")
pred = model_mobnet.predict(X_val)
labels = (pred > 0.5).astype(np.int)

print(classification_report(Y_val, labels, target_names = categories))

import seaborn as sns
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.BuPu):

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

Y_pred = model_mobnet.predict(X_val)
Y_pred_classes = np.argmax(Y_pred,axis = 1) 
Y_true = np.argmax(Y_val,axis = 1) 

confusion_mtx = confusion_matrix(Y_true, Y_pred_classes) 
print("Model 2")
plot_confusion_matrix(confusion_mtx, classes = categories)

"""Precision Score Model 2"""

Y_pred_train = model_mobnet.predict(X_train)
Y_pred_classes_train = np.argmax(Y_pred_train,axis = 1) 
Y_true_train = np.argmax(Y_train,axis = 1) 

ps_train_model2 = precision_score(Y_pred_classes_train, Y_true_train, average='weighted')
ps_val_model2 = precision_score(Y_pred_classes, Y_true, average='weighted')
print('Precision Score Training Data Model 2:', ps_train_model2)
print('Precision Score Validation Data Model 2:', ps_val_model2)

"""Recall Score Model 2"""

rs_train_model2 = recall_score(Y_pred_classes_train, Y_true_train, average='weighted')
rs_val_model2 = recall_score(Y_pred_classes, Y_true, average='weighted')
print('Precision Score Training Data Model 2:', rs_train_model2)
print('Precision Score Validation Data Model 2:', rs_val_model2)

"""F1 Score Model 2"""

f1_train_model2 = f1_score(Y_pred_classes_train, Y_true_train, average='weighted')
f1_val_model2 = f1_score(Y_pred_classes, Y_true, average='weighted')
print('Precision Score Training Data Model 2:', f1_train_model2)
print('Precision Score Validation Data Model 2:', f1_val_model2)

"""##Prediksi Gambar dengan Model 2"""

from PIL import Image 
IMG = Image.open('/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/New Dataset/val/pituitary_tumor/image(11).jpg')
plt.imshow(IMG)
IMG = IMG.resize((150,150))
IMG = np.array(IMG)
IMG = np.true_divide(IMG,255)
IMG = IMG.reshape(1, 150,150, 3)

classes = { 'training':['glioma_tumor', 'meningioma_tumor','no_tumor','pituitary_tumor'],
                  'test':['glioma_tumor', 'meningioma_tumor','no_tumor','pituitary_tumor']}

predictions_images = model_mobnet.predict(IMG)
predicted_classes = np.argmax(predictions_images,axis=1)
predicted_class = classes['test'][predicted_classes[0]]

print("Prediksi Kelas",predicted_classes)
print("Gambar Tersebut merupakan {}.".format(predicted_class.lower()))

IMG2 = Image.open('/content/drive/MyDrive/Dataset/Dataset Citra 240 - 235/New Dataset/val/meningioma_tumor/image(20).jpg')
plt.imshow(IMG2)
IMG2 = IMG2.resize((150,150))
IMG2 = np.array(IMG2)
IMG2 = np.true_divide(IMG2,255)
IMG2 = IMG2.reshape(1, 150,150, 3)

classes = { 'training':['glioma_tumor', 'meningioma_tumor','no_tumor','pituitary_tumor'],
                  'test':['glioma_tumor', 'meningioma_tumor','no_tumor','pituitary_tumor']}

predictions_images = model_mobnet.predict(IMG2)
predicted_classes = np.argmax(predictions_images,axis=1)
predicted_class = classes['test'][predicted_classes[0]]

print("Prediksi Kelas",predicted_classes)
print("Gambar Tersebut merupakan {}.".format(predicted_class.lower()))