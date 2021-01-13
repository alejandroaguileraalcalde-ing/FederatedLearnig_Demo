# FederatedLearnig_Demo
This is the code I created for showing the possibility of creating a simple linear regression model with tensorflow and used it in an android app in order to use Federated Learning. Here is both the **app** and **server** code. Also the machine learning **model** file. 

In this project I created a machine learning model and train it on device with my phone. 




![App image](app_image.PNG)


### How it works:

  Your device downloads the current model, improves it by learning from data on your phone, and then summarizes the changes as a small focused update. Only this update to the model is sent to the cloud( I used Heroku <img src="https://www.fullstackpython.com/img/logos/heroku.png" width="52"> and Google Cloud <img src="data:image/png;base64,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" width="52">but other could be used), where it is immediately averaged with other user updates to improve the shared model. All the training data remains on your device, and no individual updates are stored in the cloud.
  
  
![Image of googleAI](https://1.bp.blogspot.com/-K65Ed68KGXk/WOa9jaRWC6I/AAAAAAAABsM/gglycD_anuQSp-i67fxER1FOlVTulvV2gCLcB/s1600/FederatedLearning_FinalFiles_Flow%2BChart1.png)


### Model:
``` python

import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
from __future__ import print_function
from tensorflow.keras.callbacks import TensorBoard

x = tf.placeholder(tf.float32, name='input')
y_ = tf.placeholder(tf.float32, name='target')
W = tf.Variable(5., name='W')
b = tf.Variable(3., name='b')

y = tf.add(tf.multiply(x, W), b)
y = tf.identity(y, name='output')

loss = tf.reduce_mean(tf.square(y - y_),name ="loss")
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
train_op = optimizer.minimize(loss, name='train')

init = tf.global_variables_initializer()

 # Creating a tf.train.Saver adds operations to the graph to save and
 # restore variables from checkpoints.

saver_def = tf.train.Saver().as_saver_def()
with open('graph_mul.pb', 'wb') as f:
  f.write(tf.get_default_graph().as_graph_def().SerializeToString())

print('Operation to initialize variables:       ', init.name)
print('Tensor to feed as input data:            ', x.name)
print('Tensor to feed as training targets:      ', y_.name)
print('Tensor to fetch as prediction:           ', y.name)
print('Operation to train one step:             ', train_op.name)
print('Tensor to be fed for checkpoint filename:', saver_def.filename_tensor_name)
print('Operation to save a checkpoint:          ', saver_def.save_tensor_name)
print('Operation to restore a checkpoint:       ', saver_def.restore_op_name)
print('Tensor to read value of W                ', W.value().name)
print('Tensor to read value of b                ', b.value().name) 
print('Trainable variables: ', tf.trainable_variables())
print('Loss:       ', loss.name)
print('Loss:       ', loss.value)

saver = tf.train.Saver()
sess = tf.Session()
sess.run(init)
saver.save(sess, "/content/sample_data/h"+"/checkpoint_name.ckpt")

# For watching the graph
from __future__ import print_function
writer = tf.summary.FileWriter('.')
writer.add_graph(tf.get_default_graph())
writer.flush()


/content/sample_data/h/checkpoint_name.ckpt.data-00000-of-00001
```

### References: 

 (1)[Google AI Blog](https://ai.googleblog.com/2017/04/federated-learning-collaborative.html)

 (2)[Vision Air](https://vision-air.github.io/index.html)

