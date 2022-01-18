import numpy as np

def gen_random_offset():
  return (np.random.random_sample() - np.random.random_sample())*0.005 #(-0.005,0.005)

def gen_roi(long,lat,side_len=0.01):
  '''
  Generate square roi with offset
  side len is in degrees
  '''
  offset=gen_random_offset()

  # (long1,lat1): up left corner (-0.1,0)
  lat1=lat+(offset-side_len/2)
  long1=long+(offset-side_len/2)#*2.67   #longitude correction

  # (long2,lat2): bottom right corner (0,0.1)
  lat2=lat+(offset+side_len/2)
  long2=long+(offset+side_len/2)#*2.67   #longitude correction

  return long1,lat1,long2,lat2

def pad_arr(img,side_len=280):
  '''
  pad nparrays to a fixed shape (square)
  '''
  if img.ndim==3:  #if the image is rgb
    #print ('padding an rgb image')
    shape=np.zeros((side_len,side_len,3))
    for channel in range(img.shape[-1]):
      shape[:img.shape[0],:img.shape[1],channel]=img[...,channel]
  else:         #1 channel - label
    #print ('padding a label image')
    shape=np.zeros((side_len,side_len))
    shape[:img.shape[0],:img.shape[1]]=img
  return shape

def normalise_int8(arr):
  '''
  normalise values to 0-255
  '''
  return ((arr - arr.min()) * (1/(arr.max() - arr.min()))*255).astype(np.uint8)

def reshape_labels(ls):
  '''
  convert numerical labels to one-hot encoded labels
  '''
  out = np.zeros((ls.shape[0], ls.shape[1], ls.shape[2], 2)) #split background and forground
  for i in range(ls.shape[0]):
    out[i, ..., 0] = ~ls[i,...,-1] #not label
    out[i, ..., 1] = ls[i,...,-1] #label
  return out.astype('bool')


def conc_trainval_img(ds1,aug1,ds2,aug2):
  trainval_img=np.concatenate((
    np.concatenate(((ds1[:-30]/255).astype('float16'),
                                (aug1/255).astype('float16'))),
    np.concatenate(((ds2[:-30]/255).astype('float16'),
                                (aug2/255).astype('float16')))
                  ))
  return trainval_img


def conc_trainval_label(ls1,aug1,ls2,aug2):
  trainval_label=np.concatenate((
  np.concatenate((ls1[:-30],
                          aug1)),
  np.concatenate((ls2[:-30],
                          aug2))
              ))
  return trainval_label
