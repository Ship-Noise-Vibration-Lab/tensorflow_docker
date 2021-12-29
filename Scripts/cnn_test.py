'''
Python script for CNN performance benchmark
출처 : https://gaiag.tistory.com/74#3.-MNIST-Data
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.utils import to_categorical # one-hot 인코딩
import numpy as np
import os, datetime

learning_rate = 0.001
training_epochs = 5
batch_size = 100

mnist = keras.datasets.mnist
class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

# MNIST image load (trian, test)
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# 0~255 중 하나로 표현되는 입력 이미지들의 값을 1 이하가 되도록 정규화
train_images = train_images.astype(np.float32) / 255.
test_images = test_images.astype(np.float32) / 255.

# np.expand_dims 차원을 변경
train_images = np.expand_dims(train_images, axis=-1)
test_images = np.expand_dims(test_images, axis=-1)

# label을 ont-hot encoding
train_labels = to_categorical(train_labels, 10)
test_labels = to_categorical(test_labels, 10)

# Functional 모델 층 구성하기
def create_model():
    inputs = keras.Input(shape=(28, 28, 1))
    conv1 = keras.layers.Conv2D(filters=32, kernel_size=[3, 3], padding='SAME', activation=tf.nn.relu)(inputs)
    pool1 = keras.layers.MaxPool2D(padding='SAME')(conv1)
    conv2 = keras.layers.Conv2D(filters=64, kernel_size=[3, 3], padding='SAME', activation=tf.nn.relu)(pool1)
    pool2 = keras.layers.MaxPool2D(padding='SAME')(conv2)
    conv3 = keras.layers.Conv2D(filters=128, kernel_size=[3, 3], padding='SAME', activation=tf.nn.relu)(pool2)
    pool3 = keras.layers.MaxPool2D(padding='SAME')(conv3)
    pool3_flat = keras.layers.Flatten()(pool3)
    dense4 = keras.layers.Dense(units=256, activation=tf.nn.relu)(pool3_flat)
    drop4 = keras.layers.Dropout(rate=0.4)(dense4)
    logits = keras.layers.Dense(units=10, activation=tf.nn.softmax)(drop4)
    return keras.Model(inputs=inputs, outputs=logits)


model = create_model() # 모델 함수를 model로 변경
model.summary() # 모델에 대한 요약 출력해줌

# CNN 모델 구조 확정하고 컴파일 진행
model.compile(loss='categorical_crossentropy',      # crossentropy loss
              optimizer='adam',                      # adam optimizer
              metrics=['accuracy'])                  # 측정값 : accuracy


t1_1 = datetime.datetime.now()

# 학습실행
model.fit(train_images, train_labels,                # 입력값
          batch_size=batch_size,                      # 1회마다 배치마다 100개 프로세스
          epochs=training_epochs,                     # 15회 학습
          verbose=1,                                  # verbose는 학습 중 출력되는 문구를 설정하는 것
          validation_data=(test_images, test_labels)) # test를 val로 사용

t2_1 = datetime.datetime.now()

score = model.evaluate(test_images, test_labels, verbose=0) # test 값 결과 확인

print('Test loss:', score[0])
print('Test accuracy:', score[1])
print("Computation time: " + str(t2_1-t1_1))