import tensorflow as tf

def build_tfrecord(img,lb,trainvalsplit=0.8):
  '''
  build tfrecord from nparrays
  trainvalsplit 0.8 means for 80%:20% data will be training:validation
  '''
  print ('building tfrecord')


  n_samples=tf.data.experimental.cardinality(img).numpy()
  n_train=n_sample*trainvalsplit

  tf_train=tf.data.Dataset.from_tensor_slices((img[:-n_train],lb[:-n_train])) #90%training
  tf_val=tf.data.Dataset.from_tensor_slices((img[-n_train:],lb[-n_train:])) #10%validation
  tf_train=tf_train.prefetch(2)
  tf_val=tf_val.prefetch(2)
  return tf_train,tf_val   
