import tensorflow
import keras
from keras import models, layers
from keras.models import Sequential
#Import from keras_preprocessing not from keras.preprocessing
from keras_preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers
from tensorflow.keras import optimizers
optimizers.Adam()
opt = tensorflow.keras.optimizers.Adam()
import pandas as pd
import numpy as np
import cv2

df=pd.read_csv("foo.csv",dtype=str)
testdf=pd.read_csv("test.csv",dtype=str)

datagen=ImageDataGenerator(rescale=1./255, validation_split=0.25)
train_generator=datagen.flow_from_dataframe(dataframe=df, directory="./", x_col="res", y_col="label", class_mode="categorical", target_size=(16,16,1), batch_size=32)

model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same',
                 input_shape=(16,16,1)))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(57, activation='softmax'))

opt = tensorflow.keras.optimizers.Adam(lr=0.0001)

train_generator=datagen.flow_from_dataframe(
dataframe=df,
directory="./",
x_col="res",
y_col="label",
subset="training",
batch_size=32,
seed=42,
shuffle=True,
class_mode="categorical",
color_mode='grayscale',
target_size=(16,16))

valid_generator=datagen.flow_from_dataframe(
dataframe=df,
directory="./",
x_col="res",
y_col="label",
subset="validation",
batch_size=32,
seed=42,
shuffle=True,
class_mode="categorical",
color_mode='grayscale',
target_size=(16,16))

test_datagen=ImageDataGenerator(rescale=1./255.)

test_generator=test_datagen.flow_from_dataframe(
dataframe=testdf,
directory="./",
x_col="res",
y_col=None,
batch_size=32,
seed=42,
shuffle=False,
class_mode=None,
color_mode='grayscale',
target_size=(16,16))

#model.compile(optimizers.rmsprop(lr=0.0001),
model.compile(opt, loss="categorical_crossentropy", metrics=["accuracy"])
STEP_SIZE_TRAIN=train_generator.n//train_generator.batch_size
STEP_SIZE_VALID=valid_generator.n//valid_generator.batch_size
STEP_SIZE_TEST=test_generator.n//test_generator.batch_size

model.fit_generator(generator=train_generator,
                    steps_per_epoch=STEP_SIZE_TRAIN,
                    validation_data=valid_generator,
                    validation_steps=STEP_SIZE_VALID,
                    epochs=100)

model.evaluate_generator(generator=valid_generator,
steps=STEP_SIZE_TEST)

model.save('model.h5')

#img = cv2.imread('al.png', 0)
#img = np.expand_dims(img, axis=0)
#model.predict(img)
