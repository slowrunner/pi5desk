#!/bin/env python3

# FILE:  create3_ir_dist.py

# Create3 ir_intensity values to *approximate* distance
#   using linear interpolation between empirical test values

#   The ir sensors are not albedo (surface reflectivity) independent
#   so the distances should not be granted great confidence

import numpy as np


# Approximate distance within range of 1cm to 60cm (less or more undefined)
DISTANCES = [0.600, 0.500, 0.400, 0.300, 0.200, 0.100, 0.050, 0.025, 0.010]

# Readings are average of 20 readings at distances
READINGS  = [8    , 13   , 38   , 76   , 151  , 580  , 2044 , 3772 , 3798 ]


def dist_ir_reading(reading):
      UNDEF = -99.0
      dist = np.interp(reading,READINGS,DISTANCES, right=UNDEF, left=UNDEF)
      return dist

def main():

  for reading in [0, 8, 10, 13, 25, 38, 57, 76, 114, 151, 366, 580, 1312, 2044, 2908, 3772, 3785, 3798, 4500] :
    print("reading: {}  dist: {:.3f} m".format(reading, dist_ir_reading(reading)))


if __name__ == "__main__":
  main()
