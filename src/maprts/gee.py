import ee
import numpy as np

def gen_roi_geometry(long,lat):
  long1,lat1,long2,lat2=gen_roi(long,lat)
  geometry = ee.Geometry.Polygon(coords = [[[long1, lat1], [long1, lat2], [long2, lat2], [long2, lat1],]],
                               proj= 'EPSG:4326',
                               geodesic = None,
                               maxError= 1.,
                               evenOdd = False)
  return geometry


def eeimage_to_np(eeimage,geometry):
  '''
  convert ee.Image to np with rgb channels
  '''
  band_arrs = eeimage.sampleRectangle(region=geometry)
  band_arr_b1 = band_arrs.get('b1')
  band_arr_b2 = band_arrs.get('b2')
  band_arr_b3 = band_arrs.get('b3')

  np_arr_b1 = np.array(band_arr_b1.getInfo())
  np_arr_b2 = np.array(band_arr_b2.getInfo())
  np_arr_b3 = np.array(band_arr_b3.getInfo())

  np_arr_b1 = np.expand_dims(np_arr_b1, 2)
  np_arr_b2 = np.expand_dims(np_arr_b2, 2)
  np_arr_b3 = np.expand_dims(np_arr_b3, 2)

  rgb_img = np.concatenate((np_arr_b1, np_arr_b2, np_arr_b3), 2)
  #print(rgb_img.shape)
  return rgb_img

def label_to_np(blended,geometry):
  '''
  convert ee.Image with overlay labels to numpy arrays
  '''
  band_arrs = blended.sampleRectangle(region=geometry)
  band_arr_b1 = band_arrs.get('b1')
  band_arr_b2 = band_arrs.get('b2')
  band_arr_b3 = band_arrs.get('b3')

  np_arr_b1 = np.array(band_arr_b1.getInfo())
  np_arr_b2 = np.array(band_arr_b2.getInfo())
  np_arr_b3 = np.array(band_arr_b3.getInfo())

  np_arr_b1 = np.expand_dims(np_arr_b1, 2)
  np_arr_b2 = np.expand_dims(np_arr_b2, 2)
  np_arr_b3 = np.expand_dims(np_arr_b3, 2)

  rgb_img = np.concatenate((np_arr_b1, np_arr_b2, np_arr_b3), 2)
  #print(rgb_img.shape)
  compare12=rgb_img[:,:,0]==rgb_img[:,:,1]
  compare23=rgb_img[:,:,1]==rgb_img[:,:,2]
  compare13=rgb_img[:,:,0]==rgb_img[:,:,2]
  identical=np.logical_and(compare12,compare23,compare13)
  return overlay,labels
