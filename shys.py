import os
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
# 进行优化
from kerastuner.tuners import Hyperband
from kerastuner import HyperParameters

# 创建两个数据生成器，指定scaling范围0-1
train_data = ImageDataGenerator(rescale=1 / 255)
validation_data = ImageDataGenerator(1 / 255)
# 指向训练数据文件夹
train_generator = train_data.flow_from_directory(
    r"C:\Users\97848\Desktop\horse-or-human",  # 训练数据所在文件夹
    target_size=(300, 300),  # 指定输出尺寸
    batch_size=32,  # 每读取一批取多少
    class_mode='binary'  # 指定二分类
)
validation_generator = train_data.flow_from_directory(
    r"C:\Users\97848\Desktop\validation-horse-or-human",
    target_size=(300, 300),
    batch_size=32,
    class_mode='binary'
)

hp = HyperParameters()
def build_model(hp):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Conv2D(hp.Choice('num_filters_layer0', values=[16, 64], defaule=16), (3, 3), activation='relu', input_shape=(300, 300, 3)))
    model.add(tf.keras.layers.MaxPooling2D((2, 2)))
    for i in range(hp.int('num_conv_layers', 1, 3)):
        model.add(tf.keras.layers.Conv2D(hp.Choice(f'num_filters_layer{i}', values=[16, 64], defaule=16), (3, 3), activation='relu'))
        model.add(tf.keras.layers.MaxPooling2D(((2, 2))))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(hp.int('hidden_units', 128, 512, step=32), activation='relu'))
        model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer=RMSprop(learning_rate=0.001), metrics=['acc'])
    return model


tuner = Hyperband(
    build_model,
    objective='val_acc',
    max_epochs=15,
    directory='horse_human_params',
    hyperparameters=hp,
    project_name='my_horse_human_project'
)

tuner.search(train_generator, epochs=10, validation_data=validation_generator)
# history=model.fit(train_generator,epochs=10,verbose=1,validation_data=validation_generator,validation_steps=8)